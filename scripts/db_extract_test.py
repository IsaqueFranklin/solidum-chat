import pandas as pd
from sqlalchemy import create_engine, text
import os
import shutil
import csv
from dotenv import load_dotenv
import json

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"))

def limpo(valor):
    if valor is None:
        return False
    v = str(valor).strip().lower()
    return v not in ['none', 'desconhecido', 'nan', 'null', '']

def formatar_docente(group):
    row = group.iloc[0].to_dict()  # Pegamos a primeira linha do grupo para acessar os dados do docente

    nome = str(row['nome_docente'])
    partes = [f"DADOS DO DOCENTE: {nome}"]

    if limpo(row.get('departamento_docente')):
        depto_docente = str(row.get('departamento_docente'))
        partes.append(f"O docente {nome} é do Departamento de {depto_docente}.")

    if limpo(row.get('unidade_docente')):
        unidade_docente = str(row.get('unidade_docente'))
        partes.append(f"O docente {nome} é da Unidade acadêmica de(a) {unidade_docente}.")

    if limpo(row.get('docente_area_the')):
        area_the_docente = str(row.get('docente_area_the'))
        partes.append(f"O docente {nome} é da Área THE: {area_the_docente}.")

    if limpo(row.get('docente_grande_area')):
        grande_area_docente = str(row.get('docente_grande_area'))
        partes.append(f"O docente {nome} pertence à grande área de {grande_area_docente}.")

    if limpo(row.get('docente_area')):
        area_docente = str(row.get('docente_area', 'None'))
        partes.append(f"O docente {nome} pesquisa sobre {area_docente}.")

    if limpo(row.get('docente_colegio_capes')):
        colegio_capes_docente = str(row.get('docente_colegio_capes'))
        partes.append(f"O docente {nome} pertence ao colégio acadêmico CAPES {colegio_capes_docente}.")

    if limpo(row.get('docente_nivel_bolsa')):
        nivel_bolsa_docente = str(row.get('docente_nivel_bolsa'))
        partes.append(f"O docente {nome} tem nível de bolsa no CNPQ: {nivel_bolsa_docente}.")

    if limpo(row.get('docente_area_bolsa')):
        area_bolsa_docente = str(row.get('docente_area_bolsa'))
        partes.append(f"O docente {nome} tem área de bolsa do CNPQ: {area_bolsa_docente}.")

    if limpo(row.get('docente_area_atuacao')):
        area_atuacao_docente = str(row.get('docente_area_atuacao'))
        partes.append(f"O docente {nome} tem área de atuação de pesquisa: {area_atuacao_docente}.")

    especs = [str(e) for e in group['docente_especialidade'].dropna().unique() if limpo(e)]
    if especs:
        partes.append(f"O docente {nome} é tem especialidades de pesquisa: {', '.join(especs)}.")

    especs = group['docente_especialidade'].dropna().unique()
    
    content = " | ".join(partes)
    
    return pd.Series({
        'conteudo': content,
        'nome_docente': row.get('nome_docente'),
        'departamento_docente': row.get('departamento_docente', 'UFMG'),
    })

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

def extract_professors():
    query = text("SELECT id_docente, nome_docente, departamento_docente, unidade_docente, docente_area_the, docente_area, docente_grande_area, docente_grande_area, docente_colegio_capes, docente_nivel_bolsa, docente_area_bolsa, docente_area_atuacao, docente_especialidade FROM docente_geral")
    
    with engine.connect() as connection:
        df = pd.read_sql_query(query, connection)

    print("Achatando dados e consolidando especialidades...")
    
    # Adicionamos include_groups=False para silenciar o warning
    df_final = df.groupby('id_docente', group_keys=True).apply(
        formatar_docente, 
        include_groups=False
    ).reset_index()
    
    # O reset_index() vai criar a coluna 'id_docente' a partir do índice do grupo
    export_to_markdown(df_final)

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

def export_to_markdown(df_final):
    file_path = "docentes_prpq.md"
    print(f"📄 Gerando arquivo Markdown consolidado...")
    
    with open(file_path, "w", encoding="utf-8") as f:
        for _, row in df_final.iterrows():
            # Cabeçalho de nível 2 isola o docente para o RAG
            f.write(f"## Docente: {row['nome_docente']}\n\n")
            
            # O conteúdo denso que você formatou
            f.write(f"{row['conteudo']}\n\n")
            
            # Metadados úteis para o LLM citar
            f.write(f"**ID Registro:** {row['id_docente']} | **Departamento:** {row['departamento_docente']}\n")
            
            # Linha horizontal: O separador definitivo de contexto
            f.write("\n---\n\n")
            
    print(f"Arquivo '{file_path}' gerado com sucesso!")

if __name__ == "__main__":
    extract_professors()