
print("Iniciando o Reclass...")

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensagem": "API do Reclass funcionando!",
        "status": "ok"
    })


if __name__ == "__main__":
    print("Preparando servidor Flask...")
    app.run(host="127.0.0.1", port=5000, debug=False)