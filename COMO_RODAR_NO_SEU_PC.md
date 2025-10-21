# 🚀 TAXXAT - Como Rodar no Seu Computador (Localmente)

## 📋 Pré-requisitos (Instale Primeiro!)

Antes de começar, você precisa ter instalado no seu computador:

### 1. Python 3.8 ou superior
- **Windows**: Baixe em https://www.python.org/downloads/
- **Mac**: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

Verifique se está instalado:
```bash
python --version
```

### 2. Node.js 16+ e Yarn
- **Node.js**: Baixe em https://nodejs.org/
- **Yarn**: Depois de instalar o Node, execute:
```bash
npm install -g yarn
```

Verifique:
```bash
node --version
yarn --version
```

### 3. MongoDB
- **Windows**: https://www.mongodb.com/try/download/community
- **Mac**: `brew tap mongodb/brew && brew install mongodb-community`
- **Linux**: `sudo apt-get install mongodb`

Inicie o MongoDB:
```bash
# Windows (como serviço, inicia automaticamente)
# Mac
brew services start mongodb-community

# Linux
sudo systemctl start mongodb
```

Verifique se está rodando:
```bash
# Deve aparecer a porta 27017
mongo --eval "db.version()"
```

---

## 📁 Estrutura do Projeto

```
/app/
├── backend/          # Backend Flask (Python)
│   ├── server.py     # Servidor principal
│   ├── requirements.txt
│   ├── .env          # Configurações (IMPORTANTE!)
│   └── uploads/      # Pasta para documentos (criada automaticamente)
│
└── frontend/         # Frontend React
    ├── src/
    ├── package.json
    └── .env          # Configurações frontend (IMPORTANTE!)
```

---

## ⚙️ Configuração dos Arquivos .env

### 1. Backend - `/app/backend/.env`

Crie ou edite o arquivo `.env` no backend:

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=taxxat_database
SECRET_KEY=taxxat_secret_key_2025
GEMINI_API_KEY=sua_chave_gemini_aqui
CORS_ORIGINS=*
```

**⚠️ IMPORTANTE - Chave Gemini:**
- Você precisa de uma chave da API Gemini (Google AI)
- Pegue grátis em: https://makersuite.google.com/app/apikey
- Substitua `sua_chave_gemini_aqui` pela sua chave real

**Sem a chave Gemini, o chatbot NÃO vai funcionar!**

### 2. Frontend - `/app/frontend/.env`

Crie ou edite o arquivo `.env` no frontend:

```env
REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=3000
REACT_APP_ENABLE_VISUAL_EDITS=true
ENABLE_HEALTH_CHECK=false
```

---

## 🔧 Instalação e Execução

### Passo 1: Instalar Dependências do Backend

Abra um terminal e execute:

```bash
# Entre na pasta do backend
cd /app/backend

# Instale as dependências Python
pip install -r requirements.txt
```

**Aguarde alguns minutos** até instalar tudo (Flask, pymongo, google-generativeai, etc.)

### Passo 2: Instalar Dependências do Frontend

Abra **outro terminal** (deixe o anterior aberto) e execute:

```bash
# Entre na pasta do frontend
cd /app/frontend

# Instale as dependências Node.js
yarn install
```

### Passo 3: Iniciar o Backend (Flask)

No terminal do backend, execute:

```bash
cd /app/backend
python server.py
```

**Você deve ver:**
```
WARNING: This is a development server...
 * Running on http://127.0.0.1:8001
 * Running on http://0.0.0.0:8001
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

✅ **Backend rodando na porta 8001!**

### Passo 4: Iniciar o Frontend (React)

No terminal do frontend, execute:

```bash
cd /app/frontend
yarn start
```

**Aguarde compilar e deve abrir automaticamente** no navegador em:
```
http://localhost:3000
```

✅ **Frontend rodando na porta 3000!**

---

## 🧪 Testando se Está Funcionando

### 1. Teste a API Backend

Abra o navegador ou use curl:

```bash
# Teste básico
curl http://localhost:8001/

# Deve retornar:
# {"message": "TAXXAT API - Sistema de IA para Imposto de Renda", "status": "online"}
```

### 2. Teste o Frontend

Abra o navegador em:
```
http://localhost:3000
```

Você deve ver a página do TAXXAT carregando!

### 3. Teste o Chatbot (com Gemini)

