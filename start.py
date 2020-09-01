#!/usr/bin/env python3
import subprocess

gits = list()
name = ""

def getname(gitpath):
    parts = gitpath.split("/")
    for i in range(len(parts)):
        if parts[i] == "github.com" or parts[i] == "gitlab.com":
            return parts[i + 1]

with open("students_git", "r") as file:
    for line in file.readlines():
        gits.append(line.strip())


for git in gits:
    name = getname(git)
    if name == None:
        print("invalid git path:", git)
        exit()
    subprocess.call(["./evaluate.sh", git, name])
