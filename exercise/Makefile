NAME_STUDENT=student
NAME_CORRECT=correct
FLAGS=-Wall -Wextra
OBJ_STUDENT_DIR=obj_student
OBJ_CORRECT_DIR=obj_correct
RANDOM_UTILS=random_testing_units/random_testing_units.c
COR_DIR=correct_task
STU_DIR=student_task
SRC=$(CFILES)

ifeq ($(LANG), 1)
	MAIN_CORRECT=main_correct.c
	MAIN_STUDENT=main_student.c
	CC=gcc
	EXT=.c
else
	MAIN_CORRECT=main_correct.cpp
	MAIN_STUDENT=main_student.cpp
	CC=g++
	EXT=.cpp
endif

FILES_=$(CFILES)
FILES_+=$(MAIN_CORRECT)

FILES_CORRECT=$(addprefix $(COR_DIR), $(FILES_)) 
FILES_STUDENT=$(addprefix $(STU_DIR), $(FILES_))

OBJ_CORRECT=$(FILES_CORRECT:$(EXT)=.o)
OBJ_STUDENT=$(FILES_STUDENT:$(EXT)=.o)

all: random $(NAME_CORRECT) $(NAME_STUDENT) random_testing_units/random_testing_units.h

$(OBJ_CORRECT): %.o: %.$(EXT)
	$(CC) -c $(FLAGS) $< -o

$(NAME_CORRECT): $(OBJ_CORRECT)
	$(CC) $(FLAGS) $(OBJ_CORRECT) -o $(NAME_CORRECT)

$(OBJ_STUDENT): %.o: %.$(EXT) 

$(NAME_STUDENT): $(OBJ_STUDENT)
	$(CC) $(FLAGS) $(OBJ_STUDENT) -o $(NAME_STUDENT)


random:
	$(CC) -c $(FLAGS) $(RANDOM_UTILS)
