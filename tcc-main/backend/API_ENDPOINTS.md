# TAXXAT API - Documentação de Endpoints

Base URL: `http://192.168.1.8:8001` ou `http://localhost:8001`

## ✅ Endpoints Disponíveis

### 1. Status da API
```bash
GET /api/
```
Resposta: `{"message": "TAXXAT API - Sistema de IA para Imposto de Renda", "status": "online"}`

---

### 2. Autenticação

#### Registrar Usuário
```bash
POST /api/auth/register
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@example.com",
  "senha": "senha123",
  "cpf": "12345678900"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "joao@example.com",
  "senha": "senha123"
}
```

#### Logout
```bash
POST /api/auth/logout
```

#### Obter Usuário Atual
```bash
GET /api/auth/me
```
⚠️ Requer autenticação (sessão)

---

### 3. Chatbot (IA Gemini)

#### Enviar Mensagem
```bash
POST /api/chatbot/message
Content-Type: application/json

{
  "message": "Quem precisa declarar imposto de renda?"
}
```

#### Histórico de Conversas
```bash
GET /api/chatbot/history?limit=20
```

---

### 4. Documentos

#### Upload de Documento
```bash
POST /api/documents/upload
Content-Type: multipart/form-data

file: [arquivo.pdf/jpg/png/txt]
```
⚠️ Requer autenticação

#### Listar Documentos
```bash
GET /api/documents
# ou
GET /api/documents/
```
⚠️ Requer autenticação

---

### 5. Simulação de IR

#### Calcular Imposto
```bash
POST /api/simulation/calculate
Content-Type: application/json

{
  "renda_anual": 50000,
  "deducoes": 5000,
  "dependentes": 1
}
```

#### Histórico de Simulações
```bash
GET /api/simulation/history
```
⚠️ Requer autenticação

---

## 🔧 Testando com cURL

### Exemplo completo de fluxo:

```bash
# 1. Verificar status
curl http://192.168.1.8:8001/api/

# 2. Registrar usuário
curl -X POST http://192.168.1.8:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","email":"teste@test.com","senha":"123456"}'

# 3. Enviar mensagem ao chatbot
curl -X POST http://192.168.1.8:8001/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message":"Como declarar imposto de renda?"}'

# 4. Calcular IR
curl -X POST http://192.168.1.8:8001/api/simulation/calculate \
  -H "Content-Type: application/json" \
  -d '{"renda_anual":50000,"deducoes":5000,"dependentes":1}'

# 5. Listar documentos (sem autenticação - vai retornar 401)
curl http://192.168.1.8:8001/api/documents
```

---

## 📝 Notas Importantes

1. **Endpoints com barra final**: Agora funcionam tanto com `/api/documents` quanto `/api/documents/`

2. **CORS**: Configurado para aceitar requisições de qualquer origem (`*`)

3. **Autenticação**: Endpoints que requerem autenticação usam sessão Flask (cookies)

4. **Sessões**: Para testar endpoints autenticados via cURL, use `-c cookies.txt -b cookies.txt`

5. **Erro 404**: Só ocorre para rotas que realmente não existem

---

## 🎯 Status dos Endpoints

✅ Todos os endpoints estão funcionando corretamente
✅ CORS configurado para aceitar todas as origens
✅ Rotas com e sem barra final funcionando
✅ Gemini AI integrado e funcionando
✅ MongoDB conectado
