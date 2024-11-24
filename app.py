from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa o Flask-CORS
import csv

# Inicializar o Flask
app = Flask(__name__)
CORS(app)  # Habilita o CORS para toda a API

# Carregar o CSV com os dados das cidades
def carregar_cidades_csv(arquivo_csv):
    cidades = []
    with open(arquivo_csv, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            cidades.append({
                "id_municipio": int(row["id_municipio"]),
                "uf": row["uf"],
                "municipio": row["municipio"],
                "longitude": float(row["longitude"]),
                "latitude": float(row["latitude"])
            })
    return cidades

# Carregar os dados das cidades
cidades = carregar_cidades_csv("latitude-longitude-cidades.csv")

# Rota inicial para testar a API
@app.route('/')
def home():
    return jsonify({"message": "API de Cidades do Maranhão está ativa!"})

# Rota para buscar cidade por nome
@app.route('/buscar_cidade', methods=['GET'])
def buscar_cidade():
    nome_cidade = request.args.get('nome')
    if not nome_cidade:
        return jsonify({"error": "Parâmetro 'nome' é obrigatório"}), 400

    # Procurar cidade no CSV carregado
    for cidade in cidades:
        if cidade["municipio"].lower() in nome_cidade.lower():
            return jsonify(cidade)

    return jsonify({"error": "Cidade não encontrada"}), 404

# Rota para listar todas as cidades
@app.route('/listar_cidades', methods=['GET'])
def listar_cidades():
    return jsonify(cidades)

if __name__ == '__main__':
    app.run(debug=True)



# GET http://127.0.0.1:5000/listar_cidades
# GET http://127.0.0.1:5000/buscar_cidade?nome=São Bento
"""
{
    "id_municipio": 1298,
    "latitude": -2.697812,
    "longitude": -44.828927,
    "municipio": "São Bento",
    "uf": "MA"
}
"""

