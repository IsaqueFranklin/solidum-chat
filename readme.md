# 🏛️ Solidum-Chat

**Solidum-Chat** é uma API de orquestração de chat de alta performance, projetada para servir como o núcleo inteligente do ecossistema Continuum. O sistema utiliza o **LangChain** para gerenciamento de memória e agentes, integrando-se nativamente ao motor de embeddings do **OpenWebUI** para garantir um RAG (Retrieval-Augmented Generation) eficiente e contextual.

## 🚀 Tecnologias
* **Backend:** Python (FastAPI/Flask)
* **Orquestração:** LangChain
* **Embeddings:** OpenWebUI Engine
* **Data Flow:** Conversão de BD para CSV e ingestão via API

## 📂 Estrutura do Projeto

Abaixo, a organização do diretório `src/` e arquivos base:

```text
.
├── src/
│   ├── api/          # Endpoints para conexão com o frontend (Nuxt.js)
│   ├── core/         # Cérebro do projeto: lógica de agentes e chains do LangChain
│   ├── services/     # Funções utilitárias e integrações externas
│   └── scripts/      # ETL: Dump de DB, CSV Tools e Gestão de Embeddings
├── requirements.txt  # Dependências do projeto
└── README.mds