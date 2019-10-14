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
except ImportError as ie:
    print("Problema ao importar módulo {0}").format(ie)
    sys.exit()

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    reading_RFID = False
    GPIO.cleanup()

while (True):
        
    #Constants
    reading_RFID = True
    invasaoVerificada = False
    numeroSerial = 1
    usuarioId = 0
    fotoLink = ""
    usuarioVinculado = False
    scanForFaces = False
    BLUE_COLOR = (255, 0, 0)
    STROKE = 2
    
    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # Welcome message
    print ("Fechadura Ativada. Aguardando apresentação do cartão.")
    #print ("Press Ctrl-C to stop.")

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while reading_RFID and not invasaoVerificada:
        # Scan for cards    
        MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            # Print UID
            print ("Card read UID: %s,%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3],uid[4]))
            cardUUID = ",".join(map(str,uid))
            usuarioId, fotoLink, usuarioVinculado = requisicoesHTTP.verificaVinculoUsuario(numeroSerial, cardUUID)
            if usuarioVinculado:
                print("Acesso liberado!")
                scanForFaces = True
                reading_RFID= False
            else:
                print("Não reconhecido")
        elif not VerificaInvasao.verificaArrombamento():
            #Invasao verificada
            print("Enter here")
            invasaoVerificada=True
    
    if (invasaoVerificada == True):
        invasaoId = requisicoesHTTP.registraInvasao(numeroSerial)
        videoLink = opencvFunctions.gravaInvasao(invasaoId)
        requisicoesHTTP.editaLinkInvasao(invasaoId, videoLink)
        scanForFaces = False;
        invasaoVerificada = False
    
    xml_path = 'haarcascade_frontalface_alt2.xml'
    cap = cv2.VideoCapture(0)
    clf = cv2.CascadeClassifier(xml_path)
    
    #verifica se o arquivo de imagem do usuário está baixado
    fileName = str(usuarioId) + ".jpg"
    if (not os.path.isfile(fileName)):
        AWSFunctions.download_file(fileName)    
    
    start_time = time.time()
    while(scanForFaces):
        #capture frame-by-frame
        elapsedTime = time.time()-start_time
        if (elapsedTime >= 30):
            requisicoesHTTP.registraFalhaAutenticacao(numeroSerial, usuarioId)
            scanForFaces = False
            
        ret, frame = cap.read()#read image and return true or false
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#image operation
        faces = clf.detectMultiScale(gray)
        for x,y,w,h in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), BLUE_COLOR, STROKE)
        cv2.imshow('frame',frame)
        
        #if reconhecimento tiver sucesso
        #requisicoesHTTP.registraAcesso(numeroSerial,usuarioId)
        #Envia comando para GPIO abrir portão
        
    cap.release()               #release the capture
    cv2.destroyAllWindows()     #destroy all windows created
