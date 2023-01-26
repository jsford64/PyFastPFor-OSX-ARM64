#!/usr/bin/env python3
import os
import sys
import re
import subprocess
import tempfile

""" Fake compiler for compiling PyFastPFor on MacOS and/or ARM.

    On MacOS:
        SetupTools does not allow different flags for C and C++ source code,
        and clang does not accept all flags at the same time like other
        compilers apparently do.

        This 'compiler' intercepts the command line, edits the options and
        calls the compiler used to compile the python interpreter with the
        right options enabled for the source file being compiled (.c, .cc, or .cpp)

"""

def check_sse2neon_install ():
    # If ./sse2neon/sse2neon.h is not present, clone it
    if not os.path.isfile('./sse2neon/sse2neon.h'):
        out = subprocess.run([ 'git', 'clone', 'https://github.com/DLTcollab/sse2neon.git'], capture_output=True)
        if out.returncode == 0:
            print('git clone successful!')
        else:
            print('git clone unsuccessful!')
            exit(1)

def is_arm64_arch ():
    # Compile a fake program and dump the #defines to see if we are running on
    # Arm 64 architecture.
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')

        out = subprocess.run([ CC, '-dM', '-E', '-' ], stdin=f, capture_output=True)

        return out.returncode == 0 and b'__aarch64__' in out.stdout


if __name__ == '__main__':
    # get the actual C/C++ compiler name used to compile this python interpreter
    # usually clang on MacOS.
    CC = re.search(r'\[(\w+)',sys.version).group(1).lower()
    # Update the command line with the actual compiler name
    cmdline = [CC] + sys.argv[1:]

    # Are we running on ARM 64 architecture?
    if is_arm64_arch():
        # Yes, make sure sse2neon/sse2neon.h is installed and add it to the command line
        check_sse2neon_install()
        cmdline += ['-I./sse2neon/sse2neon.h']

    if sys.platform == 'darwin':
        # Running MacOS

        # Find the name of the source file to be compiled following the '-c' option
        sourceFile = cmdline[cmdline.index('-c')+1]
        # Check the source type to see if it is a C file
        if sourceFile.endswith('.c'):
            # C file, remove C++ compiler options from command line
            cmdline.remove('-stdlib=libc++')
            cmdline.remove('-std=c++11')

    # Execute the compiler command
    out = subprocess.run(cmdline, capture_output=True)

    # echo stdout and stderr
    if len(out.stdout):
        print(out.stdout.decode('utf-8'))
    if len(out.stderr):
        print(out.stderr.decode('utf-8'), file=sys.stderr)

    exit(out.returncode)
