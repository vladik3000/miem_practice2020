#!/usr/bin/env python3

import os, subprocess, sys

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

arglist_student = ["./task_"]

valgrind = ["valgrind", "--leak-check=full", "--error-exitcode=1"]


for subdir, dir, files in os.walk("command_line_args"):
    for file in files:
        with open("command_line_args/" + file, "r") as argfile:
            args = [line.rstrip() for line in argfile]
            arglist_student += args
            arglist_correct += args
            student_output_file = "outputs/" + file + "_student_output"
            correct_output_file = "outputs/" + file + "_correct_output"
            diffarg = ["diff", student_output_file, correct_output_file]
            filediff = "diffs/" + file + "_diff"
            with open(student_output_file, "w+") as student_output:
                subprocess.call(arglist_student, stdout=student_output)
            with open(correct_output_file, "w+") as correct_output:
                subprocess.call(arglist_correct, stdout=correct_output)
            with open(filediff, "w+") as fdiff:
                subprocess.call(diffarg, stdout=fdiff)
            print(file + "test: ", end= '')
            if os.path.getsize(filediff) == 0:
                print(OKGREEN + "OK" + ENDC, end= " ")
                rm = ["rm", filediff]
                subprocess.call(rm)
                if len(sys.argv) > 1:
                    valgrind += arglist_student
                    with open("leakchecks/" + file, "w+") as leakfile:
                        exitcode = subprocess.call(valgrind, stdout=leakfile, stderr=leakfile)
                    print("leakcheck: ", end="")
                    if exitcode == 0:
                        print(OKGREEN + "OK" + ENDC, end= " ")
                    else:
                        print(FAIL + "FAILED" + ENDC, end="")
            else:
                print(FAIL + "FAILED: see the " + filediff + "for information" + ENDC, end="")
            print('\n')
