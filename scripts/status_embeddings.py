import requests
import os
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

API_KEY = os.getenv("OPEN_WEB_UI_API_KEY")
URL_BASE = os.getenv("OPEN_WEB_URL_BASE")

def check_embedding_status(file_id):
    """Monitora o endpoint de status até que os embeddings terminem."""
    url = f"{URL_BASE}/files/{file_id}/process/status"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    print(f"Verificando processamento do arquivo {file_id}...")

    retries = 0
    max_retries = 15 # Tenta 5 vezes antes de desistir se der 502
    
    while True:
        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                result = response.json()
                status = result.get('status')

                if status == 'completed':
                    print("Processamento concluído com sucesso!")
                    return True
                elif status == 'failed':
                    print(f"Falha no processamento: {result.get('error')}")
                    return False
                else:
                    print(f"Status atual: {status}. Aguardando 3 segundos para nova verificação...")
            
            elif response.status_code == 502:
                retries += 1
                print(f"⚠️ Erro 502 (Bad Gateway). Tentativa {retries}/{max_retries}...")
                if retries >= max_retries: return False

            else:
                print(f"Erro ao verificar status: {response.status_code} - {response.text}")
                return False
            
            time.sleep(3)
        except Exception as e:
            print(f"Erro na verificação do status: {e}")
            return False
        
if __name__ == "__main__":
    test_file_id = "35efbfb8-1aff-4248-86b7-a0952666ea49"
    check_embedding_status(test_file_id)