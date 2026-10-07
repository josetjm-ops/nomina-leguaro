"""Arma la app instalable (PWA) a partir de apps-script/Index.html.

Uso: python construir.py   -> genera index.html e iconos en esta carpeta.
Correr cada vez que cambie apps-script/Index.html, y luego publicar esta carpeta en GitHub Pages.
"""
import io
import os
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
VERDE = (46, 107, 58)

CABECERA = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#2e6b3a">
<title>Nómina Leguaro</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icono-192.png">
<link rel="apple-touch-icon" href="icono-192.png">"""

REGISTRO_SW = """<script>
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js');
</script>
</body>"""


def construir_html():
    html = io.open(os.path.join(AQUI, '..', 'apps-script', 'Index.html'), encoding='utf-8').read()
    assert html.count('<meta charset="utf-8">') == 1 and html.count('</body>') == 1
    html = html.replace('<base target="_top">\n', '')
    html = html.replace('<meta charset="utf-8">', CABECERA)
    html = html.replace('</body>', REGISTRO_SW)
    io.open(os.path.join(AQUI, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)


def construir_icono(lado):
    # El dibujo va centrado y pequeño para que Android pueda recortarlo en círculo (icono "maskable").
    img = Image.new('RGB', (lado, lado), VERDE)
    d = ImageDraw.Draw(img)
    r = lado * 0.30
    c = lado / 2
    d.ellipse([c - r, c - r, c + r, c + r], fill='white')
    fuente = ImageFont.load_default(size=int(lado * 0.42))
    d.text((c, c), 'L', fill=VERDE, font=fuente, anchor='mm')
    img.save(os.path.join(AQUI, 'icono-%d.png' % lado))


if __name__ == '__main__':
    construir_html()
    for lado in (192, 512):
        construir_icono(lado)
    print('App construida en', AQUI)
