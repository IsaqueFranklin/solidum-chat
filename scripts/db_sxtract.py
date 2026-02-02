import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"))

def extract_professors():
    query = text("SELECT id_docente, nome_docente, departamento_docente, unidade_docente, docente_area_the, docente_area, docente_grande_area, docente_grande_area, docente_colegio_capes, docente_nivel_bolsa, docente_area_bolsa, docente_area_atuacao, docente_especialidade FROM docente_geral")
        
    with engine.connect() as connection:
        # O Pandas lê o resultado da consulta SQL diretamente em um DataFrame
        df = pd.read_sql_query(query, connection)

    # Criando o cerébro do RAG
    # Ao invés de colunas soltas, conectamos tudo em uma única coluna de texto
    df['conteudo_ia'] = df.apply(lambda row: 
        f"Professor(a): {row['nome_docente']}, do departamento de {row['departamento_docente']}, da unidade {row['unidade_docente']}." +
        f" Atua na área de {row['docente_area_the']} e pesquisa sobre {row['docente_area']}." +
        f" Pertence à grande área de {row['docente_grande_area']} e ao colégio acadêmico {row['docente_colegio_capes']}." +
        f" Nível de bolsa no CNPQ: {row['docente_nivel_bolsa']}, área de bolsa do CNPQ: {row['docente_area_bolsa']}." +
        f" Área de atuação de pesquisa: {row['docente_area_atuacao']} e especialidade: {row['docente_especialidade']}.",
        axis=1                          
    )

    # Dessa forma definimos as colunas finais, onde o conteudo_ia serão os embeddings e o restante metadados
    final_columns = ['conteudo_ia', 'departamento_docente', 'id_docente', 'docente_especialidade']

    # Salvamos apenas a coluna formatada para o OpenWebUI
    df[final_columns].to_csv('professores_rag.csv', index=False, header=False)
    print("Arquivo #professores gerado com sucesso!")

if __name__ == "__main__":
    extract_professors()