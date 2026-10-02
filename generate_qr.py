import qrcode
from PIL import Image
import zxingcpp

def generate_and_verify_qr():
    target_url = "https://sarthakpolshettiwar-alt.github.io/myQR/"
    
    # Configure QR code with Error Correction H (High, 30%)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=24,   # High resolution modules
        border=4       # Standard quiet zone (at least 4 modules)
    )
    
    qr.add_data(target_url)
    qr.make(fit=True)
    
    # Generate high-contrast image (crisp dark navy/black on pure white background)
    img = qr.make_image(fill_color="#181A32", back_color="#FFFFFF").convert("RGB")
    
    output_path = "qr-contact.png"
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"QR code successfully generated and saved to {output_path} (Size: {img.size[0]}x{img.size[1]}px, DPI: 300)")
    
    # Verification using zxingcpp
    decoded = zxingcpp.read_barcode(Image.open(output_path))
    if not decoded:
        raise ValueError("Failed to decode the generated QR code!")
    
    print(f"Decoded content: '{decoded.text}'")
    if decoded.text != target_url:
        raise ValueError(f"Decoded content mismatch! Expected '{target_url}', got '{decoded.text}'")
    
    print("QR verification SUCCESS: The QR code encodes EXACTLY:", decoded.text)
    return True

if __name__ == "__main__":
    generate_and_verify_qr()
