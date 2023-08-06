import torch
import xitorch as xt
from typing import List, Optional
import dqc.hamilton.intor as intor
from dqc.df.base_df import BaseDF
from dqc.hamilton.orbconverter import OrbitalOrthogonalizer
from dqc.utils.datastruct import DensityFitInfo
from dqc.utils.mem import get_memory
from dqc.utils.config import config
from dqc.utils.misc import logger

class DFMol(BaseDF):
    """
    DFMol represents the class of density fitting for an isolated molecule.
    """
    def __init__(self, dfinfo: DensityFitInfo, wrapper: intor.LibcintWrapper,
                 orthozer: Optional[OrbitalOrthogonalizer] = None):
        self.dfinfo = dfinfo
        self.wrapper = wrapper
        self._is_built = False
        self._precompute_elmat = True
        self._orthozer = orthozer

    def build(self) -> BaseDF:
        self._is_built = True

        # construct the matrix used to calculate the electron repulsion for
        # density fitting method
        method = self.dfinfo.method
        auxbasiswrapper = intor.LibcintWrapper(self.dfinfo.auxbases,
                                               spherical=self.wrapper.spherical)
        basisw, auxbw = intor.LibcintWrapper.concatenate(self.wrapper, auxbasiswrapper)

        if method == "coulomb":
            logger.log("Calculating the 2e2c integrals")
            j2c = intor.coul2c(auxbw)  # (nxao, nxao)
            logger.log("Calculating the 2e3c integrals")
            j3c = intor.coul3c(basisw, other1=basisw,
                               other2=auxbw)  # (nao, nao, nxao)
        elif method == "overlap":
            j2c = intor.overlap(auxbw)  # (nxao, nxao)
            # TODO: implement overlap3c
            raise NotImplementedError(
                "Density fitting with overlap minimization is not implemented")
        self._j2c = j2c  # (nxao, nxao)
        self._j3c = j3c  # (nao, nao, nxao)
        logger.log("Precompute matrix for density fittings")
        self._inv_j2c = torch.inverse(j2c)

        # if the memory is too big, then don't precompute elmat
        if get_memory(j3c) > config.THRESHOLD_MEMORY:
            self._precompute_elmat = False
        else:
            self._precompute_elmat = True
            self._el_mat = torch.matmul(j3c, self._inv_j2c)  # (nao, nao, nxao)

        logger.log("Density fitting done")
        return self

    def get_elrep(self, dm: torch.Tensor) -> xt.LinearOperator:
        # dm: (*BD, nao, nao)
        # elrep_mat: (nao, nao, nao, nao)
        # return: (*BD, nao, nao)

        # convert the dm into the original cgto basis
        if self._orthozer is not None:
            dm = self._orthozer.unconvert_dm(dm)

        if self._precompute_elmat:
            df_coeffs = torch.einsum("...ij,ijk->...k", dm, self._el_mat)  # (*BD, nxao)
        else:
            temp = torch.einsum("...ij,ijl->...l", dm, self._j3c)
            df_coeffs = torch.einsum("...l,lk->...k", temp, self._inv_j2c)  # (*BD, nxao)

        mat = torch.einsum("...k,ijk->...ij", df_coeffs, self._j3c)  # (*BD, nao, nao)
        mat = (mat + mat.transpose(-2, -1)) * 0.5
        if self._orthozer is not None:
            mat = self._orthozer.convert2(mat)
        return xt.LinearOperator.m(mat, is_hermitian=True)

    @property
    def j2c(self) -> torch.Tensor:
        return self._j2c

    @property
    def j3c(self) -> torch.Tensor:
        return self._j3c

    def getparamnames(self, methodname: str, prefix: str = "") -> List[str]:
        if methodname == "get_elrep":
            if self._precompute_elmat:
                params = [prefix + "_el_mat", prefix + "_j3c"]
            else:
                params = [prefix + "_inv_j2c", prefix + "_j3c"]
            if self._orthozer is not None:
                pfix = prefix + "_orthozer."
                params += self._orthozer.getparamnames("unconvert_dm", prefix=pfix) + \
                    self._orthozer.getparamnames("convert2", prefix=pfix)
            return params
        else:
            raise KeyError("getparamnames has no %s method" % methodname)
