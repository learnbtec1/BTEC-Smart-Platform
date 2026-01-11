import os
root = os.path.join(os.path.dirname(__file__), 'app')
for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        if fn.endswith('.py'):
            path = os.path.join(dirpath, fn)
            with open(path, 'r', encoding='utf-8') as f:
                s = f.read()
            if 'query' in s:
                for i,l in enumerate(s.splitlines(),1):
                    if 'query' in l:
                        print(path, i, l.strip())
