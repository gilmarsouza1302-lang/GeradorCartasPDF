import os
from tkinter import filedialog, messagebox
from PIL import Image
import customtkinter as ctk

from pdf import gerar_pdfs

# Lista global de arquivos
arquivos = []


# -------------------------------
# Selecionar imagens
# -------------------------------
def selecionar_imagens():
    global arquivos

    arquivos = filedialog.askopenfilenames(
        title="Selecione as cartas",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
    )

    lista.delete("1.0", "end")

    if not arquivos:
        contador.configure(text="0 carta(s)")
        preview.configure(image=None, text="Pré-visualização")
        return

    contador.configure(text=f"{len(arquivos)} carta(s)")

    for arquivo in arquivos:
        lista.insert("end", f"🃏 {os.path.basename(arquivo)}\n")

    mostrar_primeira_imagem()


# -------------------------------
# Preview
# -------------------------------
def mostrar_primeira_imagem():

    if not arquivos:
        return

    imagem = Image.open(arquivos[0]).convert("RGB")

    imagem.thumbnail((350, 544), Image.Resampling.LANCZOS)

    foto = ctk.CTkImage(
        light_image=imagem,
        dark_image=imagem,
        size=(imagem.width, imagem.height)
    )

    preview.configure(image=foto, text="")
    preview.image = foto


# -------------------------------
# Gerar PDF
# -------------------------------
def gerar():

    if not arquivos:
        messagebox.showwarning(
            "Aviso",
            "Selecione pelo menos uma imagem."
        )
        return

    try:
        gerar_pdfs(arquivos)

        messagebox.showinfo(
            "Sucesso",
            "PDFs gerados na pasta OUTPUT."
        )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            str(erro)
        )


# -------------------------------
# Interface
# -------------------------------
def iniciar_app():

    global lista
    global contador
    global preview

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()

    janela.title("Gerador de Cartas PDF")
    janela.geometry("1250x750")
    janela.configure(fg_color="#1A1A1A")

    # ---------------- TÍTULO ----------------

    titulo = ctk.CTkLabel(
        janela,
        text="🃏 GERADOR DE CARTAS PDF",
        font=("Segoe UI", 30, "bold"),
        text_color="#D4AF37"
    )

    titulo.pack(pady=20)

    # ---------------- BOTÃO SELECIONAR ----------------

    botao = ctk.CTkButton(
        janela,
        text="📂 Selecionar Cartas",
        command=selecionar_imagens,
        width=260,
        height=45,
        fg_color="#B8860B",
        hover_color="#D4AF37",
        text_color="black",
        font=("Segoe UI", 16, "bold")
    )

    botao.pack(pady=10)

    # ---------------- FRAME PRINCIPAL ----------------

    principal = ctk.CTkFrame(
        janela,
        fg_color="#1A1A1A"
    )

    principal.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # ---------------- LADO ESQUERDO ----------------

    esquerda = ctk.CTkFrame(
        principal,
        width=320,
        fg_color="#252525",
        corner_radius=15
    )

    esquerda.pack(
        side="left",
        fill="y",
        padx=10,
        pady=10
    )

    contador = ctk.CTkLabel(
        esquerda,
        text="0 carta(s)",
        font=("Segoe UI", 18, "bold"),
        text_color="#D4AF37"
    )

    contador.pack(pady=10)

    lista = ctk.CTkTextbox(
        esquerda,
        width=280,
        fg_color="#1F1F1F",
        text_color="white",
        font=("Consolas", 14)
    )

    lista.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    lista.insert("1.0", "Nenhuma carta selecionada.")

    # ---------------- LADO DIREITO ----------------

    direita = ctk.CTkFrame(
        principal,
        fg_color="#252525",
        corner_radius=15
    )

    direita.pack(
        side="left",
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    preview = ctk.CTkLabel(
        direita,
        text="Pré-visualização",
        font=("Segoe UI", 20, "bold"),
        text_color="#D4AF37"
    )

    preview.pack(expand=True)

    # ---------------- BOTÃO GERAR ----------------

    botao_pdf = ctk.CTkButton(
        janela,
        text="📄 GERAR PDF",
        command=gerar,
        width=260,
        height=50,
        fg_color="#B8860B",
        hover_color="#D4AF37",
        text_color="black",
        font=("Segoe UI", 18, "bold")
    )

    botao_pdf.pack(pady=20)

    janela.mainloop()