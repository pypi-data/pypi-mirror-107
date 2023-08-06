from typing import Union, Tuple
import torch
from dqc.utils.datastruct import AtomZsType, AtomPosType
from dqc.utils.periodictable import get_atomz

__all__ = ["parse_moldesc"]

def parse_moldesc(moldesc: Union[str, Tuple[AtomZsType, AtomPosType]],
                  dtype: torch.dtype = torch.float64,
                  device: torch.device = torch.device('cpu')) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Parse the string of molecular descriptor and returns tensors of atomzs and
    atom positions.

    Arguments
    ---------
    moldesc: str
        String that describes the system, e.g. ``"H -1 0 0; H 1 0 0"`` for H2 molecule
        separated by 2 Bohr.
    dtype: torch.dtype
        The datatype of the returned atomic positions.
    device: torch.device
        The device to store the returned tensors.

    Returns
    -------
    tuple of 2 tensors
        The first element is the tensor of atomz, and the second element is the
        tensor of atomic positions.
    """
    if isinstance(moldesc, str):
        # TODO: use regex!
        elmts = [
            [
                get_atomz(c.strip()) if i == 0 else float(c.strip())
                for i, c in enumerate(line.split())
            ] for line in moldesc.split(";")]
        atomzs = torch.tensor([line[0] for line in elmts], device=device)
        atompos = torch.tensor([line[1:] for line in elmts], dtype=dtype, device=device)

    else:  # tuple of atomzs, atomposs
        atomzs_raw, atompos_raw = moldesc
        assert len(atomzs_raw) == len(atompos_raw), "Mismatch length of atomz and atompos"
        assert len(atomzs_raw) > 0, "Empty atom list"

        # convert the atomz to tensor
        if not isinstance(atomzs_raw, torch.Tensor):
            atomzs = torch.tensor([get_atomz(at) for at in atomzs_raw], device=device)
        else:
            atomzs = atomzs_raw.to(device)  # already a tensor

        # convert the atompos to tensor
        if not isinstance(atompos_raw, torch.Tensor):
            atompos = torch.as_tensor(atompos_raw, dtype=dtype, device=device)
        else:
            atompos = atompos_raw.to(dtype).to(device)  # already a tensor

    # convert to dtype if atomzs is a floating point tensor, not an integer tensor
    if atomzs.is_floating_point():
        atomzs = atomzs.to(dtype)

    return atomzs, atompos
