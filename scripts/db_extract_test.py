import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"))

def limpo(valor):
    if valor is None:
        return False
    v = str(valor).strip().lower()
    return v not in ['none', 'desconhecido', 'nan', 'null', '']

def formatar_docente(group):
    row = group.iloc[0].to_dict()  # Pegamos a primeira linha do grupo para acessar os dados do docente

    partes = ['']

    if limpo(row.get('departamento_docente')):
        depto_docente = str(row.get('departamento_docente'))
        partes.append(f"De: {depto_docente}\n")

    if limpo(row.get('unidade_docente')):
        unidade_docente = str(row.get('unidade_docente'))
        partes.append(f"Unidade: {unidade_docente}\n")

    if limpo(row.get('docente_area_the')):
        area_the_docente = str(row.get('docente_area_the'))
        partes.append(f"Área THE: {area_the_docente}\n")

    if limpo(row.get('docente_grande_area')):
        grande_area_docente = str(row.get('docente_grande_area'))
        partes.append(f"Grande área: {grande_area_docente}\n")

    if limpo(row.get('docente_area')):
        area_docente = str(row.get('docente_area', 'None'))
        partes.append(f"Pesquisa sobre: {area_docente}\n")

    if limpo(row.get('docente_colegio_capes')):
        colegio_capes_docente = str(row.get('docente_colegio_capes'))
        partes.append(f"Colégio CAPES: {colegio_capes_docente}\n")

    if limpo(row.get('docente_nivel_bolsa')):
        nivel_bolsa_docente = str(row.get('docente_nivel_bolsa'))
        partes.append(f"Nível de bolsa no CNPQ: {nivel_bolsa_docente}\n")

    if limpo(row.get('docente_area_bolsa')):
        area_bolsa_docente = str(row.get('docente_area_bolsa'))
        partes.append(f"Área de bolsa do CNPQ: {area_bolsa_docente}\n")

    if limpo(row.get('docente_area_atuacao')):
        area_atuacao_docente = str(row.get('docente_area_atuacao'))
        partes.append(f"área de atuação: {area_atuacao_docente}\n")

    especs = [str(e) for e in group['docente_especialidade'].dropna().unique() if limpo(e)]
    especs_top3 = especs[:3]
    if especs:
        # Une as especialidades em uma string única
        texto_especs = ', '.join(especs_top3)
        partes.append(f"Especialidades: {texto_especs}\n")
    
    content = " | ".join(partes)
    
    return pd.Series({
        'conteudo': content,
        'nome_docente': str(row.get('nome_docente')),
        'departamento_docente': str(row.get('departamento_docente', 'UFMG')),
    })

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

def export_to_markdown(df_final):
    file_path = "docentes_prpq.md"
    print(f"Gerando arquivo Markdown consolidado...")
    
    with open(file_path, "w", encoding="utf-8") as f:
        for _, row in df_final.iterrows():
            # Cabeçalho de nível 2 isola o docente para o RAG
            f.write(f"## {row['nome_docente']}")

            f.write("\n\n")
            # Conteúdo do docente
            f.write(row['conteudo'])
            f.write(f"\n\n **ID Registro:** {row['id_docente']}\n **Departamento:** {row['departamento_docente']}\n")
            # Linha horizontal: O separador definitivo de contexto
            f.write("\n---\n\n")
            
    print(f"Arquivo '{file_path}' gerado com sucesso!")

if __name__ == "__main__":
    extract_professors()