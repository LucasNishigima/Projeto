import requests
import json

# URL da API de tradução do VLibras (este é um exemplo, pode não ser o atual)
api_url = "https://dicionario2-dth.vlibras.gov.br/api"

# Texto em português para ser traduzido
texto_para_traduzir = "Olá, como você está?"

# Dados a serem enviados na requisição POST
payload = {
    "texto": texto_para_traduzir,
    "formato_retorno": "glosa" # Ou 'video', dependendo da API
}

# Cabeçalhos da requisição (pode ser necessário um 'Content-Type')
headers = {
    "Content-Type": "application/json"
}

try:
    # Faz a requisição POST para a API
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)

    # Verifica se a requisição foi bem sucedida
    response.raise_for_status()

    # Pega os dados JSON da resposta
    dados_traduzidos = response.json()

    print("Resposta da API:")
    print(dados_traduzidos)
    
except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro ao conectar à API: {e}")