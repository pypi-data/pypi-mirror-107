import subprocess
import sys

def runCommand(command, outputToScreen=False):
    popen = subprocess.Popen(command, 
        shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        universal_newlines=True
    )

    output = []
    for line in iter(popen.stdout.readline, ""):
        output.append(line)
        if outputToScreen:
            sys.stdout.write(line)
            sys.stdout.flush()
    popen.stdout.close()
    return_code = popen.wait()
    return (return_code, ''.join(output))
