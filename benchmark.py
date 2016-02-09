#!/usr/bin/env python3

""" Generate performance graphs. """

import collections
import contextlib
import os
import platform
import subprocess
import tempfile
import timeit


FILE_SIZES_MB = tuple(2 ** x for x in range(12))


def generate_file(parent_dir, size_mb):
  """ Generate a file, write random data to it, and return its filepath. """
  fd, filepath = tempfile.mkstemp(dir=parent_dir)
  os.close(fd)
  print("Generating %u MB file to '%s'..." % (size_mb, filepath))
  cmd = ("dd", "if=/dev/frandom", "of=%s" % (filepath), "bs=1M", "count=%u" % (size_mb))
  subprocess.check_call(cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
  return filepath


def read_file(filepath):
  """ Read a file to fill OS filesystem cache. """
  cmd = ("dd", "if=%s" % (filepath), "of=/dev/null", "bs=1M")
  subprocess.check_call(cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)


if __name__ == "__main__":

  with tempfile.TemporaryDirectory() as tmp_dir:
    # measure
    data = collections.OrderedDict()
    for file_size_mb in FILE_SIZES_MB:
      data_point = []
      filepath_src = generate_file(tmp_dir, file_size_mb)
      read_file(filepath_src)  # warm up filesystem cache
      filepath_dst = "%s.dst" % (filepath_src)
      for use_fast_copy in (False, True):
        print("Measuring with%s pyfastcopy..." % ("" if use_fast_copy else "out"))
        v = timeit.repeat(setup="import shutil; import pyfastcopy; p1 = %s; p2 = %s" % (repr(filepath_src),
                                                                                        repr(filepath_dst)),
                          stmt="shutil.%s(p1, p2)" % ("copyfile" if use_fast_copy else "_orig_copyfile"),
                          number=10 if file_size_mb >= 64 else 100,
                          repeat=5)
        v = min(v)
        data_point.append(str(v / (10 if file_size_mb >= 64 else 100)))
        os.remove(filepath_dst)
      os.remove(filepath_src)
      data[file_size_mb] = tuple(data_point)

    # write data files
    data_filepaths = []
    data_fds = []
    for graph in range(3):
      fd, data_filepath = tempfile.mkstemp(suffix=".csv", dir=tmp_dir)
      data_filepaths.append(data_filepath)
      data_fds.append(fd)
    with contextlib.ExitStack() as cm:
      files = [cm.enter_context(os.fdopen(fd, "wt")) for fd in data_fds]
      for file_size_mb, data_point in data.items():
        f = files[0 if file_size_mb < 64 else 1]
        line = "%u,%s\n" % (file_size_mb, ",".join(data_point))
        f.write(line)
        files[-1].write(line)

    # plot
    for graph, data_filepath in enumerate(data_filepaths[:2], 1):
      gnuplot_code = ["set terminal png size 1024,600 font 'M+ 1c bold,12'",
                      "set title \"Time to copy file using shutil.copyfile: standard Python vs pyfastcopy\\n"
                      "(using tmpfs, on %s %s %s)\"" % (platform.system(),
                                                        platform.release(),
                                                        platform.processor()),
                      "set output '%u.png'" % (graph),
                      "set key left samplen 3 spacing 1.75",
                      "set xlabel 'File size (MB)'",
                      "set xtics rotate out",
                      "set ylabel 'Time to copy (ms)'",
                      "set format y '%.0f'",
                      "set style data histogram",
                      "set style histogram clustered",
                      "set style fill solid",
                      "set boxwidth 0.95 relative",
                      "set datafile separator ','",
                      "plot '%s' using ($2*1000):xtic(1) title 'standard', "
                      "'%s' using ($3*1000):xtic(1) title 'pyfastcopy'" % (data_filepath, data_filepath)]
      gnuplot_code = ";\n".join(gnuplot_code) + ";"
      subprocess.check_output(("gnuplot",),
                              input=gnuplot_code,
                              stderr=None,
                              universal_newlines=True)
    gnuplot_code = ["set terminal png size 1024,600 font 'M+ 1c bold,12'",
                    "set title \"shutil.copyfile performance gain of pyfastcopy vs stock Python\\n"
                    "(using tmpfs, on %s %s %s)\"" % (platform.system(),
                                                      platform.release(),
                                                      platform.processor()),
                    "set output '3.png'",
                    "set xlabel 'File size (MB)'",
                    "set xtics rotate out",
                    "set ylabel 'Performance gain (%)'",
                    "set yrange[20:50]",
                    "set format y '%.0f'",
                    "set mytics 5",
                    "set datafile separator ','",
                    "plot '%s' using (100-100*$3/$2):xtic(1) with lines title '' lw 2" % (data_filepaths[2])]
    gnuplot_code = ";\n".join(gnuplot_code) + ";"
    subprocess.check_output(("gnuplot",),
                            input=gnuplot_code,
                            stderr=None,
                            universal_newlines=True)
