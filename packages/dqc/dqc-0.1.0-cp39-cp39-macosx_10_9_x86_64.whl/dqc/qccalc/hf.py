from typing import Optional, Dict, Any, Tuple, List, Union, overload
import torch
import xitorch as xt
import xitorch.linalg
import xitorch.optimize
from dqc.system.base_system import BaseSystem
from dqc.qccalc.scf_qccalc import SCF_QCCalc, BaseSCFEngine
from dqc.utils.datastruct import SpinParam

__all__ = ["HF"]

class HF(SCF_QCCalc):
    """
    Performing Restricted or Unrestricted Kohn-Sham DFT calculation.

    Arguments
    ---------
    system: BaseSystem
        The system to be calculated.
    xc: str
        The exchange-correlation potential and energy to be used.
    vext: torch.Tensor or None
        The external potential applied to the system. It must have the shape of
        ``(*BV, system.get_grid().shape[-2])``
    restricted: bool or None
        If True, performing restricted Kohn-Sham DFT. If False, it performs
        the unrestricted Kohn-Sham DFT.
        If None, it will choose True if the system is unpolarized and False if
        it is polarized
    variational: bool
        If True, then use optimization of the free orbital parameters to find
        the minimum energy.
        Otherwise, use self-consistent iterations.
    """

    def __init__(self, system: BaseSystem,
                 restricted: Optional[bool] = None,
                 variational: bool = False):

        engine = _HFEngine(system, restricted)
        super().__init__(engine, variational)

