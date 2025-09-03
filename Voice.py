import speech_recognition as sr

def reconhecer_voz(timeout: int = 5, phrase_time_limit: int = 7) -> str | None:
    """
    Captura e reconhece fala do usuário usando Google Speech Recognition.
    :param timeout: tempo máximo de espera pelo início da fala (segundos)
    :param phrase_time_limit: tempo máximo de gravação da fala (segundos)
    :return: texto reconhecido ou None se não for possível reconhecer
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando para o ruído ambiente, por favor aguarde...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Fale alguma coisa...")
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("Tempo de espera excedido. Nenhuma fala detectada.")
            return None

    try:
        texto = r.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {texto}")
        return texto
    except sr.UnknownValueError:
        print("Não consegui entender o áudio.")
        return None
    except sr.RequestError as e:
        print(f"Erro no serviço de reconhecimento de fala: {e}")
        return None

def main():
    tentativas = 3
    for tentativa in range(1, tentativas + 1):
        texto_reconhecido = reconhecer_voz()
        if texto_reconhecido:
            print("Texto pronto para ser traduzido.")
            break
        else:
            print(f"Tentativa {tentativa} de {tentativas} falhou.\n")
    else:
        print("Não foi possível reconhecer a fala após várias tentativas.")

if __name__ == "__main__":
    main()