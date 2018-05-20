""" Speed up shutil.copyfile by using sendfile system call. """

__version__ = "1.0.3"
__author__ = "desbma"
__license__ = "PSFL"

import errno
import os
import shutil
import stat
import sys


if not sys.platform.startswith("win32"):
  try:
    _sendfile = os.sendfile
  except AttributeError:
    import sendfile
    _sendfile = sendfile.sendfile


  # errnos sendfile can set if not supported on the system
  _sendfile_err_codes = {code for code, name in errno.errorcode.items() \
                         if name in ("EIO", "EINVAL", "ENOSYS", "ENOTSUP",
                                     "EBADF", "ENOTSOCK", "EOPNOTSUPP")}


  def _copyfile_sendfile(fsrc, fdst):
    """Copy data from fsrc to fdst using sendfile, return True if success. """
    status = False
    max_bcount = 2 ** 31 - 1
    bcount = max_bcount
    offset = 0
    fdstno = fdst.fileno()
    fsrcno = fsrc.fileno()

    try:
      while bcount > 0:
        bcount = _sendfile(fdstno, fsrcno, offset, max_bcount)
        offset += bcount
      status = True
    except OSError as e:
      if e.errno in _sendfile_err_codes:
        # sendfile is not supported or does not support classic
        # files (only sockets)
        pass
      else:
        raise

    return status


  def copyfile(src, dst, follow_symlinks=True):
    """Copy data from src to dst.

    If follow_symlinks is not set and src is a symbolic link, a new
    symlink will be created instead of copying the file it points to.

    """
    if shutil._samefile(src, dst):
      raise shutil.SameFileError("{!r} and {!r} are the same file".format(src, dst))

    for fn in [src, dst]:
      try:
        st = os.stat(fn)
      except OSError:
        # File most likely does not exist
        pass
      else:
        # XXX What about other special files? (sockets, devices...)
        if stat.S_ISFIFO(st.st_mode):
          raise shutil.SpecialFileError("`%s` is a named pipe" % fn)

    if not follow_symlinks and os.path.islink(src):
      os.symlink(os.readlink(src), dst)
    else:
      with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        # Try to use sendfile if available for performance
        if not _copyfile_sendfile(fsrc, fdst):
          # sendfile is not available or failed, fallback to copyfileobj
          shutil.copyfileobj(fsrc, fdst)
    return dst

  if shutil.copyfile != copyfile:
    shutil._orig_copyfile = shutil.copyfile
    shutil.copyfile = copyfile
