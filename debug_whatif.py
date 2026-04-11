import os
os.chdir(r'c:\Users\subha\OneDrive\Desktop\Prj 3(LogicLens)')
from app import app
client = app.test_client()
response = client.get('/api/whatif?function=test', buffered=False)
print('STATUS', response.status_code)
print('HEADERS', dict(response.headers))
count = 0
for chunk in response.response:
    print('CHUNK', repr(chunk)[:400])
    count += 1
    if count >= 5:
        break
print('DONE ITERATION', count)
