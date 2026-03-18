import sys
import requests
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QTextEdit, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

        # Funções de busca da API
def buscar_artista():
    dado_busca = busca.text()
    if dado_busca == "": # Tratativa para campo vazio
        QMessageBox.critical(janela, 'Atenção', 'Para localizar o cantor/banda, você deve inserir um nome...')
        return
    url = f"https://www.theaudiodb.com/api/v1/json/123/search.php?s={dado_busca}"
    resposta = requests.get(url)
    dados = resposta.json()

    if dados.get("artists"):
        artista = dados["artists"][0]
        nome = artista.get("strArtist", "N/A")
        genero = artista.get("strGenre", "N/A")
        bio = artista.get("strBiographyPT", "Sem biografia disponível")
        pais = artista.get("strCountry", "N/A")
        
        # Formatar os resultados em quabra de linha para melhor vizualização
        texto = f"Nome: {nome}\n\nGênero: {genero}\n\nPaís: {pais} \n\nBiografia:\n\n{bio}"
        caixa_texto.setPlainText(texto)
    else:
        caixa_texto.setPlainText("Nenhum artista encontrado.")

def buscar_albuns():
    dado_busca = busca.text()
    if dado_busca == "": # Tratativa para campo vazio
        QMessageBox.critical(janela, 'Atenção', 'Para localizar o album, você deve inserir um nome...')
        return
    url = f"https://www.theaudiodb.com/api/v1/json/123/searchalbum.php?s={dado_busca}"
    resposta = requests.get(url)
    dados = resposta.json()

    if dados.get("album"):
        texto = "Álbuns encontrados:\n\n"
        for album in dados["album"]:
            nome_album = album.get("strAlbum", "N/A")
            ano = album.get("intYearReleased", "N/A")
            texto += f"- {nome_album} ({ano})\n\n"
        caixa_texto.setPlainText(texto)
    else:
        caixa_texto.setPlainText("Nenhum álbum encontrado.")

def buscar_faixas():
    dado_busca = busca.text()
    if dado_busca == "": # Tratativa para campo vazio
        QMessageBox.critical(janela, 'Atenção', 'Para localizar as musicas, você deve inserir um nome...')
        return
    url = f"https://www.theaudiodb.com/api/v1/json/123/track-top10.php?s={dado_busca}"
    resposta = requests.get(url)
    dados = resposta.json()
    
    if dados.get("track"):
        texto = "Faixas encontradas:\n\n"
        for faixa in dados["track"][:3]:  # limitada às 3 primeiras, API Grátis 😁
            nome_faixa = faixa.get("strTrack", "N/A")
            artista = faixa.get("strArtist", "N/A")
            album = faixa.get("strAlbum", "N/A")
            # thumb = faixa.get("strTrackThumb", "N/A")
            texto += f"- {nome_faixa} — {artista} (Álbum: {album})\n\n "
        caixa_texto.setPlainText(texto)
    else:
        caixa_texto.setPlainText("Nenhuma faixa encontrada.")


def baixar_pixmap(url_thumb: str) -> QPixmap:
    """Baixa a imagem (thumb) e retorna um QPixmap. Levanta exceção se falhar."""
    resp = requests.get(url_thumb, timeout=10)
    resp.raise_for_status()
    pix = QPixmap()
    if not pix.loadFromData(resp.content):
        raise ValueError("Não foi possível carregar a imagem nos bytes recebidos.")
    return pix

