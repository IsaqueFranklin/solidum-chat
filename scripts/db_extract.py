import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import csv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"))

def extract_professors():
    query = text("SELECT id_docente, nome_docente, departamento_docente, unidade_docente, docente_area_the, docente_area, docente_grande_area, docente_grande_area, docente_colegio_capes, docente_nivel_bolsa, docente_area_bolsa, docente_area_atuacao, docente_especialidade FROM docente_geral")
        
    with engine.connect() as connection:
        # O Pandas lê o resultado da consulta SQL diretamente em um DataFrame
        df = pd.read_sql_query(query, connection)

    # Agrupar por id_docente para consolidar especialidades
    print("Achatando dados e consolidando especialidades...")
    df_final = df.groupby('id_docente', group_keys=True).apply(formatar_docente, include_groups=False).reset_index()
    
    # Criando o cerébro do RAG
    # Ao invés de colunas soltas, conectamos tudo em uma única coluna de texto
    df_final[['conteudo', 'departamento_docente', 'id_docente']].to_csv(
        'docentes_rag.csv',
        index=False,
        header=False,
        encoding='utf-8',
        quoting=csv.QUOTE_ALL
    )

    print(F"Arquivo docentes_rag.csv gerado com sucesso! Contém {len(df_final)} docentes únicos.")

def formatar_docente(group):
    row = group.iloc[0].to_dict()  # Pegamos a primeira linha do grupo para acessar os dados do docente

    nome = str(row['nome_docente'])
    partes = [f"{nome}"]

    if limpo(row.get('departamento_docente')):
        depto_docente = str(row.get('departamento_docente'))
        partes.append(f"{nome} é do Departamento de {depto_docente}.")

    if limpo(row.get('unidade_docente')):
        unidade_docente = str(row.get('unidade_docente'))
        partes.append(f"{nome} é da Unidade acadêmica de(a) {unidade_docente}.")

    if limpo(row.get('docente_area_the')):
        area_the_docente = str(row.get('docente_area_the'))
        partes.append(f"{nome} é da Área THE: {area_the_docente}.")

    if limpo(row.get('docente_grande_area')):
        grande_area_docente = str(row.get('docente_grande_area'))
        partes.append(f"{nome} pertence à grande área de {grande_area_docente}.")

    if limpo(row.get('docente_area')):
        area_docente = str(row.get('docente_area', 'None'))
        partes.append(f"{nome} pesquisa sobre {area_docente}.")

    if limpo(row.get('docente_colegio_capes')):
        colegio_capes_docente = str(row.get('docente_colegio_capes'))
        partes.append(f"{nome} pertence ao colégio acadêmico CAPES {colegio_capes_docente}.")

    if limpo(row.get('docente_nivel_bolsa')):
        nivel_bolsa_docente = str(row.get('docente_nivel_bolsa'))
        partes.append(f"{nome} tem nível de bolsa no CNPQ: {nivel_bolsa_docente}.")

    if limpo(row.get('docente_area_bolsa')):
        area_bolsa_docente = str(row.get('docente_area_bolsa'))
        partes.append(f"{nome} tem área de bolsa do CNPQ: {area_bolsa_docente}.")

    if limpo(row.get('docente_area_atuacao')):
        area_atuacao_docente = str(row.get('docente_area_atuacao'))
        partes.append(f"{nome} tem área de atuação de pesquisa: {area_atuacao_docente}.")

    especs = [str(e) for e in group['docente_especialidade'].dropna().unique() if limpo(e)]
    if especs:
        partes.append(f"{nome} é tem especialidades de pesquisa: {', '.join(especs)}.")

    especs = group['docente_especialidade'].dropna().unique()
    
    content = " | ".join(partes)
    
    return pd.Series({
        'conteudo': content,
        'departamento_docente': row.get('departamento_docente', 'UFMG'),
    })

# Filtro de campos irrelevantes para não confundir o RAG
def limpo(valor):
    if valor is None:
        return False
    v = str(valor).strip().lower()
    # Retorna True se o valor for útil (NÃO estiver na lista de lixo)
    return v not in ['none', 'desconhecido', 'nan', 'null', '']

if __name__ == "__main__":
    extract_professors()