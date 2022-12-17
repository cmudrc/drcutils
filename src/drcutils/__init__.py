def is_colab() -> bool:
    import sys
    return 'google.colab' in sys.modules

def is_notebook() -> bool:
    if is_colab():
        return True
    else:
        try:
            shell = get_ipython().__class__.__name__
            print(shell)
            if shell == 'ZMQInteractiveShell':
                return True   # Jupyter notebook or qtconsole
            elif shell == 'TerminalInteractiveShell':
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False      # Probably standard Python interpreter
