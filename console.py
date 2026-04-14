import subprocess
import os

def clear():
    subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)
    print("\n\n") # lines added in case of terminal overhang on some terminals.