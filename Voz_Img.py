import cv2
import speech_recognition as sr
import threading
import time

# Variável global para armazenar o texto da legenda
texto_legenda = ""
legenda_atualizada = False

def reconhecer_voz():
    """
    Captura e reconhece fala do usuário em um loop contínuo.
    """
    global texto_legenda, legenda_atualizada
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Ajustando para o ruído ambiente, por favor aguarde...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Pronto para capturar áudio...")
        
        while True:
            try:
                # Captura áudio do microfone
                audio = r.listen(source, timeout=3, phrase_time_limit=5)
                
                # Tenta reconhecer a fala
                novo_texto = r.recognize_google(audio, language='pt-BR')
                print(f"Você disse: {novo_texto}")
                
                # Atualiza a variável global e a flag
                texto_legenda = novo_texto
                legenda_atualizada = True

            except sr.WaitTimeoutError:
                # Nenhuma fala detectada, continua o loop
                pass
            except sr.UnknownValueError:
                print("Não consegui entender o áudio.")
                # Limpa a legenda se não entender
                texto_legenda = ""
                legenda_atualizada = True
            except sr.RequestError as e:
                print(f"Erro no serviço de reconhecimento de fala: {e}")
                texto_legenda = "Erro no serviço de fala"
                legenda_atualizada = True

def main():
    global texto_legenda, legenda_atualizada

    # Inicia a thread de reconhecimento de voz
    thread_voz = threading.Thread(target=reconhecer_voz, daemon=True)
    thread_voz.start()

    # --- Configurações da Webcam ---
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_FPS, 30)  # Solicita 30 FPS à webcam

    # Variáveis para controlar a exibição do texto
    tempo_exibicao = 5 # Tempo em segundos para a legenda ficar na tela
    tempo_ultimo_update = time.time()

    # Variáveis para cálculo de FPS
    prev_time = time.time()
    fps = 0

    frame_time = 1.0 / 30  # Tempo alvo por frame (em segundos)

    while True:
        loop_start = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        # Cálculo do FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        # Se a legenda foi atualizada, salva o tempo
        if legenda_atualizada:
            tempo_ultimo_update = time.time()
            legenda_atualizada = False

        # Calcula o tempo que a legenda está na tela
        tempo_passado = time.time() - tempo_ultimo_update

        # Exibe a legenda apenas se o tempo não tiver expirado
        if tempo_passado < tempo_exibicao and texto_legenda:
            # Configurações do texto
            fonte = cv2.FONT_HERSHEY_SIMPLEX
            tamanho_fonte = 1.0
            cor_texto = (255, 255, 255)  # Branco
            espessura_linha = 2
            
            # Adiciona um fundo semi-transparente para melhorar a visibilidade
            (largura_texto, altura_texto), _ = cv2.getTextSize(texto_legenda, fonte, tamanho_fonte, espessura_linha)
            cv2.rectangle(frame, (10, frame.shape[0] - 50), (10 + largura_texto + 10, frame.shape[0] - 50 + altura_texto + 10), (0, 0, 0), cv2.FILLED)
            
            # Desenha a legenda na parte inferior esquerda
            cv2.putText(frame, texto_legenda, (20, frame.shape[0] - 30), fonte, tamanho_fonte, cor_texto, espessura_linha, cv2.LINE_AA)

        # Mostra o FPS na tela
        #cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Minha Webcam com Legenda', frame)
        
        # Sai do loop se a tecla 'q' for pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Espera o tempo necessário para manter 30 FPS
        elapsed = time.time() - loop_start
        if elapsed < frame_time:
            time.sleep(frame_time - elapsed)
    
    # Libera a câmera e fecha todas as janelas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()