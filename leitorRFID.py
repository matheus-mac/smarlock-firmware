import MFRC522
import signal

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    reading_RFID = False
    GPIO.cleanup()

def lerCartoes():
    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()
    
    # Scan for cards    
    MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        print ("Card read UID: %s,%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3],uid[4]))
        return True, uid
    else:
        return False, ""
