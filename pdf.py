import io
from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

from processamento import preparar_para_impressao, SANGRIA_CM

# -------------------------
# Configurações
# -------------------------

LARGURA_PDF = 11 * cm  # 10cm de corte + 0,5cm de sangria de cada lado
ALTURA_PDF = 16 * cm    # 15cm de corte + 0,5cm de sangria de cada lado

SANGRIA_PDF = SANGRIA_CM * cm

# Marcas de corte (crop marks) — ligue/desligue aqui
INCLUIR_MARCAS_DE_CORTE = True

TAMANHO_MARCA = 0.3 * cm     # comprimento de cada tracinho
ESPESSURA_MARCA = 0.3        # em pontos (linha bem fina)


def desenhar_marcas_de_corte(pdf):
    """
    Desenha marcas de corte nos 4 cantos, exatamente na linha
    de corte (onde termina a sangria e começa o tamanho final
    10x15cm). Ficam dentro da própria área de sangria, já que
    o documento não tem espaço extra além dela.
    """

    pdf.setLineWidth(ESPESSURA_MARCA)

    x0, y0 = SANGRIA_PDF, SANGRIA_PDF
    x1, y1 = LARGURA_PDF - SANGRIA_PDF, ALTURA_PDF - SANGRIA_PDF

    cantos = [
        (x0, y0, -1, -1),  # inferior esquerdo
        (x1, y0, 1, -1),   # inferior direito
        (x0, y1, -1, 1),   # superior esquerdo
        (x1, y1, 1, 1),    # superior direito
    ]

    for cx, cy, dir_x, dir_y in cantos:
        pdf.line(cx, cy, cx + (TAMANHO_MARCA * dir_x), cy)
        pdf.line(cx, cy, cx, cy + (TAMANHO_MARCA * dir_y))


def gerar_pdfs(lista_imagens):

    pasta = Path("output")
    pasta.mkdir(exist_ok=True)

    for caminho in lista_imagens:

        nome = Path(caminho).stem

        imagem = preparar_para_impressao(caminho)

        buffer = io.BytesIO()
        imagem.save(
            buffer,
            format="JPEG",
            quality=100,
            dpi=(300, 300)
        )
        buffer.seek(0)

        pdf = canvas.Canvas(
            str(pasta / f"{nome}.pdf"),
            pagesize=(LARGURA_PDF, ALTURA_PDF)
        )

        pdf.drawImage(
            ImageReader(buffer),
            0,
            0,
            width=LARGURA_PDF,
            height=ALTURA_PDF
        )

        if INCLUIR_MARCAS_DE_CORTE:
            desenhar_marcas_de_corte(pdf)

        pdf.save()

    print("PDFs gerados com sucesso!")