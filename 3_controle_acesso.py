import cv2
import numpy as np

def controle_acesso():

    face_cascade = cv2.CascadeClassifier('Cascade/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('../modelo_lbph.yml')
    ids_usuarios = np.load('ids_usuarios.npy')

    cap = cv2.VideoCapture(2)

    while True:
        ret, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        for (x, y, w, h) in faces:
            face_roi = gray_frame[y:y + h, x:x + w]
            face_roi_resized = cv2.resize(face_roi, (200, 200))
            face_roi_equalized = cv2.equalizeHist(face_roi_resized)


            user_id, confidence = recognizer.predict(face_roi_equalized)


            if confidence < 66:
                color = (0, 255, 0)
                label = f"ID: {user_id} (Conf: {confidence:.2f})"
            else:
                color = (0, 0, 255)
                label = "Nao autorizado"


            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow('Controle de Acesso', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

controle_acesso()
