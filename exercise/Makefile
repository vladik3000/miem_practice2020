NAME_STUDENT=student
NAME_CORRECT=correct
FLAGS=-Wall -Wextra
OBJ_STUDENT_DIR=obj_student
OBJ_CORRECT_DIR=obj_correct
RANDOM_UTILS=../random_testing_units/random_testing_units.c
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

OBJ_CORRECT=$(addprefix $(OBJ_CORRECT_DIR), $(FILES_CORRECT:$(EXT)=.o))
OBJ_STUDENT=$(addprefix $(OBJ_STUDENT_DIR), $(FILES_STUDENT:$(EXT)=.o))

all: random $(NAME_CORRECT) $(NAME_STUDENT)

$(OBJ_CORRECT): $(OBJ_CORRECT_DIR)%.o: $(COR_DIR)%.$(EXT)
	mkdir -p $(OBJ_CORRECT_DIR)
	$(CC) -c $(FLAGS) $< -o $@

$(NAME_CORRECT): $(OBJ_CORRECT)
	$(CC) $(FLAGS) $(OBJ_CORRECT) -o $(NAME_CORRECT)

$(OBJ_STUDENT): $(OBJ_STUDENT_DIR)%.o: $(STU_DIR)%.$(EXT)
	mkdir -p $(OBJ_STUDENT_DIR)
	$(CC) -c $(FLAGS) $< -o $@

$(NAME_STUDENT): $(OBJ_STUDENT)
	$(CC) $(FLAGS) $(OBJ_STUDENT) -o $(NAME_STUDENT)

clean:
	/bin/rm -rf $(OBJ_STUDENT_DIR) $(OBJ_CORRECT_DIR)

fclean: clean
	/bin/rm -rf $(NAME_CORRECT) $(NAME_STUDENT)

re: fclean all

random: ../random_testing_units/random_testing_units.h
	$(CC) -c $(FLAGS) $(RANDOM_UTILS)

.PHONY: all clean fclean re random
