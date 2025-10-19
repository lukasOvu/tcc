# 🎯 TAXXAT API - Como Usar

## ⚠️ IMPORTANTE: URL Correta

Para acessar a API de `http://192.168.1.8`, você **DEVE** incluir a porta **:8001**

### ❌ ERRADO (retorna 404):
```
http://192.168.1.8/document
http://192.168.1.8/api/documents
```

### ✅ CORRETO:
```
http://192.168.1.8:8001/document
http://192.168.1.8:8001/documents
http://192.168.1.8:8001/api/documents
```

---

## 📋 Rotas Disponíveis (TODAS funcionam com e sem /api/)

### 1. Status da API
```bash
# Qualquer uma dessas funciona:
http://192.168.1.8:8001/
http://192.168.1.8:8001/api/
```

### 2. Documentos
```bash
# Qualquer uma dessas funciona:
http://192.168.1.8:8001/document          ✅
http://192.168.1.8:8001/documents         ✅
http://192.168.1.8:8001/api/documents     ✅
```
⚠️ **Nota:** Retorna `{"error":"Não autenticado"}` (401) porque requer login

### 3. Chatbot
```bash
# POST - Qualquer uma funciona:
http://192.168.1.8:8001/chatbot/message
http://192.168.1.8:8001/api/chatbot/message
```

### 4. Autenticação
```bash
# POST - Registrar
http://192.168.1.8:8001/auth/register
http://192.168.1.8:8001/api/auth/register

# POST - Login
http://192.168.1.8:8001/auth/login
http://192.168.1.8:8001/api/auth/login
```

### 5. Simulação de IR
```bash
# POST - Calcular
http://192.168.1.8:8001/simulation/calculate
http://192.168.1.8:8001/api/simulation/calculate
```

---

## 🧪 Exemplos de Teste com cURL

### Testar Status
```bash
curl http://192.168.1.8:8001/
```

### Testar Documents (vai retornar 401 - normal)
```bash
curl http://192.168.1.8:8001/document
```

### Registrar Usuário
```bash
curl -X POST http://192.168.1.8:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","email":"teste@test.com","senha":"123456"}'
```

### Chatbot
```bash
curl -X POST http://192.168.1.8:8001/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message":"Como declarar IR?"}'
```

### Calcular IR
```bash
curl -X POST http://192.168.1.8:8001/simulation/calculate \
  -H "Content-Type: application/json" \
  -d '{"renda_anual":50000,"deducoes":5000,"dependentes":1}'
```

---

## 🔑 Respostas Esperadas

### ✅ Status 200/201 - Sucesso
```json
{"message": "...", "status": "online"}
```

### ⚠️ Status 401 - Não Autenticado (Normal para rotas protegidas)
```json
{"error": "Não autenticado"}
```

### ❌ Status 404 - Endpoint Não Encontrado
```json
{"error": "Endpoint não encontrado"}
```
**Causa:** Você esqueceu de adicionar `:8001` na URL!

---

## 📱 Testando no Navegador

Se você abrir no navegador Chrome/Firefox:

### ✅ FUNCIONA:
```
http://192.168.1.8:8001/
http://192.168.1.8:8001/document
```

### ❌ NÃO FUNCIONA (404):
```
http://192.168.1.8/document
http://192.168.1.8/api/documents
```

---

## 🔧 Resumo

1. ✅ **Sempre use a porta `:8001`**
2. ✅ `/api/` é **opcional** - funciona com ou sem
3. ✅ `/document` e `/documents` funcionam os dois
4. ✅ Erro 401 ("Não autenticado") é **normal** para rotas protegidas
5. ❌ Erro 404 significa que você **esqueceu a porta :8001**

**URL correta completa:**
```
http://192.168.1.8:8001/document
```
