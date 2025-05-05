# Guia de Solução para Problemas de Git e PowerShell

## Problema 1: Navegação para pastas com espaços no PowerShell

Quando você tenta navegar para uma pasta que contém espaços no nome usando o PowerShell, é necessário colocar o caminho entre aspas. Tente os seguintes comandos:

```powershell
# Método 1: Usar aspas duplas
cd "c:\WCD\APP PROGRAMING\FORMULARIOS DE INVITE"

# Método 2: Usar o caractere de escape de acento grave antes de cada espaço
cd c:\WCD\APP` PROGRAMING\FORMULARIOS` DE` INVITE
```

## Problema 2: Git não está instalado

O erro "O termo 'git' não é reconhecido como nome de cmdlet..." indica que o Git não está instalado ou não está no PATH do sistema. Siga estas etapas para instalar o Git:

### Passo 1: Baixar o Git

1. Acesse o site oficial do Git: https://git-scm.com/download/win
2. O download deve iniciar automaticamente para a versão mais recente do Git para Windows
3. Se não iniciar, clique no link para download manual

### Passo 2: Instalar o Git

1. Execute o arquivo baixado (ex: Git-2.40.0-64-bit.exe)
2. Siga as instruções do instalador, aceitando as configurações padrão
3. **Importante**: Na tela "Adjusting your PATH environment", selecione a opção "Git from the command line and also from 3rd-party software"
4. Complete a instalação

### Passo 3: Verificar a instalação

1. Feche e reabra o PowerShell
2. Digite o comando abaixo para verificar se o Git foi instalado corretamente:

```powershell
git --version
```

## Configuração do Git após a instalação

Depois de instalar o Git, você pode seguir os comandos do README.md para configurar seu repositório:

```powershell
# Navegue até a pasta do projeto (use aspas por causa dos espaços)
cd "c:\WCD\APP PROGRAMING\FORMULARIOS DE INVITE"

# Configure seu usuário do Git (substitua com seus dados)
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"

# Inicialize o Git
git init

# Adicione todos os arquivos
git add .

# Faça o commit inicial
git commit -m "Versão inicial do aplicativo"

# Conecte ao repositório GitHub
git remote add origin https://github.com/wash1494/Portifolio_treinamento.git

# Envie o código para o GitHub
git push -u origin master
```

## Observações importantes

1. Você precisará ter uma conta no GitHub e ter criado o repositório "Portifolio_treinamento" antes de executar estes comandos
2. Na primeira vez que usar o comando `git push`, o Git solicitará suas credenciais do GitHub
3. Se estiver usando autenticação de dois fatores no GitHub, você precisará criar um token de acesso pessoal em vez de usar sua senha

Espero que este guia ajude a resolver seus problemas! Se tiver mais dúvidas, não hesite em perguntar.