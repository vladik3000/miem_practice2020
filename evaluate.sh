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


OK='\033[0;32m'
FAIL='\033[0;31m'
NC='\033[0m'



#===============================================================================
#======================VARIABLES FOR THE CORRECTION=============================
#===============================================================================
# 1) language:	"c" or "c++"
#
# 2) gitpath:	url of student's git repository (first argument of this script)
#
# 3) checktype: three ways to evaluate: 1) no input 2) command line argument input 3) standart input
#
# 4) files:		names of the files needed to compile the executable
#
# 5) std:		standard of language when [-std=standard] flag is used
#
# 5) leakcheck: 0 or 1 whether you want to check memory leaks
#
# 6) dir:		name of the directory (second argument of the script)
language="c"
gitpath=$1 #test repository
checktype=2
files='main.c'
std="c99"
leakcheck=1
dir=$2
#===============================================================================

echo -ne "evaluation begins...for $2:\n"

if [ $language != "c" ] && [ $lanuage != "c++" ]; then
	echo "wrong language"
	exit
fi

mkdir -p ./exercise/students/ || exit 1
git clone $gitpath exercise/students/$2 &> gitlog

if [ $? -ne 0 ]; then
	echo -e "${FAIL}invalid git path: see gitlog${NC}"
	exit 1
fi
[ $language == "c" ] && make -s -C exercise LANG=1 CFILES="$files" CHECKTYPE=$checktype STD="$std" LEAK=$leakcheck DIR=$dir
[ $language == "c++" ] && make -s -C exercise LANG=0 CFILES="$files" COMMAND_ARGS=$checktype STD="$std" LEAK=$leakcheck DIR=$dir

