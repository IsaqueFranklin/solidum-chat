import json
import os
import shutil

def export_to_txt_files(df_final):
    output_dir = "docentes_txt"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    print(f"Gerando {len(df_final)} arquivos individuais...")
    for _, row in df_final.iterrows():
        # Nome do arquivo seguro: ID_Nome.txt
        nome_docente_slug = "".join(c for c in str(row['id_docente']) if c.isalnum())
        file_path = os.path.join(output_dir, f"{nome_docente_slug}.txt")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(row['conteudo'])
    
    # Compacta a pasta em um ZIP
    shutil.make_archive("docentes_prpq", 'zip', output_dir)
    print("Arquivo 'docentes_prpq.zip' gerado com sucesso!")

def export_to_jsonl(df_final):
    file_path = "docentes_prpq.jsonl"
    print(f"Gerando arquivo JSONL único...")
    
    with open(file_path, "w", encoding="utf-8") as f:
        for _, row in df_final.iterrows():
            # Formato padrão que o Open WebUI e LangChain amam
            data = {
                "text": row['conteudo'],
                "meta": {
                    "id_docente": str(row['id_docente']),
                    "departamento": row['departamento_docente']
                }
            }
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
            
    print(f"Arquivo '{file_path}' gerado!")