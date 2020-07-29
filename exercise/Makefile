NAME_S=student
NAME_C=correct
FLAGS=-Wall -Wextra
OBJ_ST=obj_student
OBJ_COR=obj_correct
RANDOM_UTILS=random_testing_units/random_testing_units.c

SRC=$(CFILES)

ifeq ($(LANG), 1)
	MAIN_CORRECT=main_correct.c
	MAIN_STUDENT=main_student.c
	COMPILER=gcc
else
	MAIN_CORRECT=main_correct.cc
	MAIN_STUDENT=main_student.cc
	COMPILER=g++
endif

all: random
	


random:
	$(COMPILER) -c $(FLAGS) $(RANDOM_UTILS)





