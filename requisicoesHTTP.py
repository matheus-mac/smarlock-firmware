import requests
import json

payload = {'numeroSerial': 1, 'rfidUUID': '221,36,133,137,245'}
r = requests.get('http://52.54.145.159:81/api/Fechaduras/VerificaCadastroUsuario/', params= payload)
parsed_json = json.loads(r.content)
print(parsed_json['Nome'])


payloadRegistraAcesso = {'numeroSerial': 1, 'usuarioId': 1}
requestRegistraAcesso = requests.post('http://52.54.145.159:81/api/Acessos/RegistraAcesso/', params= payloadRegistraAcesso)
parsed_json = json.loads(requestRegistraAcesso.content)
print(parsed_json['AcessoRegistrado'])

payloadFalhaAutenticao = {'numeroSerial': 1, 'usuarioId': 1}
requestFalhaAutenticao = requests.post('http://52.54.145.159:81/api/Acessos/FalhaAutenticacaoPorVideo/', params= payloadFalhaAutenticao)
print(requestFalhaAutenticao.content.decode())

payloadRegistraInvasao = {'numeroSerial': 1, 'linkVideo': 'linkteste'}
requestRegistraInvasao = requests.post('http://52.54.145.159:81/api/Invasoes/RegistraInvasao/', params= payloadRegistraInvasao)
print(requestRegistraInvasao.content.decode())