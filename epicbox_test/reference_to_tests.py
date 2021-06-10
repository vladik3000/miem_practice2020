import os
from sys import argv
import epicbox
from validate import validate_work_config

PROFILES={
        'gcc': {
        'docker_image': 'test',
        'user': 'root',
        'read_only': False,
        'network_disabled': False,
    }}

def prepare_files(exercise):
    files = []
    reference_filenames = os.listdir(exercise['tests']['reference'])
    for ref in reference_filenames:
        ref_path = os.path.join(exercise['tests']['reference'], ref)
        with open(ref_path, 'rb') as f:
            files.append({'name': ref, 'content': f.read()})
    return files
            


def generate_tests(exercise, wd):
    if 'inputs_path' not in exercise['tests']:
        run = epicbox.run('gcc', './main', workdir=wd)
        with open(os.path.join(exercise['tests']['outputs_path'], 'single_test'), 'w+') as wfile:
            wfile.write(run['stdout'].decode())
    else:
        input_files = os.listdir(exercise['tests']['inputs_path'])
        for inpfile in input_files:
            with open(os.path.join(exercise['tests']['inputs_path'], inpfile), 'r+') as inp:
                input_value = inp.read()
                with open(os.path.join(exercise['tests']['outputs_path'], inpfile), 'w+') as wfile:
                    run = epicbox.run('gcc', './main', stdin=input_value, workdir=wd)
                    wfile.write(run['stdout'].decode())

def build_each(exercise, compiler, wd):
    prepared_files = prepare_files(exercise)
    compile_str = ''
    files_str = ''
    for f in prepared_files:
        files_str += ' ' + f['name']
    compile_str += compiler
    if 'flags' in exercise:
        compile_str += ' ' + exercise['flags']
    compile_str += files_str + ' -o main'
    run = epicbox.run('gcc', compile_str, files=prepared_files, workdir=wd)
    print("COMPILED")
    print(run)
    generate_tests(exercise, wd)
    
def build_tests(workdir):
    config = validate_work_config(workdir)
    if config['language'] == 'c':
        compiler = 'gcc'
    else:
        compiler = 'g++'
    with epicbox.working_directory() as wd:
        epicbox.configure(profiles=PROFILES)
        if config['type'] == 'multiple':
            for exercise in config['exercises']:
                if 'reference' in exercise['tests']:
                    build_each(exercise, compiler, wd)
        else:
            if 'reference' not in config['tests']:
                print('REFERENCE IS NOT DEFINED FOR CONFIG')
            else:
                build_each(config, compiler, wd)


build_tests(argv[1])
