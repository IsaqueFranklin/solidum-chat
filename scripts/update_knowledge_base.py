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
    KNOWLEDGE_ID = "4aa81cc8-8f1a-454e-96e0-a94c5fb11401"
    FILE_ID = "91fc3991-315a-431a-87cd-97917be09421"
    
    link_to_knowledge_base(KNOWLEDGE_ID, FILE_ID)