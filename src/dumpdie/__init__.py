import builtins
from .dd import dd, print_var

if not hasattr(builtins, 'dd'):
    builtins.dd = dd
else:
    print("Warning: 'dd' is already defined in the global namespace.")
