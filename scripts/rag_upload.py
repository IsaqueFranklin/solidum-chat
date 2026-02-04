import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

API_KEY = os.getenv("OPEN_WEB_UI_API_KEY")
URL_BASE = os.getenv("OPEN_WEB_URL_BASE")

def delete_collection(collection_name):
    url = f"{URL_BASE}/files/"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # 1. LISTAR E DELETAR ANTIGOS
    print(f"Limpando documentos da coleção '{collection_name}'...")
    try:
        res = requests.get(url, headers=headers)

        # Verificamos se a resposta é válida e não vazia
        if res.status_code == 200 and res.text.strip():

            # Se a resposta estiver vazia mas com status 200, retornamos True para prosseguir
            if not res.text.strip():
                print("Nenhum arquivo encontrado no servidor. Prosseguindo...")
                return True
                
            files = res.json()
            # Se for uma lista vazia [], também prosseguimos
            if not files:
                print("Coleção já está vazia.")
                return True
            
            files = res.json()
            for file in files:
                meta = file.get('meta', {})
                # Filtra pela tag de coleção definida no upload anterior
                if meta.get('collection_name') == collection_name:
                    file_id = file['id']
                    print(f"🗑️ Deletando arquivo: {file.get('filename')} (ID: {file_id})")
                    requests.delete(f"{url}{file_id}", headers=headers)
            return True
    except Exception as e:
        print(f"⚠️ Erro ao limpar coleção '{collection_name}': {e}")
        return False
    
def upload_openwebui(caminho_csv, name_tag, collection_name):
    url = f"{URL_BASE}/files/"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # 'rb' abre o arquivo em modo de leitura binária, necessário para upload.
    with open(caminho_csv, 'rb') as file:
        files = {'file': file}

        # O campo collection_name é crucial para o langchain filtrar os dados futuramente
        payload = {
            'name': name_tag,
            'collection_name': collection_name,
        }

        print(f"Enviando {name_tag} para OpenWebUI...")
        response = requests.post(url, headers=headers, files=files, data=payload)

    if response.status_code == 200:
        print(f"Upload de {name_tag} realizado com sucesso!")
        return response.json()
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None
    
if __name__ == "__main__":
    deleted = delete_collection('docentes')
    if deleted:
        final = upload_openwebui('docentes_prpq.md', 'Docentes RAG', 'docentes')
        print(final)
    else:
        print("Falha ao limpar coleção. Upload cancelado.")