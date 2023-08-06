import os
import ctypes
import sys
import subprocess


def add_context():
    """
    Add current file's directory into system path.
    """
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def get_admin():
    """run script with administrator privilege
    """
    if ctypes.windll.shell32.IsUserAnAdmin():
        pass
    else:
        # rerun the script with admin privilege
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def exec_ps(ps_path: str, show_result=False, show_error=True):
    """Execute PowerShell script line by line

    Args:
        ps_path (str): path to PowerShell script
        show_result (bool, optional): whether to show the result or not. Defaults to False.
        show_error (bool, optional): whether to show the error or not. Defaults to True.
    """
    stdout = sys.stdout if show_result == True else None
    stderr = sys.stdout if show_error == True else None
    shell = subprocess.Popen(
        ["powershell.exe"],
        stdin=subprocess.PIPE,
        stdout=stdout,
        stderr=stderr,
        shell=True,
        universal_newlines=True
    )
    with open(ps_path, 'r') as f:
        for i in f.readlines():
            shell.stdin.write(i)
            shell.stdin.flush()
