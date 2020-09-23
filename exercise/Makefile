FLAGS=-Wall -Wextra
STU_DIR=$(DIR)
NAME_STUDENT=$(DIR)/task_$(STU_DIR)
OBJ_STUDENT_DIR=$(DIR)/obj_student/

NOINPUT=1
ARG=2
STDINP=3

DIFF_FAIL=0

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

all: makedirs $(NAME_STUDENT) 
ifeq ($(CHECKTYPE), $(NOINPUT))
	@python3 noinput_test.py $(DIR) $(LEAK)
endif
ifeq ($(CHECKTYPE), $(ARG))
	@python3 arg_test.py $(DIR) $(LEAK)
endif
ifeq ($(CHECKTYPE), $(STDINP))
	@python3 stdin_test.py $(DIR) $(LEAK)
endif

$(OBJ_STUDENT): $(OBJ_STUDENT_DIR)%.o: $(STU_DIR)/%$(EXT)
	@$(CC) -std=$(STDRD) -c $(FLAGS) $< -o $@ > $(STU_DIR)/compilation 2>&1 || echo "$(FAIL)compilation failed T_T :see the compilation file for info$(NC)" && exit 1

$(NAME_STUDENT): $(OBJ_STUDENT)
	@$(CC) -std=$(SRDRD) $(FLAGS) $(OBJ_STUDENT) -o $(NAME_STUDENT) > $(STU_DIR)/compilation 2>&1 || echo "$(FAIL)compilation failed T_T :see the compilation file for info$(NC)" && exit 1

clean:
	@/bin/rm -rf $(OBJ_STUDENT_DIR)  obj_utils

fclean: clean
	@/bin/rm -rf $(NAME_STUDENT)

re: fclean finish all

makedirs:
	@mkdir -p $(STU_DIR)/obj_student $(STU_DIR)/diffs $(STU_DIR)/leakchecks $(STU_DIR)/outputs 

leakcheck:
ifeq ($(COMMAND_ARGS), 0)
	valgrind ./student
	/bin/rm -rf student.dSYM	
endif

finish: fclean
	@/bin/rm -rf $(STU_DIR)* $(STU_DIR).git correct_answer student_answer difference diffs outputs leakchecks student.dSYM

.PHONY: all clean fclean re random move_main
