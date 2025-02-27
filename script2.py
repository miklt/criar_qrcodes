import zipfile
from PIL import Image
import io
import os

def extrair_imagens_docx(docx_path, output_folder='imagens_extraidas'):
    # Criar pasta de saída se não existir
    os.makedirs(output_folder, exist_ok=True)
    
    # Contador para nomear os arquivos
    contador = 1
    
    # Abrir o arquivo .docx como ZIP
    with zipfile.ZipFile(docx_path, 'r') as docx_zip:
        # Listar todos os arquivos no ZIP
        file_list = docx_zip.namelist()
        
        # Filtrar arquivos de mídia
        media_files = [f for f in file_list if f.startswith('word/media/')]
        
        # Processar cada arquivo de mídia
        for media_file in media_files:
            try:
                # Extrair dados da imagem
                file_data = docx_zip.read(media_file)
                
                # Gerar nome do arquivo de saída
                output_path = os.path.join(output_folder, f'{contador}.png')
                
                # Tentar salvar diretamente se for PNG, caso contrário converter
                if media_file.lower().endswith('.png'):
                    with open(output_path, 'wb') as f:
                        f.write(file_data)
                else:
                    # Converter para PNG usando Pillow
                    img = Image.open(io.BytesIO(file_data))
                    img.save(output_path, 'PNG')
                
                print(f'Imagem salva: {output_path}')
                contador += 1
                
            except Exception as e:
                print(f'Erro ao processar {media_file}: {str(e)}')

if __name__ == "__main__":
    # Usar o arquivo do usuário
    extrair_imagens_docx('QuadroEditável.docx')
    
    print("Processo concluído. Verifique a pasta 'imagens_extraidas'.")