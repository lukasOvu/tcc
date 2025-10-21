# 🧪 Exemplos de Uso da API TAXXAT

## 🌐 URLs Base

- **Produção (online):** A URL está no `.env` do backend
- **Local:** `http://localhost:8001`

Todos os exemplos abaixo usam `localhost:8001`. Ajuste conforme necessário.

---

## 1️⃣ Testar se a API está Online

```bash
curl http://localhost:8001/
```

**Resposta esperada:**
```json
{
  "message": "TAXXAT API - Sistema de IA para Imposto de Renda",
  "status": "online"
}
```

---

## 2️⃣ Autenticação

### Registrar Novo Usuário

```bash
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@email.com",
    "senha": "senha123",
    "cpf": "123.456.789-00"
  }'
```

**Resposta esperada:**
```json
{
  "message": "Cadastro realizado com sucesso!",
  "user": {
    "id": "uuid-gerado",
    "nome": "João Silva",
    "email": "joao@email.com"
  }
}
```

### Login

```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "joao@email.com",
    "senha": "senha123"
  }'
```

**Resposta esperada:**
```json
{
  "message": "Login realizado com sucesso!",
  "user": {
    "id": "uuid-do-usuario",
    "nome": "João Silva",
    "email": "joao@email.com"
  }
}
```

**Nota:** O `-c cookies.txt` salva a sessão. Use `-b cookies.txt` nas próximas requisições autenticadas.

### Obter Dados do Usuário Logado

```bash
curl -X GET http://localhost:8001/api/auth/me \
  -b cookies.txt
```

### Logout

```bash
curl -X POST http://localhost:8001/api/auth/logout \
  -b cookies.txt
```

---

## 3️⃣ Chatbot (IA com Gemini)

### Enviar Mensagem ao Chatbot

```bash
curl -X POST http://localhost:8001/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quem precisa declarar Imposto de Renda em 2025?"
  }'
```

**Resposta esperada:**
```json
{
  "message": "No Brasil, estão obrigadas a declarar o IR em 2025 as pessoas que...",
  "timestamp": "2025-10-21T00:00:00"
}
```

### Mais Exemplos de Perguntas:

```bash
# Prazos
curl -X POST http://localhost:8001/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual o prazo para declarar o IR?"}'

# Deduções
curl -X POST http://localhost:8001/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Quais despesas posso deduzir do IR?"}'

# Restituição
curl -X POST http://localhost:8001/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Como funciona a restituição do IR?"}'
```

### Histórico de Conversas

```bash
curl -X GET http://localhost:8001/api/chatbot/history \
  -b cookies.txt
```

---

## 4️⃣ Upload de Documentos

### Fazer Upload de um Documento

```bash
# Criar um arquivo de exemplo
echo "Comprovante de Renda - R$ 5000/mês" > comprovante.txt

# Upload
curl -X POST http://localhost:8001/api/documents/upload \
  -b cookies.txt \
  -F "file=@comprovante.txt"
```

**Resposta esperada:**
```json
{
  "message": "Documento enviado com sucesso!",
  "document": {
    "id": "uuid-do-documento",
    "filename": "comprovante.txt",
    "upload_date": "2025-10-21T00:00:00",
    "analysis": "Este documento parece ser um comprovante de renda..."
  }
}
```

### Tipos de Arquivos Permitidos:
- `.pdf`
- `.png`, `.jpg`, `.jpeg`
- `.txt`

### Listar Documentos do Usuário

```bash
curl -X GET http://localhost:8001/api/documents \
  -b cookies.txt
```

**Resposta esperada:**
```json
{
  "documents": [
    {
      "id": "uuid",
      "user_id": "user-uuid",
      "original_filename": "comprovante.txt",
      "upload_date": "2025-10-21T00:00:00",
      "status": "uploaded"
    }
  ]
}
```

---

## 5️⃣ Simulação de Imposto de Renda

### Calcular IR

```bash
curl -X POST http://localhost:8001/api/simulation/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "renda_anual": 60000,
    "deducoes": 8000,
    "dependentes": 2
  }'
```

**Resposta esperada:**
```json
{
  "resultado": {
    "renda_anual": 60000.0,
    "deducoes": 8000.0,
    "dependentes": 2,
    "base_calculo": 37398.08,
    "aliquota": 15.0,
    "imposto_devido": 1340.35
  }
}
```

### Exemplos de Simulações:

#### Renda Baixa (Isento)
```bash
curl -X POST http://localhost:8001/api/simulation/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "renda_anual": 20000,
    "deducoes": 2000,
    "dependentes": 0
  }'
```

#### Renda Alta
```bash
curl -X POST http://localhost:8001/api/simulation/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "renda_anual": 150000,
    "deducoes": 15000,
    "dependentes": 1
  }'
```

