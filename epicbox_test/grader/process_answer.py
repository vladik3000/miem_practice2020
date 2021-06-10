import json
from pathlib import Path
from logging import Logger

import os
import epicbox
import subprocess

from logs import get_logger

def gitclone(git_url, path):
    git_args = ['git', 'clone', git_url, path]
    g = subprocess.Popen(git_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return g

def check_file_presence(student_dir, work_script):
    if work_script['type'] == 'multiple':
        for exercise in work_script['exercises']:
            exercise_dir = os.path.join(student_dir, exercise['name'])
            if not os.path.isdir(exercise_dir):
                return False
            for filename in exercise['files']:
                filename_path = os.path.join(exercise_dir, filename)
                if not os.path.isfile(filename_path):
                    return False
    else:
        for filename in work_script['files']:
            filename_path = os.path.join(student_dir, filename)
            if not os.path.isfile(filename_path):
                return False
    return True


def prepare_files(student_dir, work_script):
    files = []
    for filename in work_script['files']:
        filename_path = os.path.join(student_dir, filename)
        with open(filename_path, 'rb') as f:
            files.append({'name': filename, 'content': f.read()})
    if work_script['type'] == 'function':
        linkfiles = os.listdir(work_script['linkfiles'])
        for linkfile in linkfiles:
            linkfile_path = os.path.join(work_script['linkfiles'], linkfile)
            with open(linkfile_path, 'rb') as lf:
                files.append({'name': linkfile, 'content': lf.read()})
    return files

def prepare_exercises_files(student_dir, work_script):
    exercises_files = {}
    for exercise in work_script['exercises']:
        exercises_files[exercise['name']] = prepare_files(os.path.join(student_dir, exercise['name']), exercise)
    return exercises_files

def prepare_tests(script):
    """
    the names of files in inputs_path and output_path should be equal!!!
    """
    tests = []
    if not 'inputs_path' in script:
        single_test_name = os.listdir(script['outputs_path'])[0] # add a proverka to check presence of tests!!
        single_output_test = os.path.join(script['outputs_path'], single_test_name)
        with open(single_output_test_path, 'r+') as f:
            output_value = f.read()
        return [{'test_name': 'single_test', 'input': None, 'output': output_value}]

    tests_filenames = os.listdir(script['inputs_path'])
    for test in tests_filenames:
        input_path = os.path.join(script['inputs_path'], test)
        output_path = os.path.join(script['outputs_path'], test)
        with open(input_path, 'r+') as inp:
            input_value = inp.read()
        with open (output_path, 'r+') as out:
            output_value = out.read()
        tests.append({'test_name': test, 'input': input_value, 'output': output_value})
    return tests
        

def process_answer(submission: dict):
    logger: Logger = get_logger("process_answer")
    student = submission['xqueue_body']['student_request']
    date = submission['xqueue_header']['submission_time']
    work_script = dict()
    with open('/works/' + student['work'] + '/config.json', 'r+') as conf:
        work_script = json.load(conf)
    logger.info("Student submission: %s", submission)
    logger.debug("laboratory work name: %s", student['work'])

    student_dir = '/submissions/' + student['name'] + '_' + student['work'] + '_' + str(date)
    #clone files to tmp dir
    git_url = student['git']
    # keep only last dir (DO IT AFTER EVERYTHING DONE)
    g = gitclone(git_url, student_dir)
    gout, gerr = g.communicate()
    if g.returncode != 0:
        subprocess.call(['rm', '-rf', student_dir])
        return {'status': 'git clone error', 'log': gerr.decode()}
    if not check_file_presence(student_dir, work_script):
        subprocess.call(['rm', '-rf', student_dir])
        return {'error': 'required files are not present'}
    if work_script['type'] == 'multiple':
        files = prepare_exercises_files(student_dir, work_script)
    else:
        files = prepare_files(student_dir, work_script)
    grades = []
    if work_script['language'] == 'c':
        compiler = 'gcc'
    else:
        compiler = 'g++'
    if work_script['type'] == 'multiple':
        for exercise in work_script['exercises']:
            tests = prepare_tests(exercise['tests'])
            if not ('limits' in exercise):
                limits = work_script['default_limits']
            else:
                limits = exercise['limits']
            grade = grade_epicbox(compiler, files[exercise['name']], tests, flags, limits, work_script['stop_if_fails'], work_script['memcheck'])
            grades.append({'name': exercise['name'], 'grade': grade})
            logger.info('task: %s\nGrade: %s', exercise['name'], grade)
            
    else:
        tests = prepare_tests(work_script['tests'])
        limits = work_script['default_limits']
        flags = ''
        if 'flags' in work_script:
            flags = work_script['flags']
        grade = grade_epicbox(compiler, files, tests, flags, limits, work_script['stop_if_fails'], work_script['memcheck'])
        return grade
    logger.info("task: %s:\nGrade: %s", work_script['name'], grade)
    print('GRADES')
    print(grades)
    return grades

def compile_code(compiler, flags, prepared_files, wd):
    filestr = ''
    for filedict in prepared_files:
        filestr += ' ' + filedict['name']
    compile_str = compiler + ' ' + flags + ' ' + filestr + ' -o main'
    print("COMPILE_STR: " + compile_str)
    comp = epicbox.run('test_code', compile_str, files=prepared_files, workdir=wd)
    print("COMPILED SUCCESSFULLY")
    return comp

def check_valgrind(inp, dlimits, wd):
    valgrind_run = 'valgrind --leak-check=full --error-exitcode=1 ./main'
    check = epicbox.run('test_code', valgrind_run, limits=dlimits, workdir=wd)
    return check

def grade_epicbox(
    compiler: str,
    prepared_files: dict,
    tests: list,
    flags: str, 
    docker_limits: dict,
    stop_if_fails: bool,
    memcheck: bool,
) -> list:
    """
    Running grading script in a separate Docker container.
    https://github.com/StepicOrg/epicbox

    :param submission: Student submission received from message broker.
    :param script_name: Name of the grading script.
    :param prepared_files: List of files and their paths.
    :param docker_profile: Epicbox profile.
    :param docker_limits: Docker container limits.
    :return: Results of grading.
    """
    logger: Logger = get_logger("process_answer")
    PROFILES = {
        'test_code': {
            'docker_image': 'test',
            'user': 'root',
            'read_only': False,
            'network_disabled': True,
    }}
    epicbox.configure(profiles=PROFILES)
    with epicbox.working_directory() as wd:

        comp = compile_code(compiler, flags, prepared_files, wd)
        if comp['exit_code'] != 0:
            return [{'status': 'CE', 'log': comp['stderr'].decode()}]
        test_results = []
        for test in tests:
            test_case = epicbox.run('test_code', './main', stdin=test['input'], limits=docker_limits, workdir=wd)
            test_case['stdout'] = test_case['stdout'].decode()
            test_case['stderr'] = test_case['stderr'].decode()
            if test_case['timeout']:
                result = {'status': 'TL', 'test_name': test['test_name'], 'input': test['input'], \
                                            'correct_output': test['output'], 'answer': test_case}
            elif test_case['oom_killed']:
                result = {'status': 'ML', 'test_name': test['test_name'], 'input': test['input'], \
                                            'correct_output': test['output'], 'answer': test_case}
            elif test_case['stdout'] != test['output']:
                result = {'status': 'WA', 'test_name': test['test_name'], 'input': test['input'], \
                                            'correct_output': test['output'], 'answer': test_case}
            else:
                result = {'status': 'OK', 'test_name': test['test_name'], 'input': test['input'], \
                                            'correct_output': test['output'], 'answer': test_case}
            if stop_if_fails == True and result['status'] != 'OK':
                test_results.append(result)
                break
            if memcheck == True and result['status'] == 'OK':
                memory_check = check_valgrind(test_input, limits, wd)
                if memory_check['exitcode'] != 0:
                    result['memcheck'] = {'memcheck': 'ERROR', 'log': memory_check['stderr'].decode()}
                else:
                    result['memcheck'] = {'memcheck': 'OK'}
            test_results.append(result)
    logger.debug("Result: %s", result)

    return test_results
