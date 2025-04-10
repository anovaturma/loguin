from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os

app = Flask(__name__)
CORS(app)

# Ping para manter o Render acordado
@app.route("/ping")
def ping():
    return "Pong!", 200

# Supabase config
url = "https://szbptsuvjmaqkcgsgagx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6YnB0c3V2am1hcWtjZ3NnYWd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQxNjA3MjEsImV4cCI6MjA1OTczNjcyMX0.wqjSCJ8evNog5AnP2dzk1t2nkn31EfvqDuaAkXDiqNo"
supabase: Client = create_client(url, key)

@app.route("/criar-conta", methods=["POST"])
def criar_conta():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"success": False, "message": "Preencha todos os campos."})

    if len(senha) < 6 or not any(not c.isalnum() for c in senha):
        return jsonify({"success": False, "message": "Senha deve ter ao menos 6 caracteres e 1 caractere especial."})

    # Verifica se já existe
    result = supabase.table("cyber").select("*").eq("email", email).execute()
    if result.data:
        return jsonify({"success": False, "message": "Email já cadastrado."})

    # Insere no Supabase
    supabase.table("cyber").insert({"email": email, "senha": senha}).execute()
    return jsonify({"success": True})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"success": False, "message": "Preencha todos os campos."})

    result = supabase.table("cyber").select("*").eq("email", email).eq("senha", senha).execute()
    if result.data:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Email ou senha incorretos."})

@app.route("/")
def home():
    return "Servidor Flask da CyberDigital está rodando!", 200

@app.route("/plataforma")
def plataforma():
    return "<script>window.location.href='https://cyberdigital.com.br';</script>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

