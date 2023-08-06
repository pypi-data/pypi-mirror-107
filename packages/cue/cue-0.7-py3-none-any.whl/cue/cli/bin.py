import sys, subprocess

def cue():
    """package the command for setup.py"""
    shell_command = ['python', '-m', 'cue.cli'] + sys.argv[1:]
    subprocess.run(shell_command)
