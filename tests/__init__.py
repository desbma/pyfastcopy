#!/usr/bin/env python3

import io
import os
import shutil
import tempfile
import time
import unittest
try:
  import unittest.mock as mock
except ImportError:
  import mock
try:
  monotonic = time.monotonic
except AttributeError:
  import monotonic as mntnc
  monotonic = mntnc.monotonic

import pyfastcopy


class TestFastCopy(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    fd, cls.tmpfile1 = tempfile.mkstemp()
    with os.fdopen(fd, "wb") as f:
      for _ in range(2 ** 16 * 1024 // io.DEFAULT_BUFFER_SIZE):
        f.write(os.urandom(io.DEFAULT_BUFFER_SIZE))

  @classmethod
  def tearDownClass(cls):
    os.remove(cls.tmpfile1)

  def setUp(self):
    fd, self.tmpfile2 = tempfile.mkstemp()
    os.close(fd)

  def tearDown(self):
    os.remove(self.tmpfile2)

  def test_monkeyPatch(self):
    self.assertEqual(shutil.copyfile, pyfastcopy.copyfile)
    self.assertNotEqual(shutil.copyfile, shutil._orig_copyfile)

  def test_copyfile(self):
    self.assertEqual(shutil.copyfile(self.tmpfile1, self.tmpfile2),
                     self.tmpfile2)
    with open(self.tmpfile1, "rb") as f1, open(self.tmpfile2, "rb") as f2:
      while True:
        c1 = f1.read(io.DEFAULT_BUFFER_SIZE)
        c2 = f2.read(io.DEFAULT_BUFFER_SIZE)
        self.assertEqual(c1, c2)
        if not c1:
          break

  def test_sendfileCalled(self):
    with mock.patch("pyfastcopy._sendfile", wraps=pyfastcopy._sendfile) as sendfile_mock:
      shutil.copyfile(self.tmpfile1, self.tmpfile2)
      self.assertTrue(sendfile_mock.called)

  def test_isFaster(self):
    for _ in range(2):  # do it 2 times to warm up os cache
      before = monotonic()
      shutil._orig_copyfile(self.tmpfile1, self.tmpfile2)
      after = monotonic()
      t1 = after - before
    before = monotonic()
    shutil.copyfile(self.tmpfile1, self.tmpfile2)
    after = monotonic()
    t2 = after - before
    self.assertGreater(t1, t2)


if __name__ == "__main__":
  # run tests
  unittest.main()
