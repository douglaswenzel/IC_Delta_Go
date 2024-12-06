from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import os

app = Flask(__name__)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def gerar_video():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    model_path = '../../modelo_lbph.yml'
    ids_path = '../ids_usuarios.npy'

    if not os.path.exists(model_path) or not os.path.exists(ids_path):
        print("Arquivos de modelo ou IDs não encontrados.")
        return

    recognizer.read(model_path)
    ids_usuarios = np.load(ids_path)
    cap = cv2.VideoCapture(2)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame da câmera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]
            face_resized = cv2.resize(face_roi, (200, 200))
            user_id, confidence = recognizer.predict(face_resized)

            if confidence < 50:
                color = (0, 255, 0)
                label = f"ID: {user_id}"
            else:
                color = (0, 0, 255)
                label = "Não autenticado"

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gerar_video(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')



@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    # Dados do formulário de cadastro
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    matricula = request.form['matricula']
    sexo = request.form['sexo']
    tipo = request.form['tipo']
    unidade = request.form['unidade']

    usuario = {
        'nome': nome,
        'sobrenome': sobrenome,
        'matricula': matricula,
        'sexo': sexo,
        'tipo': tipo,
        'unidade': unidade
    }

    return render_template('usuarios/usuariox.html', usuario=usuario)


# Rota para alterar a foto do usuário
@app.route('/alterar_foto', methods=['POST'])
def alterar_foto():
    return redirect(url_for('cadastro'))

if __name__ == '__main__':
    app.run(debug=True)
