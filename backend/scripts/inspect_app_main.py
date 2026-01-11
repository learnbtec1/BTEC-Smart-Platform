import sys, os, inspect
repo_backend = os.getcwd()
if repo_backend not in sys.path:
    sys.path.insert(0, repo_backend)
import app.main as m
print('app.main file:', m.__file__)
print('--- source snippet ---')
print(inspect.getsource(m)[:800])
