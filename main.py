import cv2
import mediapipe as mp
import math
import time

# Abrir a webcam
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Func que abre a câmera
mp_face_mesh = mp.solutions.face_mesh  # Inicia o mediapipe face
face_mesh = mp_face_mesh.FaceMesh()  # Instancia a função FaceMesh
mp_drawing = mp.solutions.drawing_utils  # Desenha os landmarks na tela

# Variável de tempo
initial = 0
status = ''
tempo = 0

# Loop que retorna a imagem
while True:
    check, img = video.read()
    img = cv2.resize(img, (1000, 720))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converter a imagem para RGB
    results = face_mesh.process(img_rgb)  # Processa a imagem RGB
    h, w, _ = img.shape  # Extrair as dimensões da tela

    # Verifica se existem landmarks detectados
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Acessa os pontos faciais necessários
            landmark_159 = face_landmarks.landmark[159]  # Ponto 159 (olho direito ponto 1)
            landmark_145 = face_landmarks.landmark[145]  # Ponto 145 (olho direito ponto 2)
            landmark_386 = face_landmarks.landmark[386]  # Ponto 386 (olho esquerdo ponto 1)
            landmark_374 = face_landmarks.landmark[374]  # Ponto 374 (olho esquerdo ponto 2)

            di1x, di1y = int((landmark_159.x) * w), int((landmark_159.y) * h)
            di2x, di2y = int((landmark_145.x) * w), int((landmark_145.y) * h)
            es1x, es1y = int((landmark_386.x) * w), int((landmark_386.y) * h)
            es2x, es2y = int((landmark_374.x) * w), int((landmark_374.y) * h)

            # Visualizar os pontos
            cv2.circle(img, (di1x, di1y), 1, (255, 0, 0), 2)
            cv2.circle(img, (di2x, di2y), 1, (255, 0, 0), 2)
            cv2.circle(img, (es1x, es1y), 1, (255, 0, 0), 2)
            cv2.circle(img, (es2x, es2y), 1, (255, 0, 0), 2)

            # Identificar a distância entre os pontos de cada olho
            distDi = math.hypot(di1x - di2x, di1y - di2y)
            distEs = math.hypot(es1x - es2x, es1y - es2y)

            # Lógica para olhos fechados
            if distDi <= 10 and distEs <= 10:
                cv2.rectangle(img, (100, 30), (390, 80), (0, 0, 255), -1)
                cv2.putText(img, 'OLHOS FECHADOS', (105, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                situacao = 'F'
                if situacao != status:  # Inicia o temporizador quando os olhos fecham
                    initial = time.time()

                # Calcula o tempo apenas se os olhos estiverem fechados
                tempo = int(time.time() - initial)

            else:
                cv2.rectangle(img, (100, 30), (370, 80), (0, 255, 0), -1)
                cv2.putText(img, 'Olhos abertos', (105, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                situacao = 'A'
                initial = time.time()  # Reinicia o tempo quando os olhos estão abertos

            # Exibir a distância (para debug se necessário)
            # print(distDi, distEs)

            # Lógica para monitorar o tempo de olhos fechados
            if situacao == 'F':
                tempo = int(time.time() - initial)

            # Atualizar o status
            status = situacao

            # Mensagem de alerta na tela se os olhos estiverem fechados por 2 ou mais segundos
            if tempo >= 2:
                cv2.rectangle(img, (300, 150), (850, 220), (0, 0, 255), -1)
                cv2.putText(img, f'DORMINDO {tempo} SEG', (310, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (255, 255, 255), 5)
            print(tempo)

    cv2.imshow('IMG', img)  # Exibir a imagem
    if cv2.waitKey(1) & 0xFF == 27:  # Pressione 'ESC' para sair
        break

# Libera a captura de vídeo e fecha as janelas
video.release()
cv2.destroyAllWindows()
