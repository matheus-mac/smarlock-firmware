import face_recognition
import cv2

def knowImageEncodingSearch(fileName):
    known_image = face_recognition.load_image_file (fileName)
    known_encoding = face_recognition.face_encodings (known_image) [ 0 ]
    return known_encoding
    
def facialRecognition(frame, known_encoding):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations(rgb_small_frame)
    print("face location" + str(face_locations))
    face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
    
    recognition = False
    for face_encoding in face_encodings:
        recognition = face_recognition.compare_faces ([known_encoding], face_encoding)
        print("recognition" + str(recognition))
        if recognition:
            break
    return recognition