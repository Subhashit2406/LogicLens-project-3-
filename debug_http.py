import os
os.chdir(r'c:\Users\subha\OneDrive\Desktop\Prj 3(LogicLens)')
from app import app
c = app.test_client()
r = c.get('/api/graph')
print('GRAPH', r.status_code)
print('GRAPH JSON', r.get_json())
r2 = c.get('/api/whatif?function=test')
print('WHATIF', r2.status_code)
print('WHATIF HEADERS', dict(r2.headers))
print('WHATIF DATA', r2.get_data()[:400])
