import requests
import json

def verificaVinculoUsuario( numeroSerial, rfidUUID ):
    payload = {'numeroSerial': numeroSerial, 'rfidUUID': rfidUUID}
    r = requests.get('http://52.54.145.159:81/api/Fechaduras/VerificaCadastroUsuario/', params= payload)
    parsed_json = json.loads(r.content)
    return parsed_json['UsuarioId'], parsed_json['Foto'], parsed_json['UsuarioVinculado'] 
    print (r.content)

def registraAcesso( numeroSerial, usuarioId ):
    payloadRegistraAcesso = {'numeroSerial': numeroSerial, 'usuarioId': usuarioId}
    requestRegistraAcesso = requests.post('http://52.54.145.159:81/api/Acessos/RegistraAcesso/', params= payloadRegistraAcesso)
    parsed_json = json.loads(requestRegistraAcesso.content)
    print(parsed_json['AcessoRegistrado'])

def registraFalhaAutenticacao( numeroSerial, usuarioId ):
    payloadFalhaAutenticao = {'numeroSerial': numeroSerial, 'usuarioId': usuarioId}
    requestFalhaAutenticao = requests.post('http://52.54.145.159:81/api/Acessos/FalhaAutenticacaoPorVideo/', params= payloadFalhaAutenticao)
    print(requestFalhaAutenticao.content.decode())

def registraInvasao( numeroSerial ):
    payloadRegistraInvasao = {'numeroSerial': numeroSerial}
    requestRegistraInvasao = requests.post('http://52.54.145.159:81/api/Invasoes/RegistraInvasao/', params= payloadRegistraInvasao)
    
def editaLinkInvasao( invasaoId, videoLink ):
    payloadEditaLinkInvasao = {'invasaoId': invasaoId, 'videoLink': videoLink}
    requestEditaLinkInvasao = requests.post('http://52.54.145.159:81/api/Invasoes/EditaLinkInvasao/', params= payloadEditaLinkInvasao)
    print(EditaLinkInvasao.content.decode())