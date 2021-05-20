import subprocess

args = [ 'valgrind', '--leak-check=full', '--error-exitcode=1', './main' ]
child = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output = child.communicate()[0]
if child.returncode == 0:
    print("OK")
else:
    print(output.decode())
