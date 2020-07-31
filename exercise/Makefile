NAME_STUDENT=student
NAME_CORRECT=correct
FLAGS=-Wall -Wextra
OBJ_STUDENT_DIR=obj_student/
OBJ_CORRECT_DIR=obj_correct/
RANDOM_UTILS=../random_testing_units/random_testing_units.c
COR_DIR=correct_task/
STU_DIR=student_task/

OK='\033[0;32m'
FAIL='\033[0;31m'
NC='\033[0m'

STDRD=$(STD)
ifeq ($(LANG), 1)
	CC=gcc
	EXT=.c
else
	CC=g++
	EXT=.cpp
endif

FILES_CORRECT=$(addprefix $(COR_DIR), $(CFILES)) 
FILES_STUDENT=$(addprefix $(STU_DIR), $(CFILES))

OBJ_CORRECT=$(addprefix $(OBJ_CORRECT_DIR), $(CFILES:$(EXT)=.o))
OBJ_STUDENT=$(addprefix $(OBJ_STUDENT_DIR), $(CFILES:$(EXT)=.o))

all: random copy_main $(NAME_STUDENT) $(NAME_CORRECT) 
	mkdir -p outputs diffs leakchecks
	echo $(LEAK)
ifeq ($(COMMAND_ARGS), 0)
	./student > outputs/student_answer
	./correct > outputs/correct_answer
	@diff student_answer correct_answer > diffs/difference && echo "TEST $(OK)OK :)$(NC)" && rm -rf diffs/difference \ 
	|| echo "$(FAIL)TEST FAILED :($(NC)"
else
	python3 arg_test.py $(LEAK) 
endif
	@rm -rf student.dSYM
$(OBJ_CORRECT): $(OBJ_CORRECT_DIR)%.o: $(COR_DIR)%$(EXT)
	$(CC) -std=$(STDRD) -c $(FLAGS) $< -o $@

$(NAME_CORRECT): $(OBJ_CORRECT) $(NAME_STUDENT)
	$(CC) $(FLAGS) $(OBJ_CORRECT) obj_utils/random_testing_units.o -o $(NAME_CORRECT)

$(OBJ_STUDENT): $(OBJ_STUDENT_DIR)%.o: $(STU_DIR)%$(EXT)
	$(CC) -std=$(STDRD) -c $(FLAGS) $< -o $@

$(NAME_STUDENT): $(OBJ_STUDENT)
	$(CC) -std=$(SRDRD) $(FLAGS) $(OBJ_STUDENT) obj_utils/random_testing_units.o -o $(NAME_STUDENT)

clean:
	/bin/rm -rf $(OBJ_STUDENT_DIR) $(OBJ_CORRECT_DIR) obj_utils

fclean: clean
	/bin/rm -rf $(NAME_CORRECT) $(NAME_STUDENT)

re: fclean all

random: ../random_testing_units/random_testing_units.h
	mkdir -p $(OBJ_CORRECT_DIR) $(OBJ_STUDENT_DIR) obj_utils
	$(CC) -std=$(STDRD) -c $(FLAGS) $(RANDOM_UTILS) -o obj_utils/random_testing_units.o

copy_main:
ifeq ($(COMMAND_ARGS), 0)
	cp correct_task/main$(EXT) student_task
endif

leakcheck:
ifeq ($(COMMAND_ARGS), 0)
	valgrind ./student
	/bin/rm -rf student.dSYM	
endif

finish: fclean
	/bin/rm -rf $(STU_DIR)* $(STU_DIR).git correct_answer student_answer difference diffs outputs leakchecks student.dSYM

.PHONY: all clean fclean re random move_main
