from PIL import Image

# -----------------------------
# Configurações de impressão
# -----------------------------

DPI = 300

# Tamanho de CORTE (o tamanho final da carta depois de cortada)
LARGURA_CM = 10
ALTURA_CM = 15

# Sangria pedida pela gráfica (adicionada em cada lado)
SANGRIA_CM = 0.5

# Conversão cm -> pixels a 300 DPI
def cm_para_px(cm):
    return int(round((cm / 2.54) * DPI))

LARGURA_CORTE = cm_para_px(LARGURA_CM)
ALTURA_CORTE = cm_para_px(ALTURA_CM)
SANGRIA_PX = cm_para_px(SANGRIA_CM)

# Tamanho TOTAL do documento = corte + sangria dos dois lados
LARGURA_TOTAL = LARGURA_CORTE + (SANGRIA_PX * 2)
ALTURA_TOTAL = ALTURA_CORTE + (SANGRIA_PX * 2)


def _esticar_bordas(canvas, img, offset_x, offset_y):
    """
    Preenche a faixa de sangria ao redor da arte "esticando" a
    borda da própria imagem para fora, em vez de cortar conteúdo
    ou colar uma cor sólida artificial. É a mesma ideia do
    "Content-Aware Extend" / "Canvas Extension" do Photoshop.
    """

    w, h = img.size

    # --- Topo e base (esticando a linha de pixels do topo/base) ---
    if offset_y > 0:
        linha_topo = img.crop((0, 0, w, 1)).resize((w, offset_y), Image.Resampling.LANCZOS)
        canvas.paste(linha_topo, (offset_x, 0))

        linha_base = img.crop((0, h - 1, w, h)).resize((w, offset_y), Image.Resampling.LANCZOS)
        canvas.paste(linha_base, (offset_x, offset_y + h))

    # --- Esquerda e direita ---
    if offset_x > 0:
        coluna_esq = img.crop((0, 0, 1, h)).resize((offset_x, h), Image.Resampling.LANCZOS)
        canvas.paste(coluna_esq, (0, offset_y))

        coluna_dir = img.crop((w - 1, 0, w, h)).resize((offset_x, h), Image.Resampling.LANCZOS)
        canvas.paste(coluna_dir, (offset_x + w, offset_y))

    # --- 4 cantos (cor sólida do pixel do canto) ---
    if offset_x > 0 and offset_y > 0:
        canvas.paste(img.getpixel((0, 0)), (0, 0, offset_x, offset_y))
        canvas.paste(img.getpixel((w - 1, 0)), (offset_x + w, 0, LARGURA_TOTAL, offset_y))
        canvas.paste(img.getpixel((0, h - 1)), (0, offset_y + h, offset_x, ALTURA_TOTAL))
        canvas.paste(img.getpixel((w - 1, h - 1)), (offset_x + w, offset_y + h, LARGURA_TOTAL, ALTURA_TOTAL))


def preparar_para_impressao(caminho):
    """
    Prepara a imagem para impressão com sangria real, SEM cortar
    conteúdo da arte:

    1. A arte é redimensionada para caber exatamente no tamanho
       de CORTE (10x15cm), preservando 100% do conteúdo.
    2. A faixa de sangria (0,5cm ao redor) é preenchida esticando
       a borda da própria arte para fora — não corta nada e não
       usa uma cor sólida "inventada".
    """

    img = Image.open(caminho).convert("RGB")

    # Redimensiona para o tamanho exato de corte (10x15cm).
    # Se a proporção da imagem já bate com 10x15 (como é o caso
    # aqui: 1024x1536 = proporção 0,6667 = 10/15), isso não
    # distorce nada.
    img_corte = img.resize((LARGURA_CORTE, ALTURA_CORTE), Image.Resampling.LANCZOS)

    # Cria o canvas final (corte + sangria)
    canvas_final = Image.new("RGB", (LARGURA_TOTAL, ALTURA_TOTAL))

    # Cola a arte centralizada
    canvas_final.paste(img_corte, (SANGRIA_PX, SANGRIA_PX))

    # Preenche a sangria esticando as bordas da própria arte
    _esticar_bordas(canvas_final, img_corte, SANGRIA_PX, SANGRIA_PX)

    return canvas_final