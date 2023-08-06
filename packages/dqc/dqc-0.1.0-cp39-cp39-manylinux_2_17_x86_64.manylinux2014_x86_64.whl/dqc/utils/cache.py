from __future__ import annotations
import contextlib
from typing import Optional, List, Callable, Dict, Any, Tuple
import warnings
import torch
import numpy as np
import h5py

class Cache(object):
    """
    Internal object to store/load cache for heavy-load calculations.
    For a class to be able to use cache, it has to have cache as its members.
    The same cache object can also be passed to other object either via
        `.add_prefix` method or just passed as it is.
    The list of cacheable parameters are constructed within the class.
    The file to store cache also set within the class via `set` method, if no
        file is set, then the cache does not work.
    To load/store cache, the context handler, `.open()` needs to be called.
    We use the magic method `cache` here to load/store cache, i.e. if the given
        dataset is not in the cache, then it is calculated then stored.
    Otherwise, the dataset is just loaded from the cache file.
    To avoid loading the wrong cache (e.g. the same file name is set for two
        different objects), we provide `check_signature` method which will
        raise a warning if the signature from the cached file and the input of
        `check_signature` do not match.
    """
    def __init__(self):
        self._cacheable_pnames: List[str] = []
        self._fname: Optional[str] = None
        self._pnames_to_cache: Optional[List[str]] = None
        self._fhandler: Optional[h5py.File] = None

    def set(self, fname: str, pnames: Optional[List[str]] = None):
        # set up the cache
        self._fname = fname
        self._pnames_to_cache = pnames

    def cache(self, pname: str, fcn: Callable[[], torch.Tensor]) -> torch.Tensor:
        # if not has been set, then just calculate and return
        if not self.isset():
            return fcn()

        # if the param is not to be cached, then just calculate and return
        if not self._pname_to_cache(pname):
            return fcn()

        # get the dataset name
        dset_name = self._pname2dsetname(pname)

        # check if dataset name is in the file (cache exist)
        file = self._get_file_handler()
        if dset_name in file:
            # retrieve the dataset if it has been computed before
            res = self._load_dset(dset_name, file)
        else:
            # if not in the file, then compute the tensor and save the cache
            res = fcn()
            self._save_dset(dset_name, file, res)
        return res

    def cache_multi(self, pnames: List[str], fcn: Callable[[], Tuple[torch.Tensor, ...]]) \
            -> Tuple[torch.Tensor, ...]:

        if not self.isset():
            return fcn()

        # if any of the pnames not to be cached, then just calculate and return
        if not all([self._pname_to_cache(pname) for pname in pnames]):
            return fcn()

        # get the dataset names
        dset_names = [self._pname2dsetname(pname) for pname in pnames]

        # get the file handler
        file = self._get_file_handler()

        # check if all the dataset is in the cache file, otherwise, just evaluate
        all_dset_names_in_file = all([dset_name in file for dset_name in dset_names])
        if all_dset_names_in_file:
            all_res = tuple(self._load_dset(dset_name, file) for dset_name in dset_names)
        else:
            all_res = fcn()
            for dset_name, res in zip(dset_names, all_res):
                self._save_dset(dset_name, file, res)
        return all_res

    @contextlib.contextmanager
    def open(self):
        # open the cache file
        try:
            if self._fname is not None:
                self._fhandler = h5py.File(self._fname, "a")
            yield self._fhandler
        finally:
            if self._fname is not None:
                self._fhandler.close()
                self._fhandler = None

    def add_prefix(self, prefix: str) -> Cache:
        # return a Cache object that will add the prefix for every input of
        # parameter names
        prefix = _normalize_prefix(prefix)
        return _PrefixedCache(self, prefix)

    def add_cacheable_params(self, pnames: List[str]):
        # add the cacheable parameter names
        self._cacheable_pnames.extend(pnames)

    def get_cacheable_params(self) -> List[str]:
        # return the cacheable parameter names
        return self._cacheable_pnames

    def check_signature(self, sig_dict: Dict[str, Any], _groupname: Optional[str] = "/"):
        # Executed while the file is opened, if there is no signature, then add
        # the signature, if there is a signature in the file, then match it.
        # If they do not match, print a warning, otherwise, do nothing
        # _groupname is internal parameter within this class, should not be
        # specified by classes other than Cache and its inheritances.

        if not self.isset():
            return

        fh = self._get_file_handler()
        sig_attrname = "signature"

        # get the group
        if _groupname in fh:
            group = fh[_groupname]
        else:
            group = fh.create_group(_groupname)

        # create the signature string
        sig_str = "\n\n".join(["%s:\n%s" % (k, str(v)) for (k, v) in sig_dict.items()])

        # if the signature does not exist, then write the signature as an attribute
        if sig_attrname not in group.attrs:
            group.attrs[sig_attrname] = str(sig_str)

        # if the signature exist, then check it, if it does not match, raise a warning
        else:
            cached_sig = str(group.attrs[sig_attrname])
            if cached_sig != sig_str:
                msg = ("Mismatch of the cached signature.\nCached signature:\n%s\n"
                       "-----------------------\n"
                       "Current signature:\n%s" % (cached_sig, sig_str))
                warnings.warn(msg)

        group.attrs["signature"] = str(sig_str)

    @staticmethod
    def get_dummy() -> Cache:
        # returns a dummy cache that does not do anything
        return _DummyCache()

    def _pname_to_cache(self, pname: str) -> bool:
        # check if the input parameter name is to be cached
        return (self._pnames_to_cache is None) or (pname in self._pnames_to_cache)

    def _pname2dsetname(self, pname: str) -> str:
        # convert the parameter name to dataset name
        return pname.replace(".", "/")

    def _get_file_handler(self) -> h5py.File:
        # return the file handler, if the file is not opened yet, then raise an error
        if self._fhandler is None:
            msg = "The cache file has not been opened yet, please use .open() before reading/writing to the cache"
            raise RuntimeError(msg)
        else:
            return self._fhandler

    def isset(self) -> bool:
        # returns the indicator whether the cache object has been set
        return self._fname is not None

    def _load_dset(self, dset_name: str, fhandler: h5py.File) -> torch.Tensor:
        # load the dataset from the file handler (check is performed outside)
        dset_np = np.asarray(fhandler[dset_name])
        dset = torch.as_tensor(dset_np)
        return dset

    def _save_dset(self, dset_name: str, fhandler: h5py.File, dset: torch.Tensor):
        # save res to the h5py in the dataset name
        fhandler[dset_name] = dset.detach()

