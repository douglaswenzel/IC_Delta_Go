import cv2
import numpy as np
import os

def treinamento():
    face_cascade = cv2.CascadeClassifier('Cascade/haarcascade_frontalface_default.xml')
    pasta_usuarios = 'usuarios/'
    faces_treinadas = []
    ids_usuarios = []

    for usuario in os.listdir(pasta_usuarios):
        usuario_path = f'{pasta_usuarios}/{usuario}'
        if os.path.isdir(usuario_path):
            id_usuario = int(usuario)  # O ID é o nome da pasta
            for arquivo in os.listdir(usuario_path):
                caminho_imagem = f'{usuario_path}/{arquivo}'
                img = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    print(f"Erro ao carregar a imagem: {caminho_imagem}")
                    continue


                equalized_img = cv2.equalizeHist(img)
                faces = face_cascade.detectMultiScale(equalized_img, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

                if len(faces) == 0:
                    print(f"Nenhum rosto detectado na imagem: {arquivo}")
                    continue

                for (x, y, w, h) in faces:
                    face_roi = equalized_img[y:y + h, x:x + w]
                    face_roi_resized = cv2.resize(face_roi, (200, 200))
                    faces_treinadas.append(face_roi_resized)
                    ids_usuarios.append(id_usuario)

    if len(faces_treinadas) == 0:
        print("Nenhuma face válida detectada. Treinamento cancelado.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(np.array(faces_treinadas), np.array(ids_usuarios))
    recognizer.save('../modelo_lbph.yml')
    np.save('ids_usuarios.npy', ids_usuarios)
    print("Treinamento concluído e modelo LBPH salvo.")

treinamento()
