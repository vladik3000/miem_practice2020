import epicbox

PROFILES = {
    'gcc_compile': {
        'docker_image': 'test',
        'user': 'root',
    },
    'gcc_run': {
        'docker_image': 'test',
        'user': 'student',
        'read_only': True,
        'network_disabled': False,
    },
    'valgrind_check': {
        'docker_image': 'test',
        'user': 'student',
        'read_only': False,
        'network_disabled': True,
    },
}


epicbox.configure(profiles=PROFILES);


untrusted_code = ''
with open('main.c', 'r') as f:
    untrusted_code = f.read().encode()

FILES = [{
    'name': 'main.c',
    'content': untrusted_code
}]
with epicbox.working_directory() as wd:
    epicbox.run('gcc_compile', 'gcc main.c -o main', files=FILES,
                workdir=wd)
    res = epicbox.run('gcc_run', './main', limits={'cputime': 1, 'memory': 64},
                workdir=wd)
    with open('leakcheck.py', 'r') as mem:
        FILES += [{ 'name': 'memcheck.py', 'content': mem.read().encode()}]
    leakcheck = epicbox.run('valgrind_check', 'python3 memcheck.py', files=FILES, limits={'cputime': 5, 'memory': 521},
                workdir=wd)
    if leakcheck['stdout'].decode() != 'OK\n':
        for line in leakcheck['stdout'].decode().strip().splitlines():
            print(line)
    else:
        print('OK :)')
    #for line in leakcheck['stderr'].strip().splitlines():
    #    print(line.decode())
    #print(leakcheck['stdout'].decode())
    print(res)
