import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

r = client.post("/api/v1/assistant/query", json={"prompt": "اريد خطة تعلم"})
print("ASSISTANT", r.status_code)
print(r.text)

r2 = client.get("/api/v1/files")
print("FILES", r2.status_code)
print(r2.text)

print('\n-- Routes and param names --')
for r in app.routes:
	try:
		name = getattr(r, 'path', getattr(r, 'name', str(r)))
		print('ROUTE:', getattr(r, 'path', getattr(r, 'name', 'unknown')))
		dep = getattr(r, 'dependant', None)
		if dep is not None:
			qp = [(p.name, getattr(p, 'annotation', None)) for p in getattr(dep, 'query_params', [])]
			bp = [(p.name, getattr(p, 'annotation', None)) for p in getattr(dep, 'body_params', [])]
			pp = [(p.name, getattr(p, 'annotation', None)) for p in getattr(dep, 'path_params', [])]
			print('  query_params:', qp)
			print('  body_params:', bp)
			print('  path_params:', pp)
			for d in getattr(dep, 'dependencies', []):
				func = getattr(d, 'call', None)
				print('   dependency call:', getattr(func, '__name__', str(func)), '->', getattr(func, '__annotations__', None))
		else:
			print('  no dependant')
	except Exception as e:
		print('  error inspecting route', e)
