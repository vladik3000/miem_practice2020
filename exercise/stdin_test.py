#!/usr/bin/env python3

import os, subprocess, sys

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

dirname = "./" + sys.argv[1] + "/"

binary_name = dirname + "/task_" + sys.argv[1]

arglist_student = [binary_name]

valgrind = ["valgrind", "--leak-check=full", "--error-exitcode=1"]

for subdir, dir, files in os.walk("inputs"):
    for file in files:
        with open("inputs/" + file, "r") as stdinput:
            #args = [line.rstrip() for line in argfile]
            #arglist_student += args
            student_output_file = dirname + file + "_output"
            correct_output_file = "./correct_outputs/" + file
            diffarg = ["diff", student_output_file, correct_output_file]
            filediff = dirname + "/diffs/" + file + "_diff"
            with open(student_output_file, "w+") as student_output:
                subprocess.call(arglist_student, stdout=student_output, stdin=stdinput)
            with open(filediff, "w+") as fdiff:
                subprocess.call(diffarg, stdout=fdiff)
            logname = dirname + "result"
            if os.path.getsize(filediff) == 0:
                print(OKGREEN + "OK" + ENDC, end= " ")
                with open(logname, "a+") as log:
                    log.write(file + ": OK")
                if int(sys.argv[2]) == 1:
                    valgrind += arglist_student
                    leakname = dirname + "/leakchecks/" + file
                    with open(leakname, "w+") as leakfile:
                        exitcode = subprocess.call(valgrind, stdout=leakfile, stderr=leakfile)
                    print("leakcheck: ", end="")
                    with open(logname, "a+") as log:
                        if exitcode == 0:
                            print(OKGREEN + "OK" + ENDC, end= " ")
                            log.write("leakcheck: OK")
                        else:
                            print(FAIL + "FAILED" + ENDC, end="")
                            log.write("leakcheck: FAILED: see the" + leakname + "for information")
            else:
                with open(logfile, "a+") as log:
                    log.write(file + ": FAILED: see the " + filediff + " for information")
                print(FAIL + "FAILED: see the " + filediff + "for information" + ENDC, end="")
            print('\n')
