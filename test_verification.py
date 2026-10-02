import os
import PIL.Image
import zxingcpp

def main():
    required_files = ['index.html', 'style.css', 'README.md', 'qr-contact.png']
    for fname in required_files:
        if not os.path.exists(fname):
            raise FileNotFoundError(f"Missing file: {fname}")
        print(f"File verified: {fname} ({os.path.getsize(fname)} bytes)")
        
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    assert 'tel:+919763574459' in html, 'Missing tel link'
    assert 'https://wa.me/919763574459' in html, 'Missing WhatsApp link'
    assert 'Sarthak Polshettiwar' in html, 'Missing owner name'
    assert '+91 9763574459' in html, 'Missing phone number display'
    assert 'SCAN TO CONTACT OWNER' in html, 'Missing SCAN TO CONTACT OWNER text'
    assert 'qr-contact.png' in html, 'Missing qr-contact.png reference'
    print("All required HTML texts and links verified!")

    decoded = zxingcpp.read_barcode(PIL.Image.open('qr-contact.png'))
    print("Decoded QR Text:", decoded.text)
    assert decoded.text == 'https://sarthakpolshettiwar-alt.github.io/myQR/', 'QR content mismatch'
    print("QR Code decoding verification SUCCESS: decoded value matches target URL exactly.")

if __name__ == '__main__':
    main()
