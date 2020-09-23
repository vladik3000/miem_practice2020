#!/usr/bin/env python3

import os, subprocess, sys

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

dirname = "./students/" + sys.argv[1] + "/"

binary_name = dirname + "task_" + sys.argv[1]

arglist_student = [binary_name]

valgrind = ["valgrind", "--leak-check=full", "--error-exitcode=1"]
student_output_file = dirname + "/outputs/output"
correct_output_file = "./correct_outputs/output"
diffarg = ["diff", student_output_file, correct_output_file]
filediff = dirname + "diffs/difference"
logname = dirname + "/result"
with open(student_output_file, "w+") as out:
    subprocess.call(arglist_student, stdout=out)
with open(filediff, "w+") as fdiff:
        subprocess.call(diffarg, stdout=fdiff)
if os.path.getsize(filediff) == 0:
    print(OKGREEN + "OK" + ENDC, end= " ")
    with open(logname, "w+") as log:
        log.write("OK\n")
    if int(sys.argv[2]) == 1:
        leakname = dirname + "/leakchecks/leaklog"
        with open(leakname, "w+") as leakfile:
            valgrind += arglist_student
            exitcode = subprocess.call(valgrind, stdout=leakfile, stderr=leakfile)
            print("leakcheck: ", end="")
            with open(logname, "a+") as log:
                if exitcode == 0:
                    print(OKGREEN + "OK :D" + ENDC)
                    log.write(" leakcheck: OK\n")
                else:
                    print(FAIL + "TEST FAILED: see the" + filediff + ENDC)
                    log.write("leakcheck: FAILED: see the" + leakname + " for information\n")
else:
    with open(logname, "a+") as log:
        log.write("TEST FAILED: see the " + filediff + " for information\n")
    print(FAIL + "FAILED: see the " + filediff + " for information" + ENDC)
