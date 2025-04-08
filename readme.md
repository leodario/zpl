### Instalar Python
- (https://www.python.org/downloads/)

### baixe o release
1. **Instale o Poppler para Windows:**
   - Faça o download do Poppler para Windows [neste link](https://github.com/oschwartz10612/poppler-windows/releases/)
   - Baixe a versão mais recente do arquivo `Release-xxxx.zip`
   - Extraia o conteúdo para uma pasta, por exemplo: `C:\Program Files\poppler`

2. **Adicione o Poppler ao PATH do sistema:**
   - Abra as Configurações do Windows
   - Procure por "Variáveis de Ambiente"
   - Em "Variáveis do Sistema", encontre "Path"
   - Clique em "Editar" e depois em "Novo"
   - Adicione o caminho para a pasta `bin` do Poppler (exemplo: `C:\Program Files\poppler\Library\bin`)


**Estrutura de pastas recomendada:**
```
D:\iq\ZPL\
│
├── pdf_to_zpl.py
├── pdf_input\
│   └── packing_slip.pdf
├── zpl_output\
└── venv\
```

### Intalando maquina virtual
- python -m venv venv

### Ativando o ambiente virtual
- .\venv\Scripts\activate

### instalando as bibliotecas necessárias
- pip install pdf2image pillow

### listando bibliotecas
- pip list

### Rodando o sistema
- python pdf_to_zpl.py