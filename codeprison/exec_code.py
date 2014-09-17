import shutil
import subprocess
import os
import random
import instructor
import resource
import threading
import signal

# Constants
SANDBOX_DIR = "/tmp/sandbox/"

default_limits = {
    "REAL_TIME": 5,
    "NPROC": 50,
    "VMEM": 0,
}

overridden_limits = {}

# Returns a dict containing a field 'stdout'
def exec_code(language, code):
    result = {
        'stdout': ""
    }

    setup_env()

    id = create_sandbox()

    instructions = instructor.getInstructions(language, code)

    for instr in instructions:
        action = instr['action']

        if (action == 'createFile'):
            filename = instr['name']
            filebody = instr['body']

            sandbox_file(id, filename, filebody)

        if (action == 'runCommand'):
            command = instr['command']
            args    = instr['args']

            r = sandbox_command(id, command, args)

            # append stdout of command to final result
            result['stdout'] += r['stdout']

    destroy_sandbox(id)

    return result


def setup_env():
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)

def create_sandbox():
    id = get_random_int()
    os.makedirs(SANDBOX_DIR + str(id))
    return id

def sandbox_file(id, filename, filebody):
    fo = open(SANDBOX_DIR + str(id) + "/" + filename, "wb")
    fo.write(filebody)
    fo.close()

def sandbox_command(id, command, args):
    
    # Excecute command
    proc = subprocess.Popen(
        [command] + args,
        preexec_fn = enforce_limits,
        cwd        = SANDBOX_DIR + str(id),
        stdin      = subprocess.PIPE,
        stdout     = subprocess.PIPE,
        stderr     = subprocess.STDOUT,
        ) 

    # Start timer to kill thread to prevent it running for too long
    timeout = get_limit_value('REAL_TIME')
    timer = threading.Timer(timeout, kill_proc, [proc])
    timer.start()

    (stdout, stderr) = proc.communicate()

    timer.cancel()

    result = {
        'stdout': stdout,
    }

    return result

def destroy_sandbox(id):
    shutil.rmtree(SANDBOX_DIR + str(id))

# Override a default process limit
def override_limit(limit, value):
    overridden_limits[limit] = value

def restore_default_limits():
    overridden_limits.clear()

def get_limit_value(limit):
    if limit in overridden_limits:
        return overridden_limits[limit]
    else:
        return default_limits[limit]

def enforce_limits():
    os.setsid()

    nproc_limit = get_limit_value("NPROC")
    resource.setrlimit(resource.RLIMIT_NPROC, (nproc_limit, nproc_limit))

    vmem_limit = get_limit_value("VMEM")
    if (vmem_limit != 0):
        resource.setrlimit(resource.RLIMIT_AS, (vmem_limit, vmem_limit))


def kill_proc(proc):
    os.killpg(proc.pid, signal.SIGTERM)

def get_random_int():
    return random.randint(10000, 99999)