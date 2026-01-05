import json
from urllib import request, error

data = json.dumps({'texto_documento': 'Teste'}).encode('utf-8')
req = request.Request('http://localhost:8000/api/validar', data=data, headers={'Content-Type': 'application/json'})
try:
    with request.urlopen(req) as resp:
        print(resp.read().decode())
except error.HTTPError as e:
    print('HTTP', e.code)
    print(e.read().decode())
