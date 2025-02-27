import re
import os
import qrcode


def parse_entries(content):
    entries = []
    current_desc = None
    for line in content.split("\n"):
        line = line.strip()
        if not line:
            continue

        if line.startswith("-"):
            parts = re.split(r"(https?://\S+)", line[1:].strip(), 1)
            current_desc = parts[0].strip()
            if len(parts) > 1 and parts[1]:
                entries.append((current_desc, parts[1]))
        elif current_desc:
            urls = re.findall(r"https?://\S+", line)
            for url in urls:
                entries.append((current_desc, url))
    return entries


def sanitize_filename(desc):
    # Remove caracteres especiais e formata para snake_case
    name = re.sub(r"[^\w\s-]", "", desc.lower())
    name = re.sub(r"[\s-]+", "_", name).strip("_")
    return name


def generate_qrcode(url, desc, size=10, output_dir="qrcodes"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = sanitize_filename(desc)
    counter = 1
    filename = f"{base_name}.png"

    # Verifica duplicatas e adiciona sufixo numérico
    while os.path.exists(os.path.join(output_dir, filename)):
        filename = f"{base_name}_{counter}.png"
        counter += 1

    filepath = os.path.join(output_dir, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)
    return filename


def create_html(entries, qr_size, output_file="output.html"):
    html = """<html><body>
    <table border="1">
    <tr><th>Descrição</th><th>URL</th><th>QR Code</th></tr>"""

    for desc, url in entries:
        qr_file = generate_qrcode(url, desc, qr_size)
        html += f"""
        <tr>
            <td>{desc}</td>
            <td><a href="{url}">{url}</a></td>
            <td><img src="qrcodes/{qr_file}" width="{qr_size*10}"></td>
        </tr>"""

    html += "</table></body></html>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)


# Configurações
qr_size = 10  # Altere este valor para ajustar o tamanho do QR Code

# Execução
with open("lista.txt", "r", encoding="utf-8") as f:
    content = f.read()

entries = parse_entries(content)
create_html(entries, qr_size)