def buscar_faixas():
    dado_busca = busca.text().strip()
    if dado_busca == "":  # Tratativa para campo vazio
        QMessageBox.critical(janela, 'Atenção', 'Para localizar as músicas, você deve inserir um nome...')
        return

    try:
        url = f"https://www.theaudiodb.com/api/v1/json/123/track-top10.php?s={dado_busca}"
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
    except Exception as e:
        QMessageBox.critical(janela, 'Erro', f"Falha ao consultar a API: {e}")
        return

    # Limpa o label de thumb a cada busca (se existir)
    try:
        thumb_label.clear()
        thumb_label.setText("")
        thumb_label.setAlignment(Qt.AlignCenter)
    except NameError:
        # Se não existir um QLabel de miniatura, ignore
        pass

    if dados.get("track"):
        texto = "Faixas encontradas:\n\n"
        primeira_thumb_url = None

        for faixa in dados["track"][:3]:  # limitada às 3 primeiras, API grátis
            nome_faixa = faixa.get("strTrack", "N/A")
            artista = faixa.get("strArtist", "N/A")
            album = faixa.get("strAlbum", "N/A")
            thumb_url = faixa.get("strTrackThumb")  # pode ser None

            if not primeira_thumb_url and thumb_url:
                primeira_thumb_url = thumb_url

            texto += f"- {nome_faixa} — {artista} (Álbum: {album})\n\n"

        caixa_texto.setPlainText(texto)

        # Com a QLabel para a thumb, irá mostrar a primeira disponível
        if primeira_thumb_url:
            try:
                pix = baixar_pixmap(primeira_thumb_url)

                # Opcional: redimensiona a miniatura para caber no label mantendo proporção
                if thumb_label.width() > 0 and thumb_label.height() > 0:
                    pix = pix.scaled(
                        thumb_label.width(),
                        thumb_label.height(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )

                thumb_label.setPixmap(pix)
                thumb_label.setText("")  # limpa texto
                thumb_label.setAlignment(Qt.AlignCenter)
            except Exception as e:
                # Se falhar o download, apenas não exibirá a thumb
                print(f"Falha ao baixar/exibir thumb: {e}")
        else:
            # Não há thumb nas 3 primeiras faixas
            try:
                thumb_label.setText("")
            except NameError:
                pass

    else:
        caixa_texto.setPlainText("Nenhuma faixa encontrada.")
        try:
            thumb_label.setText("")
        except NameError:
            pass

        #Criando o APP
app = QApplication(sys.argv)

        #Criando o QWidget
janela = QWidget()
janela.setWindowTitle('App localizador de músicas') # Título
janela.setFixedSize(600, 700) # Tamanho da Janela
        # Caminho do arquivo .ico na mesma pasta do script
caminho_icone = os.path.join(os.path.dirname(__file__), "ico.jpg")
janela.setWindowIcon(QIcon(caminho_icone))
#janela.setWindowIcon(QIcon('C:/Users/luiz.cribas/OneDrive - SENAC - SP/Área de Trabalho/Apresentar API/ico.jpg'))  # caminho do icone PC


        # Linha de inserir dados para busca
busca = QLineEdit(janela)
busca.setPlaceholderText("Digite o nome do cantor, album ou música...")
busca.setFixedWidth(600)   # largura fixa
busca.setFixedHeight(20)   # altura fixa

        # Caixa de Texto que receberá os dados
caixa_texto = QTextEdit(janela)
caixa_texto.move(5,150)
caixa_texto.setReadOnly(True) # Comando para não deixar escrever na caixa de texto
caixa_texto.setFixedWidth(590)
caixa_texto.setFixedHeight(590)

            # Botões de pesquisa
botao_artista = QPushButton("Buscar Cantor/Banda 😎🎶")
botao_album = QPushButton("Buscar Álbuns 💿📀")
botao_faixa = QPushButton("Buscar Música 🔊🎵")
caixa_texto = QTextEdit()
caixa_texto.setReadOnly(True)

layout = QVBoxLayout()
layout.addWidget(busca)
layout.addWidget(botao_artista)
layout.addWidget(botao_album)
layout.addWidget(botao_faixa)
layout.addWidget(caixa_texto)
janela.setLayout(layout)

# QLabel em branco para exibir a Thumb
thumb_label = QLabel("")
thumb_label.setFixedSize(300, 300)  # Tamanho da Label
thumb_label.setAlignment(Qt.AlignCenter) # Alinhamento
layout.addWidget(thumb_label)

botao_artista.clicked.connect(buscar_artista)
botao_album.clicked.connect(buscar_albuns)
botao_faixa.clicked.connect(buscar_faixas)

janela.show()
sys.exit(app.exec_())