from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Localizador de Músicas</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: Arial, sans-serif;
      background: #f0f0f0;
      text-align: center;
      padding: 40px 20px;
    }
    .container {
      background: white;
      max-width: 700px;
      margin: auto;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h1 { margin-bottom: 10px; color: #222; }
    p { margin-bottom: 20px; color: #555; }
    input[type="text"] {
      width: 80%;
      max-width: 400px;
      padding: 12px;
      font-size: 16px;
      margin-bottom: 15px;
      border: 1px solid #ccc;
      border-radius: 6px;
    }
    button {
      background: #169656;
      color: white;
      border: none;
      padding: 10px 18px;
      margin: 5px;
      border-radius: 5px;
      cursor: pointer;
      font-size: 15px;
    }
    button:hover { background: #0d6b3c; }
    .resultado {
      text-align: left;
      margin-top: 25px;
      background: #f9f9f9;
      padding: 20px;
      border-radius: 8px;
      white-space: pre-wrap;
      line-height: 1.5;
    }
    a {
      display: inline-block;
      margin-top: 25px;
      color: #169656;
      text-decoration: none;
      font-weight: bold;
    }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🎵 Localizador de Músicas</h1>
    <p>Digite o nome do artista ou banda:</p>

    <form method="POST">
      <input type="text" name="nome" placeholder="Ex: Coldplay, Anitta, Legião Urbana..." value="{{ nome }}" required>
      <br>
      <button type="submit" name="acao" value="artista">Buscar Artista</button>
      <button type="submit" name="acao" value="albuns">Buscar Álbuns</button>
      <button type="submit" name="acao" value="faixas">Buscar Músicas</button>
    </form>

    {% if resultado %}
      <div class="resultado">{{ resultado }}</div>
    {% endif %}

    <a href="/">← Voltar para a página inicial</a>
  </div>
</body>
</html>
"""

def buscar_artista(nome):
    url = f"https://www.theaudiodb.com/api/v1/json/123/search.php?s={nome}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        dados = r.json()
        if dados.get("artists"):
            a = dados["artists"][0]
            bio = a.get("strBiographyPT") or a.get("strBiographyEN", "Sem biografia disponível")
            return (
                f"Nome: {a.get('strArtist', 'N/A')}\n"
                f"Gênero: {a.get('strGenre', 'N/A')}\n"
                f"País: {a.get('strCountry', 'N/A')}\n\n"
                f"Biografia:\n{bio}"
            )
        return "Nenhum artista encontrado."
    except Exception as e:
        return f"Erro na consulta: {e}"

def buscar_albuns(nome):
    url = f"https://www.theaudiodb.com/api/v1/json/123/searchalbum.php?s={nome}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        dados = r.json()
        if dados.get("album"):
            texto = "Álbuns encontrados:\n\n"
            for album in dados["album"]:
                texto += f"• {album.get('strAlbum', 'N/A')} ({album.get('intYearReleased', 'N/A')})\n"
            return texto
        return "Nenhum álbum encontrado."
    except Exception as e:
        return f"Erro na consulta: {e}"

def buscar_faixas(nome):
    url = f"https://www.theaudiodb.com/api/v1/json/123/track-top10.php?s={nome}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        dados = r.json()
        if dados.get("track"):
            texto = "Faixas encontradas (Top 3):\n\n"
            for faixa in dados["track"][:3]:
                texto += (
                    f"• {faixa.get('strTrack', 'N/A')} — {faixa.get('strArtist', 'N/A')}\n"
                    f"  Álbum: {faixa.get('strAlbum', 'N/A')}\n\n"
                )
            return texto
        return "Nenhuma faixa encontrada."
    except Exception as e:
        return f"Erro na consulta: {e}"

@app.route("/")
def home():
    return app.send_static_file("index.html") if False else open("index.html", encoding="utf-8").read()

@app.route("/musicas", methods=["GET", "POST"])
def musicas():
    resultado = ""
    nome = ""
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        acao = request.form.get("acao")
        if nome:
            if acao == "artista":
                resultado = buscar_artista(nome)
            elif acao == "albuns":
                resultado = buscar_albuns(nome)
            elif acao == "faixas":
                resultado = buscar_faixas(nome)
    return render_template_string(HTML, resultado=resultado, nome=nome)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
