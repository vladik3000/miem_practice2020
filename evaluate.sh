#!/bin/bash - 
#===============================================================================
#
#          FILE: asd.sh
# 
#         USAGE: ./asd.sh 
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
# 3) command_line_arg_check: 0 or 1 (whether the command line arg tests needed)
#
# 4) files: names of the files needed to compile executable except main.c
# or main.cpp (depends on the language) separated by space
#
# 5) leakcheck: 0 or 1 (memory leak check)
#
language="c"
gitpath="asd"
command_line_arg_check=1
leakcheck=1
files="average_between_negatives.c"
#===============================================================================

echo "evaluation begins...\nmake sure you set the variables correctly..."

git clone $gitpath exercise/student || echo "invalid git path" || exit

if [ $language -ne "c" && $lanuage -ne "c++" ]; then
	echo "wrong language"
	exit
fi

[ language -eq "c" ] && make -c exercise LANG=1 CFILES=files
[ language -eq "c++" ] && make -c exercise LANG=0 CFILES=files



