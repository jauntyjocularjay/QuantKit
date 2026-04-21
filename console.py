import subprocess
import os

# To import use from the same folder:
# import console 
#
# To import use from the parent folder:
# from PyTils import console 

def clear():
    subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)

    # lines added in case of terminal overhang on some terminals.
    print('\n\n')

