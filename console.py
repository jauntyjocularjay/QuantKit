import subprocess
import os

def clear():
    subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)