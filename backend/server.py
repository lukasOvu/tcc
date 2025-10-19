from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from datetime import datetime, timedelta
import google.generativeai as genai
import os
from dotenv import load_dotenv
import uuid
from pathlib import Path
import traceback

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'taxxat_secret_key_2025')

# CORS Configuration - Allow all origins for development
CORS(app,
     supports_credentials=True,
     origins="*",
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# MongoDB Configuration
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'taxxat_database')
client = MongoClient(mongo_url)
db = client[db_name]

# Collections
users_collection = db.usuarios
conversations_collection = db.conversacoes
documents_collection = db.documentos
declarations_collection = db.declaracoes

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Upload folder configuration
UPLOAD_FOLDER = ROOT_DIR / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'txt'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== ROUTES ====================


@app.route('/', methods=['GET'])
@app.route('/api/', methods=['GET'])
@app.route('/api', methods=['GET'])
def home():
    return jsonify({"message": "TAXXAT API - Sistema de IA para Imposto de Renda", "status": "online"})

# ==================== AUTENTICAÇÃO ====================


@app.route('/auth/register', methods=['POST'])
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        cpf = data.get('cpf', '')

        if not nome or not email or not senha:
            return jsonify({"error": "Todos os campos são obrigatórios"}), 400

        # Check if user already exists
        if users_collection.find_one({"email": email}):
            return jsonify({"error": "Email já cadastrado"}), 409

        # Hash password
        senha_hash = generate_password_hash(senha)

        # Create user
        user = {
            "id": str(uuid.uuid4()),
            "nome": nome,
            "email": email,
            "senha": senha_hash,
            "cpf": cpf,
            "data_cadastro": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow()
        }

        users_collection.insert_one(user)

        return jsonify({
            "message": "Cadastro realizado com sucesso!",
            "user": {
                "id": user["id"],
                "nome": nome,
                "email": email
            }
        }), 201

    except Exception as e:
        print(f"Error in register: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Erro ao realizar cadastro"}), 500


@app.route('/auth/login', methods=['POST'])
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

        if not email or not senha:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400

        # Find user
        user = users_collection.find_one({"email": email})

        if not user or not check_password_hash(user['senha'], senha):
            return jsonify({"error": "Email ou senha incorretos"}), 401

        # Create session
        session['user_id'] = user['id']
        session['user_email'] = user['email']

        return jsonify({
            "message": "Login realizado com sucesso!",
            "user": {
                "id": user['id'],
                "nome": user['nome'],
                "email": user['email']
            }
        }), 200

    except Exception as e:
        print(f"Error in login: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Erro ao realizar login"}), 500


@app.route('/auth/logout', methods=['POST'])
@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logout realizado com sucesso!"}), 200


@app.route('/auth/me', methods=['GET'])
@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "Não autenticado"}), 401

    user = users_collection.find_one({"id": user_id}, {"_id": 0, "senha": 0})

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify({"user": user}), 200

# ==================== CHATBOT ====================


@app.route('/chatbot/message', methods=['POST'])
@app.route('/api/chatbot/message', methods=['POST'])
def chatbot_message():
    try:
        data = request.get_json()
        user_message = data.get('message')
        user_id = session.get('user_id', 'guest')

        if not user_message:
            return jsonify({"error": "Mensagem não pode estar vazia"}), 400

        # Create context for IR chatbot
        context = """Você é TAXXAT, um assistente virtual especializado em Imposto de Renda brasileiro.
        Seu papel é ajudar as pessoas a entenderem melhor sobre declaração de IR, responder dúvidas sobre:
        - Quem precisa declarar IR
        - Prazos e documentos necessários
        - Deduções permitidas
        - Como declarar diferentes tipos de renda
        - Restituição e impostos a pagar
        
        Sempre seja educado, claro e objetivo. Se não souber algo com certeza, indique que a pessoa deve consultar a Receita Federal ou um contador.
        """

        # Generate response with Gemini
        prompt = f"{context}\n\nPergunta do usuário: {user_message}\n\nResposta:"
        response = model.generate_content(prompt)
        bot_response = response.text

        # Save conversation
        conversation = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow()
        }
        conversations_collection.insert_one(conversation)

        return jsonify({
            "message": bot_response,
            "timestamp": conversation["timestamp"]
        }), 200

    except Exception as e:
        print(f"Error in chatbot: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "error": "Erro ao processar mensagem",
            "message": "Desculpe, tive um problema ao processar sua pergunta. Tente novamente."
        }), 500


@app.route('/chatbot/history', methods=['GET'])
@app.route('/api/chatbot/history', methods=['GET'])
def get_chat_history():
    try:
        user_id = session.get('user_id', 'guest')
        limit = request.args.get('limit', 20, type=int)

        conversations = list(conversations_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("created_at", -1).limit(limit))

        return jsonify({"conversations": conversations}), 200

    except Exception as e:
        print(f"Error in get_chat_history: {str(e)}")
        return jsonify({"error": "Erro ao buscar histórico"}), 500

