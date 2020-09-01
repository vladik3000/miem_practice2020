import subprocess


with open("students_git", "r") as file:
    for line in file.readlines():
        gits.append(line.strip())

