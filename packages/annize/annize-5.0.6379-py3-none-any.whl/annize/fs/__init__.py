# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import abc
import datetime
import os
import shutil
import subprocess
import time
import typing as t

import annize.fs

_TransferPredicate = t.Callable[[str, "FsEntry", "FsEntry"], bool]


class _TransferHelper:

    def __transfer_prepare(self, srcf: "FsEntry", dstf: "FsEntry", overwrite: bool) -> None:
        if not srcf.exists():
            raise Exception("TODO")
        if dstf.exists():
            if overwrite:
                dstf.remove()
            else:
                raise IOError("TODO")

    def transfer_action_copy(self, srcf: "FsEntry", dstf: "FsEntry", overwrite: bool) -> None:
        self.__transfer_prepare(srcf, dstf, overwrite)
        if srcf.is_link():
            os.symlink(os.readlink(srcf.path()), dstf.path())
        elif srcf.is_dir():
            shutil.copytree(srcf.readable_path(), dstf.path(), symlinks=True)  # TODO all usages of shutil.copy* : check what it does with symlinks!
        else:
            shutil.copy2(srcf.readable_path(), dstf.path())

    def transfer_action_move(self, srcf: "FsEntry", dstf: "FsEntry", overwrite: bool) -> None:
        self.__transfer_prepare(srcf, dstf, overwrite)
        shutil.move(srcf.path(), dstf.path())

    def __transfer_dirmerge(self, action: t.Callable,
                            transfer_predicate: t.Optional[_TransferPredicate]) -> t.Callable:
        # TODO transfer_predicate also outside here
        def merge(srcf: "FsEntry", dstf: "FsEntry", overwrite: bool, _relpath: str = "") -> None:
            if transfer_predicate:
                if not transfer_predicate(_relpath, srcf, dstf):
                    return
            if not srcf.is_dir():  # TODO noh links
                raise Exception("TODO")
            if dstf.exists() and not dstf.is_dir():
                raise Exception("TODO")
            for srccf in srcf.children():
                dstcf = dstf.child_by_relative_path(srccf.basename())
                if srccf.is_dir():
                    merge(srccf, dstcf, overwrite, f"{_relpath}/{srccf.basename()}")
                else:
                    dstcf.parent().mkdir()
                    action(srccf, dstcf, overwrite)
        return merge

    def transfer_to(self, srcf: "FsEntry", path: str, *, merge: bool, overwrite: bool, action: t.Callable,
                    transfer_predicate: t.Optional[_TransferPredicate] = None) -> "FsEntry":
        if merge:
            if srcf.is_dir():
                action = self.__transfer_dirmerge(action, transfer_predicate)
            else:  # TODO messy
                overwrite = True
        result = fsentry_by_path(path, is_ownable=True, is_owned=True)
        fsentry_by_path(result.parent().readable_path(), is_ownable=True, is_owned=True).mkdir()
        action(srcf, result, overwrite)
        return result.disowned()


class FsEntry(abc.ABC):

    def __init__(self, *, is_ownable: bool = False, is_owned: bool = False):
        if is_owned and not is_ownable:
            raise ValueError("is_owned must not be True unless is_owned also is")
        self.__transferhelper = _TransferHelper()
        self.__is_ownable = is_ownable
        self.__is_owned = is_owned