```bash
curl -X POST http://localhost:8001/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message":"Quem precisa declarar IR?"}'
```

Se a chave Gemini estiver correta, você receberá uma resposta!

---

## 📡 Endpoints da API Disponíveis

Todos os endpoints funcionam com e sem `/api/` no caminho:

### Autenticação
- `POST /api/auth/register` - Registrar novo usuário
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Dados do usuário logado

### Chatbot
- `POST /api/chatbot/message` - Enviar mensagem para o chatbot
- `GET /api/chatbot/history` - Histórico de conversas

### Documentos
- `POST /api/documents/upload` - Upload de documento
- `GET /api/documents` - Listar documentos do usuário

### Simulação de IR
- `POST /api/simulation/calculate` - Calcular imposto de renda
- `GET /api/simulation/history` - Histórico de simulações

---

## 🐛 Problemas Comuns

### ❌ MongoDB não está rodando
**Erro:** `pymongo.errors.ServerSelectionTimeoutError`

**Solução:**
```bash
# Windows: Inicie o serviço MongoDB nas configurações
# Mac:
brew services start mongodb-community

# Linux:
sudo systemctl start mongodb
```

### ❌ Erro "Module not found: flask"
**Solução:**
```bash
cd /app/backend
pip install -r requirements.txt
```

### ❌ Porta 8001 já está em uso
**Solução:**
```bash
# Linux/Mac
lsof -ti:8001 | xargs kill -9

# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8001).OwningProcess | Stop-Process
```

### ❌ Frontend não conecta no backend
Verifique o arquivo `/app/frontend/.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

### ❌ Chatbot retorna erro
Verifique se você colocou a chave Gemini correta no `/app/backend/.env`:
```env
GEMINI_API_KEY=SUA_CHAVE_AQUI
```

---

## 🌐 Acessar de Outros Dispositivos na Rede Local

Se você quer acessar de outro computador/celular na mesma rede WiFi:

### 1. Descubra seu IP local:

```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
# ou
ip addr show
```

Procure por algo como: `192.168.1.X` ou `10.0.0.X`

### 2. Altere o frontend `.env`:

```env
REACT_APP_BACKEND_URL=http://SEU_IP_LOCAL:8001
# Exemplo:
REACT_APP_BACKEND_URL=http://192.168.1.10:8001
```

### 3. Acesse de outro dispositivo:

```
http://SEU_IP_LOCAL:3000
```

---

## 🛑 Como Parar os Servidores

Para parar os servidores, pressione `CTRL+C` em cada terminal.

---

## 📊 Banco de Dados MongoDB

Os dados são salvos no MongoDB local:
- **Database:** `taxxat_database`
- **Collections:**
  - `usuarios` - Usuários cadastrados
  - `conversacoes` - Histórico do chatbot
  - `documentos` - Documentos enviados
  - `declaracoes` - Simulações de IR

Para visualizar os dados:
```bash
mongo
use taxxat_database
db.usuarios.find()
```

---

## 🎯 Resumo Rápido

```bash
# Terminal 1 - Backend
cd /app/backend
python server.py

# Terminal 2 - Frontend  
cd /app/frontend
yarn start

# Acesse:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8001
```

---

## ✅ Checklist Final

Antes de começar a usar:

- [ ] Python 3.8+ instalado
- [ ] Node.js 16+ e Yarn instalados
- [ ] MongoDB instalado e rodando
- [ ] Chave Gemini configurada no `/app/backend/.env`
- [ ] Backend rodando em `http://localhost:8001`
- [ ] Frontend rodando em `http://localhost:3000`
- [ ] API testada com curl ou navegador

---

## 💡 Próximos Passos

Agora que está tudo funcionando localmente, você pode:

1. **Testar todas as funcionalidades**
2. **Criar sua conta** no sistema
3. **Conversar com o chatbot** sobre Imposto de Renda
4. **Fazer upload de documentos**
5. **Simular seu IR**

---

## 📞 Suporte

Se tiver problemas, verifique:
1. Todos os pré-requisitos estão instalados?
2. MongoDB está rodando?
3. A chave Gemini está correta?
4. Os arquivos `.env` estão configurados corretamente?
5. As portas 3000 e 8001 estão livres?

**Dica:** Sempre verifique os logs no terminal para ver mensagens de erro detalhadas!
