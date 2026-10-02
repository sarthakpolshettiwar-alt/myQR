import qrcode
import qrcode.image.svg
from PIL import Image, ImageDraw, ImageFont
import zxingcpp
import os

target_url = "https://sarthakpolshettiwar-alt.github.io/myQR/"

def generate_all():
    print("Generating Highest Quality QR Assets...")
    
    # 1. VECTOR SVG (Infinite Lossless Resolution)
    factory = qrcode.image.svg.SvgPathImage
    qr_svg = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=30,
        border=4,
        image_factory=factory
    )
    qr_svg.add_data(target_url)
    qr_svg.make(fit=True)
    svg_img = qr_svg.make_image(fill_color="#181A32", back_color="#FFFFFF")
    svg_img.save("qr-contact-final.svg")
    print("[OK] Generated Vector SVG: qr-contact-final.svg (Infinite Resolution)")

    # 2. ULTRA-HD PNG (4000 x 4000 px, 600 DPI)
    # Box size 80 with 49 modules (including border) gives 3920 x 3920 px
    # Box size 82 gives 4018 x 4018 px!
    qr_png = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=82,
        border=4
    )
    qr_png.add_data(target_url)
    qr_png.make(fit=True)
    
    ultra_img = qr_png.make_image(fill_color="#181A32", back_color="#FFFFFF").convert("RGB")
    ultra_img.save("qr-contact-final.png", "PNG", dpi=(600, 600))
    ultra_img.save("qr-contact.png", "PNG", dpi=(600, 600))
    print(f"[OK] Generated Ultra-HD PNG: qr-contact-final.png ({ultra_img.size[0]}x{ultra_img.size[1]} px, 600 DPI)")
    
    # Verify ultra PNG
    decoded_ultra = zxingcpp.read_barcode(Image.open("qr-contact-final.png"))
    assert decoded_ultra.text == target_url, "QR Mismatch!"
    print(f"[OK] Verified qr-contact-final.png: '{decoded_ultra.text}'")

    # 3. PRINTABLE STICKER ULTRA (3000 x 4000 px, 300 DPI)
    canvas_w = 3000
    canvas_h = 4000
    sticker = Image.new("RGB", (canvas_w, canvas_h), color="#FFFFFF")
    draw = ImageDraw.Draw(sticker)
    
    # Outer cut border
    draw.rounded_rectangle(
        [(80, 80), (canvas_w - 80, canvas_h - 80)],
        radius=100,
        outline="#383B66",
        width=16
    )
    
    # Inner pink accent line
    draw.rounded_rectangle(
        [(120, 120), (canvas_w - 120, canvas_h - 120)],
        radius=80,
        outline="#EAADC2",
        width=6
    )
    
    # Header Banner
    banner_top = 150
    banner_bottom = 460
    draw.rounded_rectangle(
        [(150, banner_top), (canvas_w - 150, banner_bottom)],
        radius=40,
        fill="#383B66"
    )
    
    try:
        font_banner = ImageFont.truetype("arialbd.ttf", 92)
        font_name = ImageFont.truetype("arialbd.ttf", 115)
        font_sub = ImageFont.truetype("arial.ttf", 66)
        font_phone = ImageFont.truetype("arialbd.ttf", 86)
        font_footer = ImageFont.truetype("arialbd.ttf", 80)
    except Exception:
        font_banner = ImageFont.load_default()
        font_name = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_phone = ImageFont.load_default()
        font_footer = ImageFont.load_default()

    # Banner Text
    t_banner = "CONTACT THE CAR OWNER"
    bb = draw.textbbox((0, 0), t_banner, font=font_banner)
    draw.text(((canvas_w - (bb[2] - bb[0])) / 2, banner_top + 105), t_banner, font=font_banner, fill="#FFFFFF")
    
    # Owner Name
    t_name = "Sarthak Polshettiwar"
    bb = draw.textbbox((0, 0), t_name, font=font_name)
    draw.text(((canvas_w - (bb[2] - bb[0])) / 2, 530), t_name, font=font_name, fill="#1A1C33")
    
    # Phone Numbers
    t_p1 = "Primary: +91 9763574459"
    bb = draw.textbbox((0, 0), t_p1, font=font_phone)
    draw.text(((canvas_w - (bb[2] - bb[0])) / 2, 680), t_p1, font=font_phone, fill="#383B66")
    
    t_p2 = "Secondary: +91 8007057507"
    bb = draw.textbbox((0, 0), t_p2, font=font_phone)
    draw.text(((canvas_w - (bb[2] - bb[0])) / 2, 790), t_p2, font=font_phone, fill="#5E4272")
    
    # Accent line
    draw.line([(350, 920), (canvas_w - 350, 920)], fill="#EAADC2", width=6)
    
    # Resize QR to paste in center: 2260 x 2260 px
    qr_display_size = 2260
    resized_qr = ultra_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)
    sticker.paste(resized_qr, ((canvas_w - qr_display_size) // 2, 990))
    
    # Prompt text
    t_footer = "SCAN TO CONTACT OWNER"
    bb = draw.textbbox((0, 0), t_footer, font=font_footer)
    draw.text(((canvas_w - (bb[2] - bb[0])) / 2, 3340), t_footer, font=font_footer, fill="#383B66")
    
    t_reasons = "Parking Concern  •  Lights Left On  •  Emergency"
    bb = draw.textbbox((0, 0), t_reasons, font=font_sub)
    draw.text(((canvas_w - (bb[2] - bb[0])) / 2, 3470), t_reasons, font=font_sub, fill="#7E82A3")

    sticker.save("qr-contact-final-print.png", "PNG", dpi=(300, 300))
    sticker.save("qr-contact-final-print.pdf", "PDF", resolution=300.0)
    print(f"[OK] Generated Printable Sticker PNG & PDF: qr-contact-final-print.png ({canvas_w}x{canvas_h} px)")

    # Verify Printable Sticker
    decoded_sticker = zxingcpp.read_barcode(Image.open("qr-contact-final-print.png"))
    assert decoded_sticker.text == target_url, "Sticker QR Mismatch!"
    print(f"[OK] Verified qr-contact-final-print.png: '{decoded_sticker.text}'")

if __name__ == '__main__':
    generate_all()