#TODO some abstract stuff
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def owned(self, allow_clone: bool = True) -> "FsEntry":
        if not self.is_ownable or self.is_owned:
            if not allow_clone:
                raise OriginalOwnershipImpossibleError(self.readable_path())
            return self.temp_clone().owned()
        return fsentry_by_path(self.readable_path(), is_ownable=True, is_owned=True)

    def disowned(self) -> "FsEntry":  # TODO also "unownable()" ?!
        if not self.is_owned:
            raise BadDisowningError(self.readable_path())
        return fsentry_by_path(self.readable_path(), is_ownable=True, is_owned=False)

    @property
    def is_owned(self) -> bool:
        return self.__is_owned

    @property
    def is_ownable(self) -> bool:
        return self.__is_ownable

    def readable_path(self) -> str:
        raise NotImplementedError()

    def path(self) -> str:
        if not self.is_owned:
            raise MissingOwnershipError(self.readable_path())
        return self.readable_path()

    def is_file(self, follow_symlinks: bool = True) -> bool:
        if (not follow_symlinks) and self.is_link():
            return False
        return os.path.isfile(self.readable_path())

    def is_dir(self, follow_symlinks: bool = True) -> bool:
        if (not follow_symlinks) and self.is_link():
            return False
        return os.path.isdir(self.readable_path())

    def is_link(self) -> bool:
        return os.path.islink(self.readable_path())

    def exists(self) -> bool:
        return os.path.exists(self.readable_path())

    def basename(self) -> str:
        return os.path.basename(self.readable_path())

    def filesize(self) -> int:
        return os.path.getsize(self.readable_path())

    def created_time(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(os.path.getctime(self.readable_path()))

    def modified_time(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(os.path.getmtime(self.readable_path()))

    def children(self) -> t.List["FsEntry"]:
        return [self.child_by_relative_path(x) for x in sorted(os.listdir(self.readable_path()))]

    def child_by_relative_path(self, name) -> "FsEntry":
        return fsentry_by_path(f"{self.readable_path()}/{name or ''}",
                               is_ownable=self.is_ownable, is_owned=self.is_owned)  # TODO rlly? , is_ownable=..., ...

    def parent(self) -> t.Optional["FsEntry"]:
        parentpath = os.path.dirname(self.readable_path())
        if parentpath != self.readable_path():
            return fsentry_by_path(parentpath, is_ownable=self.is_ownable, is_owned=self.is_owned)
            # TODO rlly? , is_ownable=..., ...
        return None

    def copy_to(self, path: str, *, path_is_parent: bool = False, merge: bool = False,
                overwrite: bool = False, transfer_predicate: t.Optional[_TransferPredicate] = None) -> "FsEntry":
        if path_is_parent:
            return self.copy_to(f"{path}/{self.basename()}", merge=merge, overwrite=overwrite,
                                transfer_predicate=transfer_predicate)
        return self.__transferhelper.transfer_to(self, path, merge=merge, overwrite=overwrite,
                                                 action=self.__transferhelper.transfer_action_copy,
                                                 transfer_predicate=transfer_predicate)

    def move_to(self, path: str, *, path_is_parent: bool = False, merge: bool = False,
                overwrite: bool = False, transfer_predicate: t.Optional[_TransferPredicate] = None) -> "FsEntry":
        # TODO other FsEntry instead of path?!
        if path_is_parent:
            return self.move_to(f"{path}/{self.basename()}", merge=merge, overwrite=overwrite,
                                transfer_predicate=transfer_predicate)
        result = self.__transferhelper.transfer_to(self, path, merge=merge, overwrite=overwrite,
                                                   action=self.__transferhelper.transfer_action_move,
                                                   transfer_predicate=transfer_predicate)
        if merge:  # TODO nicer?!  TODO breaks transfer_predicate
            shutil.rmtree(self.path(), ignore_errors=True)
        return result

    def remove(self) -> None:  # TODO windows retry loop
        if self.exists():
            if self.is_dir(follow_symlinks=False):
                shutil.rmtree(self.path())
            else:
                os.unlink(self.path())

    def mkdir(self, *, exist_ok: bool = True) -> None:
        if self.exists() and not self.is_dir():
            raise Exception("TODO")
        os.makedirs(self.path(), exist_ok=exist_ok)

    def read_file(self) -> bytes:
        with open(self.readable_path(), "rb") as f:
            return f.read()

    def write_file(self, content: t.AnyStr) -> None:
        if isinstance(content, str):
            content = content.encode()
        self.parent().mkdir()
        with open(self.path(), "wb") as f:
            f.write(content)

    def temp_clone(self, *, temprootpath: t.Optional[str] = None, basename: t.Optional[str] = None) -> "FsEntry":
        import annize.fs.temp
        result = annize.fs.temp.fresh_temp_dir(temprootpath=temprootpath)
        dest = result.child_by_relative_path(basename or self.basename())
        self.copy_to(dest.owned(allow_clone=False).path())
        result.restrict_path(dest.basename())
        return result


class _SimpleFsEntry(FsEntry):

    def __init__(self, path: str, *, is_ownable: bool = False, is_owned: bool = False):
        super().__init__(is_ownable=is_ownable, is_owned=is_owned)
        self.__path = os.path.abspath(path)

    def readable_path(self):
        return self.__path


class AdHocFsEntry(FsEntry):  # TODO owning TODO refactor TODO test

    def __init__(self):
        super().__init__()
        self.__inner = None

    def _initialize(self) -> FsEntry:
        raise NotImplementedError()

    def __getinner(self):
        if not self.__inner:
            self.__inner = self._initialize()
            if not self.__inner:
                raise Exception("TODO")
        return self.__inner

    def readable_path(self):  # TODO efficient & correct?
        return self.__getinner().readable_path()

    def __enter__(self):
        return self.__getinner().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.__getinner().__exit__(exc_type, exc_val, exc_tb)


def fsentry_by_path(path: str, *, is_ownable: bool = False, is_owned: bool = False) -> FsEntry:
    # TODO
    return _SimpleFsEntry(path, is_ownable=is_ownable, is_owned=is_owned)


class Mount:

    def __init__(self, src: str, dst: str, *, options: t.Iterable[str] = (),
                 mounter: t.Optional[t.Iterable[str]] = None, unmounter: t.Optional[t.Iterable[str]] = None):
        self.__src = src
        self.__destination = annize.fs.fsentry_by_path(dst, is_ownable=True)
        self.__options = options or []
        self.__mounter = mounter or ["mount"]
        self.__unmounter = unmounter or ["umount"]

    @property
    def destination(self) -> FsEntry:
        return self.__destination

    def __enter__(self):
        subprocess.check_call([*self.__mounter, self.__src, self.__destination.readable_path(), *self.__options])
        return self

    def __exit__(self, etype, evalue, etraceback):
        for i in reversed(range(4)):
            subprocess.call(["sync"])
            try:
                subprocess.check_call([*self.__unmounter, self.__destination.readable_path()])
                break
            except subprocess.CalledProcessError:
                if i == 0:
                    raise
            time.sleep(1)
        else:
            raise Exception("TODO")


class ChDir:#TODO
    """
    Temporarily changes the current working directory in a scope of the :samp:`with` keyword.
    """

    def __init__(self, path: str):
        """
        :param path: The path to the new working directory.
        """
        self.newpath = path

    def __enter__(self):
        self.oldpath = os.getcwd()
        os.chdir(self.newpath)
        return self

    def __exit__(self, etype, evalue, etraceback):
        os.chdir(self.oldpath)


class MissingOwnershipError(RuntimeError):

    def __init__(self, path: str):
        super().__init__(f"Attempted to get read/write access to '{path}' without owning it")


class OriginalOwnershipImpossibleError(RuntimeError):

    def __init__(self, path: str):
        super().__init__(f"Attempted to acquire ownership of uncloned '{path}' when it was already owned")


class BadDisowningError(RuntimeError):

    def __init__(self, path: str):
        super().__init__(f"Attempted to disown '{path}' without owning it")
