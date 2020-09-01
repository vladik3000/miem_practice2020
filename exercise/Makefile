FLAGS=-Wall -Wextra
OBJ_STUDENT_DIR=obj_student/
RANDOM_UTILS=../random_testing_units/random_testing_units.c
STU_DIR=$(DIR)
NAME_STUDENT=task_$(STU_DIR)

OK='\033[0;32m'
FAIL='\033[0;31m'
NC='\033[0m'

STDRD=$(STD)
ifeq ($(LANG), 1)
	CC=clang
	EXT=.c
else
	CC=g++
	EXT=.cpp
endif

FILES_STUDENT=$(addprefix $(STU_DIR), $(CFILES))

OBJ_STUDENT=$(addprefix $(OBJ_STUDENT_DIR), $(CFILES:$(EXT)=.o))

all: random copy_main $(NAME_STUDENT) 
	mkdir -p logs
	mkdir -p logs/outputs logs/diffs logs/leakchecks logs/results
ifeq ($(COMMAND_ARGS), 0)
	./task > logs/outputs/$(NAME_STUDENT)
	@diff logs/outputs/$(NAME_STUDENT) correct_outputs/output > logs/diffs/difference_$(NAME_STUDENT) &&
	echo "TEST $(OK)OK :)$(NC)" && rm -rf logs/diffs/difference_$(NAME_STUDENT) && echo "OK" > logs/results/result_$(NAME_STUDENT) \ 
	|| echo "$(FAIL)TEST FAILED :($(NC)" && echo "TEST FAILED" > logs/results/result_$(NAME_STUDENT)
else
	python3 arg_test.py $(LEAK) 
endif
	@rm -rf student.dSYM

$(OBJ_STUDENT): $(OBJ_STUDENT_DIR)%.o: $(STU_DIR)%$(EXT)
	$(CC) -std=$(STDRD) -c $(FLAGS) $< -o $@

$(NAME_STUDENT): $(OBJ_STUDENT)
	$(CC) -std=$(SRDRD) $(FLAGS) $(OBJ_STUDENT) obj_utils/random_testing_units.o -o $(NAME_STUDENT)

clean:
	/bin/rm -rf $(OBJ_STUDENT_DIR)  obj_utils

fclean: clean
	/bin/rm -rf $(NAME_STUDENT)

re: fclean finish all

random: ../random_testing_units/random_testing_units.h
	mkdir -p $(OBJ_STUDENT_DIR) obj_utils
	$(CC) -std=$(STDRD) -c $(FLAGS) $(RANDOM_UTILS) -o obj_utils/random_testing_units.o

copy_main:
ifeq ($(COMMAND_ARGS), 0)
	cp main$(EXT) $(STU_DIR)
endif

leakcheck:
ifeq ($(COMMAND_ARGS), 0)
	valgrind ./student
	/bin/rm -rf student.dSYM	
endif

finish: fclean
	/bin/rm -rf $(STU_DIR)* $(STU_DIR).git correct_answer student_answer difference diffs outputs leakchecks student.dSYM

.PHONY: all clean fclean re random move_main
