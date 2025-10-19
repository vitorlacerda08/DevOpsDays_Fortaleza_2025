"""
ChatLiteLLM - Uma interface de chat simples usando LiteLLM proxy e Langfuse para observabilidade

Este script implementa uma interface de chat em linha de comando que utiliza o LiteLLM proxy
para comunicação com modelos de linguagem e Langfuse para monitoramento e observabilidade.

Dependências:
    - requests: Para fazer requisições HTTP ao LiteLLM proxy
    - urllib3: Para tratamento de funcionalidades HTTP
    - langfuse: Para observabilidade e monitoramento
"""
import os
import requests
import urllib3
from langfuse import Langfuse, observe

# Desabilita mensagens de aviso SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ----------------------------
# Configurações de Conexão
# ----------------------------
# Recomenda-se definir essas variáveis via variáveis de ambiente (ex.: .env) em vez de hardcode.
# Exemplos de nomes de variáveis de ambiente:
#   LITELLM_API_URL         -> URL do proxy LiteLLM (ex.: http://localhost:4000/v1/chat/completions)
#   LITELLM_API_KEY         -> Chave de autenticação do LiteLLM (Bearer token)
#   LITELLM_MODEL           -> Nome do modelo a ser usado (ex.: gpt-4.1-mini)
#   LANGFUSE_SECRET_KEY     -> Langfuse secret key
#   LANGFUSE_PUBLIC_KEY     -> Langfuse public key
#   LANGFUSE_HOST           -> Host do Langfuse (ex.: http://localhost:3000)

# LiteLLM (valores padrão exemplo — ajuste em produção)
APIGATEWAY = os.getenv("LITELLM_API_URL", "http://localhost:4000/v1/chat/completions")
APIKEY = os.getenv("LITELLM_API_KEY", "replace-with-your-litellm-api-key")
MODEL = os.getenv("LITELLM_MODEL", "gpt-4.1-mini")

# Langfuse (valores padrão exemplo)
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "replace-with-langfuse-secret")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "replace-with-langfuse-public")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "http://localhost:3000")

# Inicialização do Langfuse para observabilidade
langfuse = Langfuse(
    secret_key=LANGFUSE_SECRET_KEY,
    public_key=LANGFUSE_PUBLIC_KEY,
    host=LANGFUSE_HOST
)

@observe(name="llm-call", as_type="generation")
def query_llm(messages, proxy_url, api_key, model):
    """
    Envia uma consulta ao modelo de linguagem através do LiteLLM proxy.

    Argumentos:
        messages (list): Lista de dicionários contendo o histórico da conversa
        proxy_url (str): URL do LiteLLM proxy
        api_key (str): Chave de autenticação para a API
        model (str): Nome do modelo de linguagem a ser usado

    Retorna:
        dict: Resposta JSON da API se bem-sucedido, None caso contrário
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    
    payload = {
        'model': model,
        'messages': messages,
        'max_tokens': 1000,
        'temperature': 0.7,
    }

    try:
        response = requests.post(proxy_url, headers=headers, json=payload, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

if __name__ == "__main__":
    """
    Loop principal do chat que gerencia a interação do usuário com o chatbot.
    Os usuários podem digitar 'sair' para encerrar o chat.
    """
    proxy_url = APIGATEWAY
    api_key = APIKEY
    model = MODEL
    print("Bem-vindo ao ChatBot! Digite 'sair' para encerrar.\n")
    messages = []

    while True:
        # Obtém entrada do usuário
        user_input = input("Você: ")
        if user_input.strip().lower() == "sair":
            print("Encerrando o chat.")
            break

        # Adiciona mensagem do usuário ao histórico da conversa
        messages.append({"role": "user", "content": user_input})
        
        # Obtém resposta do modelo de linguagem
        resposta = query_llm(messages, proxy_url, api_key, model)

        if resposta:
            try:
                # Extrai e exibe a resposta do modelo
                content = resposta["choices"][0]["message"]["content"]
                print("Bot:", content)
                # Adiciona resposta do bot ao histórico da conversa
                messages.append({"role": "assistant", "content": content})
            except (KeyError, IndexError):
                print("Não foi possível extrair a resposta do modelo:", resposta)
        else:
            print("Erro ao obter resposta do modelo.")
