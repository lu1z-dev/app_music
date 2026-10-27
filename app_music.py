import requests

def buscar_artista(nome):
    url = f"https://www.theaudiodb.com/api/v1/json/123/search.php?s={nome}"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
    except Exception as e:
        print(f"Erro na consulta: {e}")
        return

    if dados.get("artists"):
        artista = dados["artists"][0]
        nome_artista = artista.get("strArtist", "N/A")
        genero = artista.get("strGenre", "N/A")
        pais = artista.get("strCountry", "N/A")
        bio = artista.get("strBiographyPT") or artista.get("strBiographyEN", "Sem biografia disponível")

        print("\n" + "="*50)
        print(f"Nome: {nome_artista}")
        print(f"Gênero: {genero}")
        print(f"País: {pais}")
        print(f"\nBiografia:\n{bio}")
        print("="*50)
    else:
        print("\nNenhum artista encontrado.")


def buscar_albuns(nome):
    url = f"https://www.theaudiodb.com/api/v1/json/123/searchalbum.php?s={nome}"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
    except Exception as e:
        print(f"Erro na consulta: {e}")
        return

    if dados.get("album"):
        print("\n" + "="*50)
        print("Álbuns encontrados:\n")
        for album in dados["album"]:
            nome_album = album.get("strAlbum", "N/A")
            ano = album.get("intYearReleased", "N/A")
            print(f"• {nome_album} ({ano})")
        print("="*50)
    else:
        print("\nNenhum álbum encontrado.")


def buscar_faixas(nome):
    url = f"https://www.theaudiodb.com/api/v1/json/123/track-top10.php?s={nome}"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
    except Exception as e:
        print(f"Erro na consulta: {e}")
        return

    if dados.get("track"):
        print("\n" + "="*50)
        print("Faixas encontradas (Top 3):\n")
        for faixa in dados["track"][:3]:
            nome_faixa = faixa.get("strTrack", "N/A")
            artista = faixa.get("strArtist", "N/A")
            album = faixa.get("strAlbum", "N/A")
            print(f"• {nome_faixa} — {artista}")
            print(f"  Álbum: {album}\n")
        print("="*50)
    else:
        print("\nNenhuma faixa encontrada.")


# ====================== PROGRAMA PRINCIPAL ======================

print("="*50)
print("       LOCALIZADOR DE MÚSICAS - TheAudioDB")
print("="*50)

while True:
    print("\nEscolha uma opção:")
    print("1 - Buscar Cantor/Banda")
    print("2 - Buscar Álbuns")
    print("3 - Buscar Músicas (Top 3)")
    print("0 - Sair")

    opcao = input("\nDigite o número da opção: ").strip()

    if opcao == "0":