# ==================== DOCUMENTOS ====================


@app.route('/api/documents/upload', methods=['POST'])
def upload_document():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Não autenticado"}), 401

        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "Nenhum arquivo selecionado"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = UPLOAD_FOLDER / unique_filename
            file.save(str(filepath))

            # Save document info to database
            document = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "original_filename": filename,
                "stored_filename": unique_filename,
                "filepath": str(filepath),
                "upload_date": datetime.utcnow().isoformat(),
                "status": "uploaded",
                "created_at": datetime.utcnow()
            }
            documents_collection.insert_one(document)

            # Analyze document with Gemini (basic analysis)
            analysis_prompt = f"""Analise este documento relacionado a Imposto de Renda.
            Nome do arquivo: {filename}
            
            Por favor, identifique que tipo de documento pode ser (recibo, comprovante de renda, despesa médica, etc.) 
            e extraia informações relevantes se possível."""

            try:
                analysis_response = model.generate_content(analysis_prompt)
                analysis = analysis_response.text
            except:
                analysis = "Documento recebido. Análise detalhada em desenvolvimento."

            return jsonify({
                "message": "Documento enviado com sucesso!",
                "document": {
                    "id": document["id"],
                    "filename": filename,
                    "upload_date": document["upload_date"],
                    "analysis": analysis
                }
            }), 201

        return jsonify({"error": "Tipo de arquivo não permitido"}), 400

    except Exception as e:
        print(f"Error in upload_document: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Erro ao fazer upload do documento"}), 500


@app.route('/api/documents', methods=['GET'])
@app.route('/api/documents/', methods=['GET'])
def get_documents():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Não autenticado"}), 401

        documents = list(documents_collection.find(
            {"user_id": user_id},
            {"_id": 0, "filepath": 0}
        ).sort("created_at", -1))

        return jsonify({"documents": documents}), 200

    except Exception as e:
        print(f"Error in get_documents: {str(e)}")
        return jsonify({"error": "Erro ao buscar documentos"}), 500

# ==================== SIMULAÇÃO DE IR ====================


@app.route('/api/simulation/calculate', methods=['POST'])
def calculate_ir():
    try:
        user_id = session.get('user_id')
        data = request.get_json()

        renda_anual = float(data.get('renda_anual', 0))
        deducoes = float(data.get('deducoes', 0))
        dependentes = int(data.get('dependentes', 0))

        # Tabela progressiva 2025 (simplificada)
        base_calculo = renda_anual - deducoes - (dependentes * 2275.08 * 12)

        if base_calculo <= 0:
            imposto_devido = 0
            aliquota = 0
        elif base_calculo <= 22847.76:
            imposto_devido = 0
            aliquota = 0
        elif base_calculo <= 33919.80:
            imposto_devido = (base_calculo * 0.075) - 1713.58
            aliquota = 7.5
        elif base_calculo <= 45012.60:
            imposto_devido = (base_calculo * 0.15) - 4257.57
            aliquota = 15
        elif base_calculo <= 55976.16:
            imposto_devido = (base_calculo * 0.225) - 7633.51
            aliquota = 22.5
        else:
            imposto_devido = (base_calculo * 0.275) - 10432.32
            aliquota = 27.5

        resultado = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "renda_anual": renda_anual,
            "deducoes": deducoes,
            "dependentes": dependentes,
            "base_calculo": round(base_calculo, 2),
            "aliquota": aliquota,
            "imposto_devido": round(max(0, imposto_devido), 2),
            "data_simulacao": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow()
        }

        # Save simulation
        if user_id:
            declarations_collection.insert_one(resultado)

        return jsonify({
            "resultado": {
                "renda_anual": resultado["renda_anual"],
                "deducoes": resultado["deducoes"],
                "dependentes": resultado["dependentes"],
                "base_calculo": resultado["base_calculo"],
                "aliquota": resultado["aliquota"],
                "imposto_devido": resultado["imposto_devido"]
            }
        }), 200

    except Exception as e:
        print(f"Error in calculate_ir: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Erro ao calcular imposto"}), 500


@app.route('/api/simulation/history', methods=['GET'])
def get_simulation_history():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Não autenticado"}), 401

        simulations = list(declarations_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("created_at", -1).limit(10))

        return jsonify({"simulations": simulations}), 200

    except Exception as e:
        print(f"Error in get_simulation_history: {str(e)}")
        return jsonify({"error": "Erro ao buscar histórico"}), 500

# ==================== ERROR HANDLERS ====================


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint não encontrado"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Erro interno do servidor"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)

# ASGI wrapper for uvicorn compatibility
from asgiref.wsgi import WsgiToAsgi
app = WsgiToAsgi(app)