import subprocess

def subprocess_cmd(command):
    print ('executing:')
    print (command)

    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print (proc_stdout.decode("utf-8"))

subprocess_cmd('apt-get install -y binutils libproj-dev gdal-bin')
subprocess_cmd('GUNICORN_CMD_ARGS="--bind=0.0.0.0 --timeout 600" gunicorn exodus.wsgi')
