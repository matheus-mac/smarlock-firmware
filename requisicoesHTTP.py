import requests
import json

linkServidor = "http://52.54.145.159:81/api/"

def verificaVinculoUsuario( numeroSerial, rfidUUID ):
    payload = {'numeroSerial': numeroSerial, 'rfidUUID': rfidUUID}
    r = requests.get(linkServidor + 'Fechaduras/VerificaCadastroUsuario/', params= payload)
    parsed_json = json.loads(r.content)
    return parsed_json['UsuarioId'], parsed_json['Foto'], parsed_json['UsuarioVinculado'] 
    print ("Verificou vínculo do usuário")

def registraAcesso( numeroSerial, usuarioId ):
    payloadRegistraAcesso = {'numeroSerial': numeroSerial, 'usuarioId': usuarioId}
    requestRegistraAcesso = requests.post(linkServidor + 'Acessos/RegistraAcesso/', params= payloadRegistraAcesso)
    parsed_json = json.loads(requestRegistraAcesso.content)
    print("Acesso Registrado: " + str(parsed_json['AcessoRegistrado']))

def registraFalhaAutenticacao( numeroSerial, usuarioId ):
    payloadFalhaAutenticao = {'numeroSerial': numeroSerial, 'usuarioId': usuarioId}
    requestFalhaAutenticao = requests.post(linkServidor + 'Acessos/FalhaAutenticacaoPorVideo/', params= payloadFalhaAutenticao)
    print("Registrou Falha na autenticação: " + requestFalhaAutenticao.content.decode())

def registraInvasao( numeroSerial ):
    payloadRegistraInvasao = {'numeroSerial': numeroSerial}
    requestRegistraInvasao = requests.post(linkServidor + 'Invasoes/RegistraInvasao/', params= payloadRegistraInvasao)
    print("Registrou invasão: " + requestRegistraInvasao.content.decode()) 
    
def editaLinkInvasao( invasaoId, videoLink ):
    payloadEditaLinkInvasao = {'invasaoId': invasaoId, 'videoLink': videoLink}
    requestEditaLinkInvasao = requests.post(linkServidor + 'Invasoes/EditaLinkInvasao/', params= payloadEditaLinkInvasao)
    print("Editou link da invasão: " + EditaLinkInvasao.content.decode())