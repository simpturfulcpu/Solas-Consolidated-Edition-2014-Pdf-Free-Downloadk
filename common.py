# Copyright (C) 2016 Ben Smith
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#
import fnmatch
import os
import hashlib
import re
import subprocess

TESTER_DEBUG = 'out/tester'
TESTER_RELEASE = 'out/tester-release'


class Error(Exception):
  pass


def Run(exe, *args):
  cmd = [exe] + list(args)
  # print('Running:', ' '.join(cmd))
  basename = os.path.basename(exe)
  try:
    PIPE = subprocess.PIPE
    process = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
      raise Error('Error running "%s":\n%s' % (basename, stderr.decode('ascii')))
  except OSError as e:
    raise Error('Error running "%s": %s' % (basename, str(e)))


def RunTester(rom, frames=None, out_ppm=None, animate=False,
              controller_input=None, debug_exe=False, timeout_sec=None):
  exe = TESTER_DEBUG if debug_exe else TESTER_RELEASE
  cmd = []
  if frames:
    cmd.extend(['-f', str(frames)])
  if controller_input:
    cmd.extend(['-i', controller_input])
  if out_ppm:
    cmd.extend(['-o', out_ppm])
  if animate:
    cmd.append('-a')
  if timeout_sec:
    cmd.extend(['-t', str(timeout_sec)])
  cmd.append(rom)
  Run(exe, *cmd)


def HashFile(filename):
  m = hashlib.sha1()
  m.update(open(filename, 'rb').read())
  return m.hexdigest()


def MakePatternRE(patterns):
  if patterns:
    pattern_re = '|'.join(fnmatch.translate('*%s*' % p) for p in patterns)
  else:
    pattern_re = '.*'
  return re.compile(pattern_re)
