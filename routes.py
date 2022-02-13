from flask import Flask, request
from scraper import scrape

app = Flask("Letras")


@app.route('/letras', methods=["GET"])
def consultar_letra():
    titulo = request.args.get('titulo')
    artista = request.args.get('artista')

    if not titulo:
        return {'erro': 'o campo titulo é obrigatório'}, 400

    letra = scrape(titulo, artista)

    if not letra:
        return {'erro': 'letra não localizada'}, 400

    return letra


app.run(
    debug=True
)