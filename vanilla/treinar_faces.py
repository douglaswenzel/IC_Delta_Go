import cv2
import numpy as np
import os

def treinar_faces():
    face_cascade = cv2.CascadeClassifier('../Cascade/haarcascade_frontalface_default.xml')
    pasta_usuarios = 'usuarios/'
    faces_treinadas = []
    ids_usuarios = []

    for usuario in os.listdir(pasta_usuarios):
        usuario_path = f'{pasta_usuarios}/{usuario}'
        if os.path.isdir(usuario_path):
            id_usuario = int(usuario)  # O ID é o nome da pasta
            for arquivo in os.listdir(usuario_path):
                caminho_imagem = f'{usuario_path}/{arquivo}'
                img = cv2.imread(caminho_imagem)
                if img is None:
                    print(f"Erro ao carregar a imagem: {caminho_imagem}")
                    continue

                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=4)

                if len(faces) == 0:
                    print(f"Nenhum rosto detectado na imagem: {arquivo}")
                    continue

                for (x, y, w, h) in faces:
                    face_roi = gray_img[y:y + h, x:x + w]
                    face_roi_redimensionado = cv2.resize(face_roi, (200, 200))
                    faces_treinadas.append(face_roi_redimensionado)
                    ids_usuarios.append(id_usuario)

    faces_treinadas = np.array(faces_treinadas)
    ids_usuarios = np.array(ids_usuarios)


    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces_treinadas, ids_usuarios)


    recognizer.save('../modelo_lbph.yml')
    np.save('../ids_usuarios.npy', ids_usuarios)
    print("Treinamento concluído e modelo LBPH salvo.")

treinar_faces()