class _PrefixedCache(Cache):
    # this class adds a prefix to every parameter names input
    def __init__(self, obj: Cache, prefix: str):
        self._obj = obj
        self._prefix = prefix

    def set(self, fname: str, pnames: Optional[List[str]] = None):
        # set must only be done in the parent object, not in the children objects
        raise RuntimeError("Cache.set() must be done on non-prefixed cache")

    def cache(self, pname: str, fcn: Callable[[], torch.Tensor]) -> torch.Tensor:
        return self._obj.cache(self._prefixed(pname), fcn)

    def cache_multi(self, pnames: List[str], fcn: Callable[[], Tuple[torch.Tensor, ...]]) \
            -> Tuple[torch.Tensor, ...]:
        ppnames = [self._prefixed(pname) for pname in pnames]
        return self._obj.cache_multi(ppnames, fcn)

    @contextlib.contextmanager
    def open(self):
        with self._obj.open() as f:
            try:
                yield f
            finally:
                pass

    def add_prefix(self, prefix: str) -> Cache:
        # return a deeper prefixed object
        prefix = self._prefixed(_normalize_prefix(prefix))
        return self._obj.add_prefix(prefix)

    def add_cacheable_params(self, pnames: List[str]):
        # add the cacheable parameter names
        pnames = [self._prefixed(pname) for pname in pnames]
        self._obj.add_cacheable_params(pnames)

    def get_cacheable_params(self) -> List[str]:
        # this can only be done on the root cache (non-prefixed) to avoid
        # confusion about which name should be provided (absolute or relative)
        raise RuntimeError("Cache.get_cacheable_params() must be done on non-prefixed cache")

    def check_signature(self, sig_dict: Dict[str, Any], _groupname: Optional[str] = "/"):
        # use the prefix as the groupname to do signature check of the root object
        if not self.isset():
            return

        groupname = "/" + self._prefix.replace(".", "/")
        if groupname.endswith("/"):
            groupname = groupname[:-1]

        self._obj.check_signature(sig_dict, _groupname=groupname)

    def isset(self) -> bool:
        return self._obj.isset()

    def _prefixed(self, pname: str) -> str:
        # returns the prefixed name
        return self._prefix + pname

class _DummyCache(Cache):
    # this class just an interface of cache without doing anything
    def __init__(self):
        pass

    def set(self, fname: str, pnames: Optional[List[str]] = None):
        pass

    def cache(self, pname: str, fcn: Callable[[], torch.Tensor]) -> torch.Tensor:
        return fcn()

    def cache_multi(self, pnames: List[str], fcn: Callable[[], Tuple[torch.Tensor, ...]]) \
            -> Tuple[torch.Tensor, ...]:
        return fcn()

    @contextlib.contextmanager
    def open(self):
        try:
            yield None
        finally:
            pass

    def add_prefix(self, prefix: str) -> Cache:
        # return a deeper prefixed object
        return self

    def add_cacheable_params(self, pnames: List[str]):
        pass

    def get_cacheable_params(self) -> List[str]:
        return []

    def check_signature(self, sig_dict: Dict[str, Any], _groupname: Optional[str] = "/"):
        pass

    def isset(self):
        return False

def _normalize_prefix(prefix: str) -> str:
    # added a dot at the end of prefix if it is not so
    if not prefix.endswith("."):
        prefix = prefix + "."
    return prefix
