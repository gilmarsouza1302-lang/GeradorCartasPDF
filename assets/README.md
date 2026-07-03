# 🃏 Gerador de Cartas PDF

Aplicativo desenvolvido em **Python** para transformar imagens de cartas em **PDFs individuais**, prontos para impressão em gráfica.

Este projeto surgiu da necessidade de preparar cartas para um projeto escolar, ajustando automaticamente as imagens para o tamanho correto e adicionando a sangria necessária para impressão.

---

## 📸 Interface

![Interface do aplicativo](assets/interface.png)

---

## ✨ Funcionalidades

- 📂 Selecionar uma ou várias imagens
- 👀 Pré-visualização da carta
- 📄 Gerar um PDF para cada carta
- 📏 Formato 10 × 15 cm
- ✂️ Sangria de 0,5 cm
- 🎨 Interface gráfica moderna com CustomTkinter
- 🖥️ Geração de executável (.exe)

---

## 🛠️ Tecnologias utilizadas

- Python 3
- CustomTkinter
- Pillow (PIL)
- ReportLab
- Git
- GitHub

---

## 📂 Estrutura do projeto

```text
GeradorPDFCartas/
│
├── assets/
├── output/
├── interface.py
├── processamento.py
├── pdf.py
├── main.py
├── README.md
└── .gitignore
```

---

## 🚀 Como executar

Clone o repositório:

```bash
git clone https://github.com/gilmarsouza1302-lang/GeradorCartasPDF.git
```

Entre na pasta:

```bash
cd GeradorCartasPDF
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python main.py
```

---

## 📦 Gerar o executável

```bash
pyinstaller --onefile --windowed --name GeradorCartasPDF main.py
```

---

## 👨‍💻 Autor

**Gilmar da Silva Souza**

Estudante de desenvolvimento de software, desenvolvendo projetos práticos com Python, JavaScript e Inteligência Artificial.

GitHub:
https://github.com/gilmarsouza1302-lang

---

## 📄 Licença

Projeto desenvolvido para fins de estudo e portfólio.