class _HFEngine(BaseSCFEngine):
    """
    Engine to be used with Hartree Fock.
    This class provides the calculation of the self-consistency iteration step
    and the calculation of the post-calculation properties.
    """
    def __init__(self, system: BaseSystem,
                 restricted: Optional[bool] = None):

        # decide if this is restricted or not
        if restricted is None:
            self._polarized = bool(system.spin != 0)
        else:
            self._polarized = not restricted

        # build the basis
        self._hamilton = system.get_hamiltonian().build()
        self._system = system

        # get the orbital info
        self._orb_weight = system.get_orbweight(polarized=self._polarized)  # (norb,)
        self._norb = SpinParam.apply_fcn(lambda orb_weight: int(orb_weight.shape[-1]),
                                         self._orb_weight)

        # set up the 1-electron linear operator
        self._core1e_linop = self._hamilton.get_kinnucl()  # kinetic and nuclear

    def get_system(self) -> BaseSystem:
        return self._system

    @property
    def shape(self):
        # returns the shape of the density matrix
        return self._core1e_linop.shape

    @property
    def dtype(self):
        # returns the dtype of the density matrix
        return self._core1e_linop.dtype

    @property
    def device(self):
        # returns the device of the density matrix
        return self._core1e_linop.device

    @property
    def polarized(self):
        return self._polarized

    def dm2scp(self, dm: Union[torch.Tensor, SpinParam[torch.Tensor]]) -> torch.Tensor:
        # convert from density matrix to a self-consistent parameter (scp)
        if isinstance(dm, torch.Tensor):  # unpolarized
            # scp is the fock matrix
            return self.__dm2fock(dm).fullmatrix()
        else:  # polarized
            # scp is the concatenated fock matrix
            fock = self.__dm2fock(dm)
            mat_u = fock.u.fullmatrix().unsqueeze(0)
            mat_d = fock.d.fullmatrix().unsqueeze(0)
            return torch.cat((mat_u, mat_d), dim=0)

    def scp2dm(self, scp: torch.Tensor) -> Union[torch.Tensor, SpinParam[torch.Tensor]]:
        # scp is like KS, using the concatenated Fock matrix
        if not self._polarized:
            fock = xt.LinearOperator.m(_symm(scp), is_hermitian=True)
            return self.__fock2dm(fock)
        else:
            fock_u = xt.LinearOperator.m(_symm(scp[0]), is_hermitian=True)
            fock_d = xt.LinearOperator.m(_symm(scp[1]), is_hermitian=True)
            return self.__fock2dm(SpinParam(u=fock_u, d=fock_d))

    def scp2scp(self, scp: torch.Tensor) -> torch.Tensor:
        # self-consistent iteration step from a self-consistent parameter (scp)
        # to an scp
        dm = self.scp2dm(scp)
        return self.dm2scp(dm)

    def aoparams2ene(self, aoparams: torch.Tensor, with_penalty: Optional[float] = None) -> torch.Tensor:
        # calculate the energy from the atomic orbital params
        dm, penalty = self.aoparams2dm(aoparams, with_penalty)
        ene = self.dm2energy(dm)
        return (ene + penalty) if penalty is not None else ene

    def aoparams2dm(self, aoparams: torch.Tensor, with_penalty: Optional[float] = None) -> \
            Tuple[Union[torch.Tensor, SpinParam[torch.Tensor]], Optional[torch.Tensor]]:
        # convert the aoparams to density matrix and penalty factor
        aop = self.unpack_aoparams(aoparams)  # tensor or SpinParam of tensor
        dm_penalty = SpinParam.apply_fcn(
            lambda aop, orb_weight: self._hamilton.ao_orb_params2dm(aop, orb_weight, with_penalty=with_penalty),
            aop, self._orb_weight
        )
        if with_penalty is not None:
            dm = SpinParam.apply_fcn(lambda dm_penalty: dm_penalty[0], dm_penalty)
            penalty: Optional[torch.Tensor] = SpinParam.sum(
                SpinParam.apply_fcn(lambda dm_penalty: dm_penalty[1], dm_penalty))
        else:
            dm = dm_penalty
            penalty = None
        return dm, penalty

    def pack_aoparams(self, aoparams: Union[torch.Tensor, SpinParam[torch.Tensor]]) -> torch.Tensor:
        # if polarized, then pack it by concatenating them in the last dimension
        if isinstance(aoparams, SpinParam):
            return torch.cat((aoparams.u, aoparams.d), dim=-1)
        else:
            return aoparams

    def unpack_aoparams(self, aoparams: torch.Tensor) -> Union[torch.Tensor, SpinParam[torch.Tensor]]:
        # if polarized, then construct the SpinParam (reverting the pack_aoparams)
        if isinstance(self._norb, SpinParam):
            return SpinParam(u=aoparams[..., :self._norb.u], d=aoparams[..., self._norb.u:])
        else:
            return aoparams

    def set_eigen_options(self, eigen_options: Dict[str, Any]) -> None:
        # set the eigendecomposition (diagonalization) option
        self.eigen_options = eigen_options

    def dm2energy(self, dm: Union[torch.Tensor, SpinParam[torch.Tensor]]) -> torch.Tensor:
        # calculate the energy given the density matrix
        dmtot = SpinParam.sum(dm)
        e_core = self._hamilton.get_e_hcore(dmtot)
        e_elrep = self._hamilton.get_e_elrep(dmtot)
        e_exch = self._hamilton.get_e_exchange(dm)
        return e_core + e_elrep + e_exch + self._system.get_nuclei_energy()

    @overload
    def __dm2fock(self, dm: torch.Tensor) -> xt.LinearOperator:
        ...

    @overload
    def __dm2fock(self, dm: SpinParam[torch.Tensor]) -> SpinParam[xt.LinearOperator]:
        ...

    def __dm2fock(self, dm):
        vhf = self.__dm2vhf(dm)
        fock = SpinParam.apply_fcn(lambda vhf: self._core1e_linop + vhf, vhf)
        return fock

    @overload
    def __dm2vhf(self, dm: torch.Tensor) -> xt.LinearOperator:
        ...

    @overload
    def __dm2vhf(self, dm: SpinParam[torch.Tensor]) -> SpinParam[xt.LinearOperator]:
        ...

    def __dm2vhf(self, dm):
        # from density matrix, returns the linear operator on electron-electron
        # coulomb and exchange
        elrep = self._hamilton.get_elrep(SpinParam.sum(dm))
        exch = self._hamilton.get_exchange(dm)
        vhf = SpinParam.apply_fcn(lambda exch: elrep + exch, exch)
        return vhf

    @overload
    def __fock2dm(self, fock: xt.LinearOperator) -> torch.Tensor:
        ...

    @overload
    def __fock2dm(self, fock: SpinParam[xt.LinearOperator]) -> SpinParam[torch.Tensor]:  # type: ignore
        ...

    def __fock2dm(self, fock):
        # diagonalize the fock matrix and obtain the density matrix
        eigvals, eigvecs = self.diagonalize(fock, self._norb)
        dm = SpinParam.apply_fcn(lambda eivecs, orb_weights: self._hamilton.ao_orb2dm(eivecs, orb_weights),
                                 eigvecs, self._orb_weight)
        return dm

    @overload
    def diagonalize(self, fock: xt.LinearOperator, norb: int) -> Tuple[torch.Tensor, torch.Tensor]:
        ...

    @overload
    def diagonalize(self, fock: SpinParam[xt.LinearOperator], norb: SpinParam[int],  # type: ignore
                    ) -> Tuple[SpinParam[torch.Tensor], SpinParam[torch.Tensor]]:
        ...

    def diagonalize(self, fock, norb):
        ovlp = self._hamilton.get_overlap()
        if isinstance(fock, SpinParam):
            assert isinstance(self._norb, SpinParam)
            eivals_u, eivecs_u = xitorch.linalg.lsymeig(
                A=fock.u,
                neig=norb.u,
                M=ovlp,
                **self.eigen_options)
            eivals_d, eivecs_d = xitorch.linalg.lsymeig(
                A=fock.d,
                neig=norb.d,
                M=ovlp,
                **self.eigen_options)
            return SpinParam(u=eivals_u, d=eivals_d), SpinParam(u=eivecs_u, d=eivecs_d)
        else:
            return xitorch.linalg.lsymeig(
                A=fock,
                neig=norb,
                M=ovlp,
                **self.eigen_options)

    def getparamnames(self, methodname: str, prefix: str = "") -> List[str]:
        if methodname == "scp2scp":
            return self.getparamnames("scp2dm", prefix=prefix) + \
                self.getparamnames("dm2scp", prefix=prefix)
        elif methodname == "scp2dm":
            return self.getparamnames("__fock2dm", prefix=prefix)
        elif methodname == "dm2scp":
            return self.getparamnames("__dm2fock", prefix=prefix)
        elif methodname == "aoparams2ene":
            return self.getparamnames("aoparams2dm", prefix=prefix) + \
                self.getparamnames("dm2energy", prefix=prefix)
        elif methodname == "aoparams2dm":
            if isinstance(self._orb_weight, SpinParam):
                params = [prefix + "_orb_weight.u", prefix + "_orb_weight.d"]
            else:
                params = [prefix + "_orb_weight"]
            return params + \
                self._hamilton.getparamnames("ao_orb_params2dm", prefix=prefix + "_hamilton.")
        elif methodname == "pack_aoparams":
            return []
        elif methodname == "unpack_aoparams":
            return []
        elif methodname == "dm2energy":
            hprefix = prefix + "_hamilton."
            sprefix = prefix + "_system."
            return self._hamilton.getparamnames("get_e_hcore", prefix=hprefix) + \
                self._hamilton.getparamnames("get_e_elrep", prefix=hprefix) + \
                self._hamilton.getparamnames("get_e_exchange", prefix=hprefix) + \
                self._system.getparamnames("get_nuclei_energy", prefix=sprefix)
        elif methodname == "__fock2dm":
            if isinstance(self._orb_weight, SpinParam):
                params = [prefix + "_orb_weight.u", prefix + "_orb_weight.d"]
            else:
                params = [prefix + "_orb_weight"]
            return self.getparamnames("diagonalize", prefix=prefix) + \
                self._hamilton.getparamnames("ao_orb2dm", prefix=prefix + "_hamilton.") + \
                params
        elif methodname == "__dm2fock":
            return self._core1e_linop._getparamnames(prefix=prefix + "_core1e_linop.") + \
                self.getparamnames("__dm2vhf", prefix=prefix)
        elif methodname == "__dm2vhf":
            hprefix = prefix + "_hamilton."
            return self._hamilton.getparamnames("get_elrep", prefix=hprefix) + \
                self._hamilton.getparamnames("get_exchange", prefix=hprefix)
        elif methodname == "diagonalize":
            return self._hamilton.getparamnames("get_overlap", prefix=prefix + "_hamilton.")
        else:
            raise KeyError("Method %s has no paramnames set" % methodname)
        return []  # TODO: to complete

def _symm(scp: torch.Tensor):
    # forcely symmetrize the tensor
    return (scp + scp.transpose(-2, -1)) * 0.5
