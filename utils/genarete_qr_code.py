import os
import qrcode

def calc_crc16(payload: str) -> str:
    crc = 0xFFFF
    for c in payload:
        crc ^= ord(c) << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return f"{crc:04X}"

def generate_payload_pix(pix_key: str, name: str, city: str, price: float = None, tx_id: str = "***") -> str:
    payload = "000201"
    gui = "br.gov.bcb.pix"
    info_adicional = "***"
    template26 = f"00{len(gui):02d}{gui}01{len(pix_key):02d}{pix_key}02{len(info_adicional):02d}{info_adicional}"
    payload += f"26{len(template26):02d}{template26}"

    payload += "52040000"
    payload += "5303986"

    if price:
        price_str = f"{float(price):.2f}"
        payload += f"54{len(price_str):02d}{price_str}"

    payload += f"58{len('BR'):02d}BR"
    payload += f"59{len(name):02d}{name}"
    payload += f"60{len(city):02d}{city}"

    payload += f"62{len('05' + '03' + tx_id):02d}05{len(tx_id):02d}{tx_id}"

    payload += "6304"
    payload += calc_crc16(payload)

    return payload


def generate_qrcode_pix(pix_key: str, name: str, city: str, price: float, tx_id: str, order_id: int,
                     folder: str = "qrcodes") -> str:
    os.makedirs(folder, exist_ok=True)

    payload = generate_payload_pix(pix_key, name, city, price, tx_id)
    qr = qrcode.make(payload)

    file_path = os.path.join(folder, f"pix_order_{order_id}.png")
    qr.save(file_path)
    return file_path