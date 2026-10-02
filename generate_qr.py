import qrcode
from PIL import Image, ImageDraw, ImageFont
import zxingcpp
import os

def generate_qrs():
    target_url = "https://sarthakpolshettiwar-alt.github.io/myQR/"
    
    # 1. Generate High-Res Final QR (min 2000x2000 px)
    # With box_size=40 and border=4:
    # A version 3 QR has 29 modules + 8 border = 37 modules -> 37 * 40 = 1480.
    # To get >= 2000x2000 px, box_size=60 gives ~2220x2220 px!
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=60,
        border=4
    )
    qr.add_data(target_url)
    qr.make(fit=True)
    
    # Dark modules on crisp white background
    qr_img = qr.make_image(fill_color="#181A32", back_color="#FFFFFF").convert("RGB")
    print(f"Generated QR image size: {qr_img.size}")
    
    # Save qr-contact-final.png
    qr_img.save("qr-contact-final.png", "PNG", dpi=(300, 300))
    print("Saved qr-contact-final.png")
    
    # Also save as qr-contact.png for backward compatibility & website use
    qr_img.save("qr-contact.png", "PNG", dpi=(300, 300))
    print("Saved qr-contact.png (updated to high-res final)")
    
    # 2. Verify qr-contact-final.png with zxingcpp
    decoded1 = zxingcpp.read_barcode(Image.open("qr-contact-final.png"))
    assert decoded1 is not None, "Failed to decode qr-contact-final.png"
    assert decoded1.text == target_url, f"Mismatch in qr-contact-final.png: {decoded1.text}"
    print(f"Verification SUCCESS for qr-contact-final.png: '{decoded1.text}'")

    # 3. Generate Printable Sticker Version: qr-contact-final-print.png
    # Sticker Canvas: e.g. 2400 x 3200 px at 300 DPI
    canvas_w = 2400
    canvas_h = 3200
    sticker = Image.new("RGB", (canvas_w, canvas_h), color="#FFFFFF")
    draw = ImageDraw.Draw(sticker)
    
    # Draw an outer rounded sticker border / cut line
    border_margin = 60
    border_color = "#383B66"
    draw.rounded_rectangle(
        [(border_margin, border_margin), (canvas_w - border_margin, canvas_h - border_margin)],
        radius=80,
        outline=border_color,
        width=12
    )
    
    # Inner decorative accent frame
    inner_margin = 90
    draw.rounded_rectangle(
        [(inner_margin, inner_margin), (canvas_w - inner_margin, canvas_h - inner_margin)],
        radius=60,
        outline="#EAADC2",
        width=4
    )
    
    # Top Header banner (Navy)
    banner_top = 110
    banner_bottom = 360
    draw.rounded_rectangle(
        [(inner_margin + 20, banner_top), (canvas_w - inner_margin - 20, banner_bottom)],
        radius=30,
        fill="#383B66"
    )
    
    # Load fonts (system default fallback or Truetype if available)
    try:
        font_banner = ImageFont.truetype("arialbd.ttf", 72)
        font_name = ImageFont.truetype("arialbd.ttf", 92)
        font_sub = ImageFont.truetype("arial.ttf", 52)
        font_phone = ImageFont.truetype("arialbd.ttf", 68)
        font_footer = ImageFont.truetype("arialbd.ttf", 64)
    except Exception:
        font_banner = ImageFont.load_default()
        font_name = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_phone = ImageFont.load_default()
        font_footer = ImageFont.load_default()

    # Draw Banner Text: "CONTACT THE CAR OWNER"
    text_banner = "CONTACT THE CAR OWNER"
    bbox = draw.textbbox((0, 0), text_banner, font=font_banner)
    text_w = bbox[2] - bbox[0]
    draw.text(((canvas_w - text_w) / 2, banner_top + 80), text_banner, font=font_banner, fill="#FFFFFF")
    
    # Owner Name: Sarthak Polshettiwar
    text_name = "Sarthak Polshettiwar"
    bbox = draw.textbbox((0, 0), text_name, font=font_name)
    text_w = bbox[2] - bbox[0]
    draw.text(((canvas_w - text_w) / 2, 410), text_name, font=font_name, fill="#1A1C33")
    
    # Phone Numbers Display
    text_p1 = "Primary: +91 9763574459"
    bbox = draw.textbbox((0, 0), text_p1, font=font_phone)
    text_w = bbox[2] - bbox[0]
    draw.text(((canvas_w - text_w) / 2, 530), text_p1, font=font_phone, fill="#383B66")
    
    text_p2 = "Secondary: +91 8007057507"
    bbox = draw.textbbox((0, 0), text_p2, font=font_phone)
    text_w = bbox[2] - bbox[0]
    draw.text(((canvas_w - text_w) / 2, 620), text_p2, font=font_phone, fill="#5E4272")
    
    # Divider line
    draw.line([(300, 720), (canvas_w - 300, 720)], fill="#EAADC2", width=4)

    # Paste QR Code in center
    # Resize QR to fit nicely: 1800 x 1800 px
    qr_display_size = 1800
    resized_qr = qr_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)
    qr_x = (canvas_w - qr_display_size) // 2
    qr_y = 780
    sticker.paste(resized_qr, (qr_x, qr_y))
    
    # Bottom callout: "SCAN TO CONTACT OWNER"
    text_footer = "SCAN TO CONTACT OWNER"
    bbox = draw.textbbox((0, 0), text_footer, font=font_footer)
    text_w = bbox[2] - bbox[0]
    draw.text(((canvas_w - text_w) / 2, 2660), text_footer, font=font_footer, fill="#383B66")
    
    # Sub-footer instructions
    text_inst = "Parking Concern  •  Lights Left On  •  Emergency"
    bbox = draw.textbbox((0, 0), text_inst, font=font_sub)
    text_w = bbox[2] - bbox[0]
    draw.text(((canvas_w - text_w) / 2, 2760), text_inst, font=font_sub, fill="#7E82A3")

    sticker.save("qr-contact-final-print.png", "PNG", dpi=(300, 300))
    print("Saved qr-contact-final-print.png (Size: 2400x3200, DPI: 300)")
    
    # 4. Verify qr-contact-final-print.png with zxingcpp
    decoded2 = zxingcpp.read_barcode(Image.open("qr-contact-final-print.png"))
    assert decoded2 is not None, "Failed to decode qr-contact-final-print.png"
    assert decoded2.text == target_url, f"Mismatch in qr-contact-final-print.png: {decoded2.text}"
    print(f"Verification SUCCESS for qr-contact-final-print.png: '{decoded2.text}'")

if __name__ == "__main__":
    generate_qrs()
