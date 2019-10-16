#Import Modules
try:
    import numpy as np #import library numpy (working with matrix)
    import cv2         #importing open cv
    import spi
    import RPi.GPIO as GPIO
    import MFRC522
    import signal
    #import mywebserver
    import VerificaInvasao
    import requisicoesHTTP
    import time
    import opencvFunctions
    import os.path
    import AWSFunctions
    import FacialRecognition
    import leitorRFID
except ImportError as ie:
    print("Problema ao importar módulo {0}").format(ie)
    sys.exit()

while (True):
    #Constants
    reading_RFID = True
    invasaoVerificada = False
    numeroSerial = 1
    usuarioId = 0
    fotoLink = ""
    usuarioVinculado = False
    scanForFaces = False

    print ("Fechadura Ativada. Aguardando apresentação do cartão.")

    while reading_RFID and not invasaoVerificada:
        statusLeitura, uuid = leitorRFID.lerCartoes()        
        if statusLeitura:
            cardUUID = ",".join(map(str,uuid))
            usuarioId, fotoLink, usuarioVinculado = requisicoesHTTP.verificaVinculoUsuario(numeroSerial, cardUUID)
            if usuarioVinculado:
                print("Acesso liberado!")
                scanForFaces = True
                reading_RFID= False
            else:
                print("Não reconhecido")
        elif not VerificaInvasao.portaoAberto():
            #Invasao verificada
            print("InvasaoVerificada")
            invasaoVerificada=True
            reading_RFID = False
    GPIO.cleanup()
    
    if (invasaoVerificada == True):
        invasaoId = requisicoesHTTP.registraInvasao(numeroSerial)
        videoLink = opencvFunctions.gravaInvasao(invasaoId)
        requisicoesHTTP.editaLinkInvasao(invasaoId, videoLink)
        scanForFaces = False;
        invasaoVerificada = False
    
    if (scanForFaces):
    #verifica se o arquivo de imagem do usuário está baixado
        fileName = str(usuarioId) + ".jpg"
    #Se o arquivo referente ao usuário não tenha sido baixado ainda realiza o download do AWS    
        if (not os.path.isfile(fileName)):
            AWSFunctions.download_file(fileName)          
        
    #Decodifica a imagem referente ao usuário em uma matriz para realizar a comparação
        knownEncoding = FacialRecognition.knowImageEncodingSearch(fileName)
    #Abre a câmera para captura da imagem por meio da openCV
        captura = cv2.VideoCapture(0)
    #Registra o início do processo de reconhecimento, para fins de timeout
        start_time = time.time()
    #Enquanto a variável de controle de leitura estiver assinalada
        while(scanForFaces):
    #Tempo em segundos que o reconhecimento está sendo executado
            elapsedTime = time.time()-start_time
    #Se o tempo de reconhecimento for igual ou mais à 30 segundos, registra a falha na autenticação via email 
            if (elapsedTime >= 30):
                requisicoesHTTP.registraFalhaAutenticacao(numeroSerial, usuarioId)
                print("Tempo expirado")
                scanForFaces = False
    #Se o tempo não tiver expirado
            else:
    #Retorna se houve sucesso na captura do frame e o frame
                ret, frame = captura.read()
    #Verifica se a câmera conseguiu capturar o frame
                if ret:
    #Realiza o reconhecimento facial retornando True caso a face da foto seja reconhecida na câmera
                    recognition = FacialRecognition.facialRecognition(frame, knownEncoding)
                    print("Reconhecimento " + str(recognition))
    #Se reconhecido
                    if (recognition):
    #Registra o acesso
                        requisicoesHTTP.registraAcesso(numeroSerial,usuarioId)
    #Envia comando para GPIO abrir portão
    #Termina o reconhecimento facial mudando a variável de controle para Falso
                        scanForFaces = False
    #Entrar num loop aguardando portão ser aberto
                        while(not VerificaInvasao.portaoAberto()):
                            pass
    #Entra num loop aguardando portão ser fechado
                        while(VerificaInvasao.portaoAberto()):
                            pass
        captura.release()
