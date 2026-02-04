import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

URL_BASE = os.getenv("OPEN_WEB_URL_BASE")
TOKEN = os.getenv("OPEN_WEB_UI_API_KEY")

def link_to_knowledge_base(knowledge_id, file_id):
    url = f"{URL_BASE}/knowledge/{knowledge_id}/file/add"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"file_id": file_id}
    
    print(f"Vinculando arquivo {file_id} ao Workspace {knowledge_id}...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Sucesso! O arquivo agora é visível no Workspace.")
        return response.json()
    else:
        print(f"Erro ao vincular: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    KNOWLEDGE_ID = "7a9224da-361a-468d-aaa3-e213f9d2c5e4"
    FILE_ID = "6476714d-4332-46b3-a665-34fae43be443"
    
    link_to_knowledge_base(KNOWLEDGE_ID, FILE_ID)