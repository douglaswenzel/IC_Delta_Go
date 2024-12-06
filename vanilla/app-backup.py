from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

def gerar_video():
    face_cascade = cv2.CascadeClassifier('../Cascade/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('../modelo_lbph.yml')
    ids_usuarios = np.load('../ids_usuarios.npy')
    cap = cv2.VideoCapture(2)

    while True:
        ret, frame = cap.read()
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gerar_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
