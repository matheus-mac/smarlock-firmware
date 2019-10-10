#Import Modules
try:
    import numpy as np #import library numpy (working with matrix)
    import cv2         #importing open cv
    import spi
    import RPi.GPIO as GPIO
    import MFRC522
    import signal
    import mywebserver
except ImportError as ie:
    print("Problema ao importar módulo {0}").format(ie)
    sys.exit()
    
#Constants
acessos_autorizados = [[221,36,133,137,245]]
reading_RFID = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    reading_RFID = False
    GPIO.cleanup()

while (True):
    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # Welcome message
    print ("Fechadura Ativada. Aguardando apresentação do cartão.")
    #print ("Press Ctrl-C to stop.")

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while reading_RFID:
        # Scan for cards    
        MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            # Print UID
            print ("Card read UID: %s,%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3],uid[4]))
            #This condition will be replaced by an API
            if uid in acessos_autorizados:
                print("Acesso liberado!")
                reading_RFID= False
            else:
                print("Não reconhecido")
    
    
    
    #xml_path = 'haarcascade_frontalface_alt2.xml'
    cap = cv2.VideoCapture(0)
    clf = cv2.CascadeClassifier(xml_path)
    
    while(True):
        #capture frame-by-frame
        ret, frame = cap.read()#read image and return true or false
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#image operation
        #faces = clf.detectMultiScale(gray)
        #for x,y,w,h in faces:
        #    cv2.rectangle(frame, (x,y), (x+w, y+h), BLUE_COLOR, STROKE)
        cv2.imshow('frame',frame)#functio to display an image
                                #(window name, image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                                #waitKey keyboard binding function (time ms)
                                #& 0xFF read condition on 64bit machine
                                #ord('q') conversion of unicode to q
    cap.release()               #release the capture
    cv2.destroyAllWindows()     #destroy all windows created
