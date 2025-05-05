# Guia de Deploy no Streamlit Cloud

Este guia explica como fazer o deploy da aplicação de Portfólio de Treinamentos no Streamlit Cloud.

## Pré-requisitos

1. Uma conta no [GitHub](https://github.com/)
2. Uma conta no [Streamlit Cloud](https://streamlit.io/cloud)

## Passo a Passo

### 1. Preparar o Repositório no GitHub

1. Crie um novo repositório no GitHub ou use um existente
2. Certifique-se de que os seguintes arquivos estejam no repositório:
   - `INVITES_DEPLOY_ENHANCE.py` (arquivo principal da aplicação)
   - `requirements.txt` (dependências)
   - `.streamlit/config.toml` (configurações do Streamlit)
   - `.streamlit/secrets.toml` (senhas e configurações sensíveis)
   - `README.md` (documentação)
   - Pasta `images` com a imagem padrão `default_course.png`

### 2. Configurar o Streamlit Cloud

1. Acesse [Streamlit Cloud](https://streamlit.io/cloud) e faça login
2. Clique em "New app"
3. Conecte sua conta do GitHub se ainda não estiver conectada
4. Selecione o repositório onde está o código da aplicação
5. Configure os seguintes campos:
   - **Repository**: Seu repositório no GitHub
   - **Branch**: main (ou a branch que contém o código)
   - **Main file path**: `INVITES_DEPLOY_ENHANCE.py`
   - **App URL**: Escolha um nome para a URL da aplicação

### 3. Configurar Secrets

As senhas estão configuradas no arquivo `.streamlit/secrets.toml`, mas para o deploy no Streamlit Cloud, você precisa configurá-las no painel de controle:

1. Na página do seu app no Streamlit Cloud, clique em "Settings" (ícone de engrenagem)
2. Vá para a seção "Secrets"
3. Adicione o seguinte conteúdo:

```toml
[passwords]
library = "IDG2025"
admin = "ADMINIDG2025"
```

4. Clique em "Save"

### 4. Gerenciamento de Arquivos

O Streamlit Cloud tem um sistema de arquivos efêmero, o que significa que os arquivos criados durante a execução da aplicação (como os bancos de dados Excel) não são persistentes entre reinicializações. Para resolver isso, você tem algumas opções:

#### Opção 1: Usar o GitHub para armazenar os dados iniciais

1. Inclua os arquivos `courses.xlsx` e `registrations.xlsx` vazios no repositório
2. A aplicação irá inicializá-los se não existirem

#### Opção 2: Usar um serviço de armazenamento externo

Para uma solução mais robusta, considere usar:

- Google Drive ou Dropbox para armazenar os arquivos Excel
- Um banco de dados como MongoDB Atlas ou PostgreSQL

### 5. Deploy

1. Após configurar tudo, clique em "Deploy!"
2. Aguarde o processo de build e deploy (pode levar alguns minutos)
3. Quando concluído, você receberá uma URL para acessar sua aplicação

## Solução de Problemas

### Arquivos não são salvos

Se os arquivos Excel não estiverem sendo salvos corretamente:

1. Verifique se os caminhos dos arquivos são relativos (como já configurado no código)
2. Considere implementar uma das opções de armazenamento externo mencionadas acima

### Erros de Dependências

Se ocorrerem erros relacionados a dependências:

1. Verifique se todas as bibliotecas necessárias estão listadas no `requirements.txt`
2. Certifique-se de especificar as versões exatas das bibliotecas

## Manutenção

Para atualizar a aplicação após o deploy:

1. Faça as alterações no código
2. Envie as alterações para o GitHub
3. O Streamlit Cloud detectará as alterações e fará o redeploy automaticamente

## Recursos Adicionais

- [Documentação do Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud)
- [Gerenciamento de Secrets no Streamlit](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)