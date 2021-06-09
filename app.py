from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dados'

db = SQLAlchemy(app)

# CREATE TABLE/JSON

class dado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dado = db.Column(db.VARCHAR(255))

    def to_json(self):
        return{"id": self.id, "dado": self.dado}

# READ DATABASE DATA

@app.route("/dados", methods=['GET'])
def seleciona_dado():
    dados_objetos = dado.query.all()
    dados_json = [dado.to_json() for dado in dados_objetos]
    print(dados_json)

    return gResponse(200, "dados", dados_json);

    app.run()

def gResponse(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

# CADASTRAR

@app.route("/dados", methods=['POST'])
def registerData():
    body = request.get_json()
    try:
        dados = dado(id = body["id"], dado = body["dado"])
        db.session.add(dados)
        db.session.commit()
        return gResponse(201, "dados", dados.to_json(), "Realizado inserção de dado!")
    except Exception as e:
        print('Erro', e)
        return gResponse(400, "dados", {}, "Erro ao realizar nova inserção")

# UPDATE

@app.route("/dados/<id>", methods=['PUT'])
def updateData(id):
    dados_objeto = dado.query.filter_by(id = id).first()
    body = request.get_json()

    try:
        dados_objeto.dado = body['dado']

        db.session.add(dados_objeto)
        db.session.commit()
        return gResponse(200, "dados", dados_objeto.to_json(), "Informação atualizada!")
    except Exception as e:
        print('Erro', e)
        return gResponse(400, "dados", {}, "Erro durante atualização de informação.")

# DELETE

@app.route("/dados/<id>", methods=["DELETE"])
def deleteData(id):
    dados_objeto = dado.query.filter_by(id = id).first()
    
    try:
        db.session.delete(dados_objeto)
        db.session.commit()
        return gResponse(200, "dados", dados_objeto.to_json(), "Informação deletada!")
    except Exception as e:
        print('Erro', e)
        return gResponse(400,"dados", {}, "Erro ao deletar informação") 