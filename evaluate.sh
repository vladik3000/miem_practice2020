#!/bin/bash - 
#===============================================================================
#
#          FILE: evaluate.sh
# 
#         USAGE: ./evaluate.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: VLADISLAV KRASKOV 
#  ORGANIZATION: MIEM HSE
#       CREATED: 07/29/2020 15:50
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

#===============================================================================
#======================VARIABLES FOR THE CORRECTION=============================
#===============================================================================
# 1) language: "c" or "c++"
#
# 2) gitpath: url of student's git repository
#
# 3) command_line_arg_check_not_req: 0 or 1 (whether the command line arg tests needed)
#
# 4) files: names of the files needed to compile executable except main.c
# or main.cpp (depends on the language) separated by space
#
# 5) leakcheck: manually in makefile
#
# 6) standard of language when [-std=standard] flag is used
#
language="c"
gitpath="https://github.com/vladik3000/test.git" #test repository
command_line_arg_check_not_req=1
files='main.c aplusb.c'
std=""
#===============================================================================

echo -ne "evaluation begins...\nmake sure you set the variables correctly...\n"

if [ $language != "c" ] && [ $lanuage != "c++" ]; then
	echo "wrong language"
	exit
fi

git clone $gitpath exercise/student_task || echo "invalid git path" || exit

[ $language == "c" ] && make -C exercise LANG=1 CFILES="$files" COMMAND_LINE_ARG_NOT_REQ=1
[ $language == "c++" ] && make -C exercise LANG=0 CFILES="$files" COMMAND_LINE_ARG_NOT_REQ=1

