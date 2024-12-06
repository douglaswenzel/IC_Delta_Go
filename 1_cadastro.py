import cv2
import os

def cadastrar_usuario(user_id):
    cap = cv2.VideoCapture(2)  # Certifique-se de que o índice da câmera está correto.
    print(f"Capturando imagens para o usuário ID: {user_id}")


    if not os.path.exists(f'usuarios/{user_id}'):
        os.makedirs(f'usuarios/{user_id}')

    count = 0
    face_cascade = cv2.CascadeClassifier('Cascade/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('Cascade/haarcascade_eye.xml')

    while count < 35:
        ret, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        equalized_frame = cv2.equalizeHist(gray_frame)


        faces = face_cascade.detectMultiScale(equalized_frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        for (x, y, w, h) in faces:
            face_roi = equalized_frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=3, minSize=(15, 15))


            if len(eyes) >= 2:
                face_roi_resized = cv2.resize(face_roi, (200, 200))
                cv2.imwrite(f'usuarios/{user_id}/{count}.jpg', face_roi_resized)
                count += 1
                print(f"Imagem {count} capturada para o usuário ID: {user_id}")

        cv2.imshow('Capturando Imagens', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Cadastro concluído!")
[]
cadastrar_usuario(100)
