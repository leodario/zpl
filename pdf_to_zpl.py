import os
from pdf2image import convert_from_path
from PIL import Image
import tempfile

POPPLER_PATH = r"C:\Program Files\poppler\Library\bin"

def pdf_to_zpl_batch(input_folder, output_folder, width_cm=10, height_cm=15, dpi=203):
    """
    Converte todos os PDFs de uma pasta para ZPL em outra pasta
    :param input_folder: Pasta com os PDFs de entrada
    :param output_folder: Pasta para salvar os arquivos ZPL
    :param width_cm: Largura desejada em centímetros (padrão 10cm)
    :param height_cm: Altura desejada em centímetros (padrão 15cm)
    :param dpi: Resolução em DPI (pontos por polegada, padrão 203)
    """
    # Verifica se as pastas existem
    if not os.path.exists(input_folder):
        print(f"Pasta de entrada '{input_folder}' não encontrada!")
        return
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Pasta de saída '{output_folder}' criada.")

    # Converte cm para pixels (1 polegada = 2.54 cm)
    width_px = int((width_cm / 2.54) * dpi)
    height_px = int((height_cm / 2.54) * dpi)

    # Processa cada arquivo PDF na pasta de entrada
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            zpl_filename = os.path.splitext(filename)[0] + '.zpl'
            zpl_path = os.path.join(output_folder, zpl_filename)

            print(f"Processando: {filename}...")

            try:
                # Converte PDF para imagem
                images = convert_from_path(pdf_path, dpi=dpi, poppler_path=POPPLER_PATH)

                # Processa cada página do PDF
                for i, image in enumerate(images):
                    # Redimensiona a imagem
                    resized_image = image.resize((width_px, height_px))

                    # Converte para preto e branco (1-bit)
                    bw_image = resized_image.convert('1')

                    # Cria o arquivo ZPL
                    zpl_data = image_to_zpl(bw_image)

                    # Salva o ZPL em arquivo
                    if len(images) > 1:
                        # Se tiver múltiplas páginas, adiciona número ao nome
                        base_name, ext = os.path.splitext(zpl_filename)
                        page_zpl_path = os.path.join(output_folder, f"{base_name}_p{i+1}{ext}")
                    else:
                        page_zpl_path = zpl_path

                    with open(page_zpl_path, 'w') as zpl_file:
                        zpl_file.write(zpl_data)

                    print(f"  Página {i+1} salva como {os.path.basename(page_zpl_path)}")

            except Exception as e:
                print(f"Erro ao processar {filename}: {str(e)}")

def image_to_zpl(image):
    """
    Converte uma imagem PIL para ZPL
    :param image: Imagem PIL no modo '1' (1-bit)
    :return: String com o código ZPL
    """
    width, height = image.size
    bytes_per_row = (width + 7) // 8  # Calcula bytes necessários por linha

    # Cabeçalho ZPL
    zpl = f"^XA\n^FO0,0\n^GFA,{bytes_per_row * height},{bytes_per_row * height},{bytes_per_row},"

    # Dados da imagem
    image_data = []
    for y in range(height):
        row_data = 0
        for x in range(width):
            pixel = image.getpixel((x, y))
            if pixel == 0:  # Preto
                row_data |= 1 << (7 - (x % 8))
            if x % 8 == 7 or x == width - 1:
                image_data.append(f"{row_data:02X}")
                row_data = 0

    zpl += ''.join(image_data) + "\n^XZ"
    return zpl

if __name__ == "__main__":
    # Configurações
    input_folder = "pdf_input"  # Pasta com os PDFs de entrada
    output_folder = "zpl_output"  # Pasta para salvar os ZPLs

    print("Iniciando conversão de PDF para ZPL...")
    pdf_to_zpl_batch(input_folder, output_folder)
    print("Conversão concluída!")