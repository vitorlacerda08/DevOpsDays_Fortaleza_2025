# DevOpsDay Fortaleza 2025 - Chat Demo

## Sobre o Projeto
Este projeto é uma demonstração apresentada no DevOpsDay Fortaleza 2025, implementando um chatbot utilizando LiteLLM para gerenciamento de modelos de linguagem e Langfuse para observabilidade.

## Pré-requisitos

Para executar este projeto, você precisará ter instalado:
- Docker e Docker Compose
- Python 3.8+
- pip

## Estrutura do Projeto
```
devopsday-fortaleza-2025/
├── OpenAI_Assistent_Chat/
│   └── chat-litellm-app/
│       ├── ChatLiteLLM.py
│       └── key.py
├── liteLLM/
│   └── docker-compose.yml
├── Langfuse/
│   └── docker-compose.yml
├── README.md
└── requirements.txt
```

## Configuração do Ambiente

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/devopsday-fortaleza-2025.git
cd devopsday-fortaleza-2025
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o LiteLLM:
```bash
cd liteLLM
docker-compose up -d
```

4. Configure o Langfuse:
```bash
cd ../Langfuse
docker-compose up -d
```

## Configuração das Chaves de API

1. LiteLLM:
   - Acesse http://localhost:4000
   - Configure o modelo desejado e guarde o APIKEY gerado

2. Langfuse:
   - Acesse http://localhost:3000
   - Crie uma nova conta e gere as chaves de API (secret_key e public_key)

## Executando o Chat

```bash
cd devopsday-fortaleza-2025
python OpenAI_Assistent_Chat/chat-litellm-app/ChatLiteLLM.py
```

## Contribuindo
Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter um Pull Request.