### Histórico de Simulações

```bash
curl -X GET http://localhost:8001/api/simulation/history \
  -b cookies.txt
```

---

## 📊 Tabela Progressiva do IR (2025)

| Base de Cálculo (R$)      | Alíquota | Dedução (R$) |
|---------------------------|----------|--------------|
| Até 22.847,76             | Isento   | 0            |
| 22.847,77 a 33.919,80     | 7,5%     | 1.713,58     |
| 33.919,81 a 45.012,60     | 15%      | 4.257,57     |
| 45.012,61 a 55.976,16     | 22,5%    | 7.633,51     |
| Acima de 55.976,16        | 27,5%    | 10.432,32    |

**Dedução por dependente:** R$ 2.275,08/mês (R$ 27.300,96/ano)

---

## 🧪 Script de Teste Completo

Salve isso como `teste_api.sh` e execute: `bash teste_api.sh`

```bash
#!/bin/bash

echo "=== 1. Testando Status da API ==="
curl http://localhost:8001/
echo -e "\n"

echo "=== 2. Registrando Usuário ==="
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste User",
    "email": "teste@teste.com",
    "senha": "senha123"
  }'
echo -e "\n"

echo "=== 3. Fazendo Login ==="
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "teste@teste.com",
    "senha": "senha123"
  }'
echo -e "\n"

echo "=== 4. Testando Chatbot ==="
curl -X POST http://localhost:8001/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Como declarar IR?"
  }'
echo -e "\n"

echo "=== 5. Calculando IR ==="
curl -X POST http://localhost:8001/api/simulation/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "renda_anual": 50000,
    "deducoes": 5000,
    "dependentes": 1
  }'
echo -e "\n"

echo "=== 6. Listando Documentos ==="
curl -X GET http://localhost:8001/api/documents \
  -b cookies.txt
echo -e "\n"

echo "=== Testes Concluídos! ==="
```

---

## 🐍 Script Python de Teste

```python
import requests
import json

BASE_URL = "http://localhost:8001"
session = requests.Session()

# 1. Testar status
print("=== 1. Status da API ===")
response = session.get(f"{BASE_URL}/")
print(json.dumps(response.json(), indent=2))

# 2. Registrar usuário
print("\n=== 2. Registrar Usuário ===")
response = session.post(f"{BASE_URL}/api/auth/register", json={
    "nome": "Python User",
    "email": "python@test.com",
    "senha": "python123"
})
print(json.dumps(response.json(), indent=2))

# 3. Login
print("\n=== 3. Login ===")
response = session.post(f"{BASE_URL}/api/auth/login", json={
    "email": "python@test.com",
    "senha": "python123"
})
print(json.dumps(response.json(), indent=2))

# 4. Chatbot
print("\n=== 4. Chatbot ===")
response = session.post(f"{BASE_URL}/api/chatbot/message", json={
    "message": "Quais documentos preciso para declarar IR?"
})
print(json.dumps(response.json(), indent=2))

# 5. Calcular IR
print("\n=== 5. Calcular IR ===")
response = session.post(f"{BASE_URL}/api/simulation/calculate", json={
    "renda_anual": 80000,
    "deducoes": 10000,
    "dependentes": 2
})
print(json.dumps(response.json(), indent=2))

print("\n=== Testes Concluídos! ===")
```

---

## ⚠️ Notas Importantes

1. **Autenticação:** Rotas protegidas (`/documents`, `/simulation/history`) requerem login
2. **Sessão:** Use cookies (`-c` e `-b` no curl) para manter a sessão
3. **Gemini API:** O chatbot só funciona com uma chave válida
4. **CORS:** Está configurado para aceitar todas as origens (`*`)
5. **Porta:** Sempre use `:8001` quando acessar localmente

---

## 🔍 Verificar Dados no MongoDB

```bash
# Entrar no MongoDB
mongo

# Selecionar database
use taxxat_database

# Ver usuários
db.usuarios.find().pretty()

# Ver conversas do chatbot
db.conversacoes.find().pretty()

# Ver documentos
db.documentos.find().pretty()

# Ver simulações
db.declaracoes.find().pretty()
```

---

## 📞 Troubleshooting

### Erro 404 - Not Found
✅ Verifique se incluiu a porta `:8001`

### Erro 401 - Não autenticado  
✅ Faça login primeiro e use cookies

### Erro 500 - Internal Server Error
✅ Verifique os logs do servidor no terminal
✅ Verifique se MongoDB está rodando
✅ Verifique se a chave Gemini está correta

### Chatbot não responde
✅ Verifique a chave GEMINI_API_KEY no `.env`
✅ Veja os logs do backend para erros da API Gemini
