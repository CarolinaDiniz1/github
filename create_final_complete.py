#!/usr/bin/env python3
"""
VERSÃO FINAL: Carrossel sem texto no rodapé (espaço para logo manual)
+ Banner para site 2000x600px
"""

from PIL import Image, ImageDraw, ImageFont
import os

# === CONFIGURAÇÕES CARROSSEL ===
WIDTH_CAROUSEL = 1080
HEIGHT_CAROUSEL = 1080

# === CONFIGURAÇÕES BANNER SITE ===
WIDTH_BANNER = 2000
HEIGHT_BANNER = 600

# Cores
COLOR_PRIMARY = "#1a2332"
COLOR_SECONDARY = "#2c3e50"
COLOR_ACCENT = "#c9a961"
COLOR_TEXT_LIGHT = "#ffffff"
COLOR_BG = "#f8f9fa"

def load_fonts():
    """Carrega fontes"""
    try:
        fonts = {
            'title': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70),
            'subtitle': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48),
            'body': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35),
            'highlight': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38),
            'small': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30),
            'tiny': ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26),
        }
        return fonts
    except:
        return {k: ImageFont.load_default() for k in ['title', 'subtitle', 'body', 'highlight', 'small', 'tiny']}

def center_text(draw, text, font, width=WIDTH_CAROUSEL):
    """Centraliza texto"""
    bbox = draw.textbbox((0, 0), text, font=font)
    return (width - (bbox[2] - bbox[0])) // 2

# === CARROSSEL - SLIDES ===

def create_carousel_slide_1():
    """Slide 1 - SEM texto no rodapé"""
    img = Image.new('RGB', (WIDTH_CAROUSEL, HEIGHT_CAROUSEL), COLOR_BG)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()

    # Header
    draw.rectangle([(0, 0), (WIDTH_CAROUSEL, 380)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 370), (WIDTH_CAROUSEL, 380)], fill=COLOR_ACCENT)

    text = "JANEIRO 2026"
    draw.text((center_text(draw, text, fonts['title']), 60), text, fill=COLOR_ACCENT, font=fonts['title'])

    text = "O MÊS DO RECOMEÇO"
    draw.text((center_text(draw, text, fonts['subtitle']), 160), text, fill=COLOR_TEXT_LIGHT, font=fonts['subtitle'])

    draw.rectangle([(WIDTH_CAROUSEL//2 - 150, 250), (WIDTH_CAROUSEL//2 + 150, 255)], fill=COLOR_ACCENT)

    text = "KITS CORPORATIVOS"
    draw.text((center_text(draw, text, fonts['subtitle']), 285), text, fill=COLOR_TEXT_LIGHT, font=fonts['subtitle'])

    y_pos = 420

    text = "TRANSFORME A"
    draw.text((center_text(draw, text, fonts['subtitle']), y_pos), text, fill=COLOR_PRIMARY, font=fonts['subtitle'])

    text = "PRIMEIRA IMPRESSÃO"
    draw.text((center_text(draw, text, fonts['subtitle']), y_pos + 60), text, fill=COLOR_PRIMARY, font=fonts['subtitle'])

    # Box principal
    draw.rectangle([(80, y_pos + 150), (WIDTH_CAROUSEL - 80, y_pos + 280)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=4)

    text = "Brindes de Alto Impacto"
    draw.text((center_text(draw, text, fonts['highlight']), y_pos + 175),
              text, fill=COLOR_ACCENT, font=fonts['highlight'])

    text = "para Onboarding e Volta ao Trabalho"
    draw.text((center_text(draw, text, fonts['body']), y_pos + 225),
              text, fill=COLOR_TEXT_LIGHT, font=fonts['body'])

    # Footer - SEM TEXTO (espaço para logo manual)
    draw.rectangle([(0, 950), (WIDTH_CAROUSEL, HEIGHT_CAROUSEL)], fill=COLOR_PRIMARY)

    # Setas
    text = "→ → →"
    draw.text((center_text(draw, text, fonts['highlight']), 970), text, fill=COLOR_ACCENT, font=fonts['highlight'])

    return img

def create_carousel_slide_2():
    """Slide 2 - SEM texto no rodapé"""
    img = Image.new('RGB', (WIDTH_CAROUSEL, HEIGHT_CAROUSEL), COLOR_BG)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()

    draw.rectangle([(0, 0), (WIDTH_CAROUSEL, 380)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 370), (WIDTH_CAROUSEL, 380)], fill=COLOR_ACCENT)

    text = "KIT ONBOARDING"
    draw.text((center_text(draw, text, fonts['title']), 100), text, fill=COLOR_ACCENT, font=fonts['title'])

    text = "Receba com Excelência"
    draw.text((center_text(draw, text, fonts['body']), 220), text, fill=COLOR_TEXT_LIGHT, font=fonts['body'])

    draw.rectangle([(WIDTH_CAROUSEL//2 - 180, 290), (WIDTH_CAROUSEL//2 + 180, 295)], fill=COLOR_ACCENT)

    y_pos = 420
    padding = 90

    items = [
        "✓ Garrafa Térmica Premium",
        "✓ Caderno Executivo",
        "✓ Caneta Premium",
        "✓ Ecobag Personalizada",
        "✓ Tag Personalizada",
    ]

    for i, item in enumerate(items):
        draw.rectangle([(padding, y_pos + (i * 85)), (WIDTH_CAROUSEL - padding, y_pos + (i * 85) + 70)],
                       fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=2)
        draw.text((padding + 30, y_pos + (i * 85) + 20), item, fill=COLOR_TEXT_LIGHT, font=fonts['body'])

    # Footer - SEM TEXTO
    draw.rectangle([(0, 950), (WIDTH_CAROUSEL, HEIGHT_CAROUSEL)], fill=COLOR_PRIMARY)

    text = "100% PERSONALIZÁVEL"
    draw.text((center_text(draw, text, fonts['highlight']), 890), text, fill=COLOR_ACCENT, font=fonts['highlight'])

    text = "→ → →"
    draw.text((center_text(draw, text, fonts['small']), 970), text, fill=COLOR_ACCENT, font=fonts['small'])

    return img

def create_carousel_slide_3():
    """Slide 3 - SEM texto no rodapé"""
    img = Image.new('RGB', (WIDTH_CAROUSEL, HEIGHT_CAROUSEL), COLOR_BG)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()

    draw.rectangle([(0, 0), (WIDTH_CAROUSEL, 380)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 370), (WIDTH_CAROUSEL, 380)], fill=COLOR_ACCENT)

    text = "KIT VOLTA AO"
    draw.text((center_text(draw, text, fonts['title']), 80), text, fill=COLOR_ACCENT, font=fonts['title'])

    text = "TRABALHO"
    draw.text((center_text(draw, text, fonts['title']), 160), text, fill=COLOR_ACCENT, font=fonts['title'])

    text = "Reengaje seu Time"
    draw.text((center_text(draw, text, fonts['body']), 270), text, fill=COLOR_TEXT_LIGHT, font=fonts['body'])

    draw.rectangle([(WIDTH_CAROUSEL//2 - 180, 330), (WIDTH_CAROUSEL//2 + 180, 335)], fill=COLOR_ACCENT)

    y_pos = 420
    padding = 90

    items = [
        "✓ Moleskine",
        "✓ Squeeze Personalizado",
        "✓ Mousepad Premium",
        "✓ Bloco de Notas",
        "✓ Caneta",
    ]

    for i, item in enumerate(items):
        draw.rectangle([(padding, y_pos + (i * 85)), (WIDTH_CAROUSEL - padding, y_pos + (i * 85) + 70)],
                       fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=2)
        draw.text((padding + 30, y_pos + (i * 85) + 20), item, fill=COLOR_TEXT_LIGHT, font=fonts['body'])

    # Footer - SEM TEXTO
    draw.rectangle([(0, 950), (WIDTH_CAROUSEL, HEIGHT_CAROUSEL)], fill=COLOR_PRIMARY)

    text = "FORTALEÇA O ENGAJAMENTO"
    draw.text((center_text(draw, text, fonts['highlight']), 890), text, fill=COLOR_ACCENT, font=fonts['highlight'])

    text = "→ → →"
    draw.text((center_text(draw, text, fonts['small']), 970), text, fill=COLOR_ACCENT, font=fonts['small'])

    return img

def create_carousel_slide_4():
    """Slide 4 - SEM texto no rodapé"""
    img = Image.new('RGB', (WIDTH_CAROUSEL, HEIGHT_CAROUSEL), COLOR_BG)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()

    draw.rectangle([(0, 0), (WIDTH_CAROUSEL, 380)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 370), (WIDTH_CAROUSEL, 380)], fill=COLOR_ACCENT)

    text = "POR QUE ESCOLHER"
    draw.text((center_text(draw, text, fonts['subtitle']), 50), text, fill=COLOR_TEXT_LIGHT, font=fonts['subtitle'])

    text = "BRINDES"
    draw.text((center_text(draw, text, fonts['subtitle']), 115), text, fill=COLOR_ACCENT, font=fonts['subtitle'])

    text = "MARCELO E WAGNER?"
    draw.text((center_text(draw, text, fonts['subtitle']), 175), text, fill=COLOR_ACCENT, font=fonts['subtitle'])

    draw.rectangle([(WIDTH_CAROUSEL//2 - 250, 250), (WIDTH_CAROUSEL//2 + 250, 255)], fill=COLOR_ACCENT)

    # Box dourado
    draw.rectangle([(60, 280), (WIDTH_CAROUSEL - 60, 390)],
                   fill=COLOR_ACCENT, outline=COLOR_ACCENT, width=3)

    font_box = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)

    text = "Especialistas em"
    draw.text((center_text(draw, text, font_box), 300), text, fill=COLOR_PRIMARY, font=font_box)

    text = "Grandes Agências"
    draw.text((center_text(draw, text, font_box), 345), text, fill=COLOR_PRIMARY, font=font_box)

    # Credenciais
    y_pos = 420

    draw.rectangle([(100, y_pos), (WIDTH_CAROUSEL - 100, y_pos + 70)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "+10.000 CLIENTES"
    draw.text((center_text(draw, text, fonts['highlight']), y_pos + 20), text, fill=COLOR_ACCENT, font=fonts['highlight'])

    y_pos += 90
    draw.rectangle([(100, y_pos), (WIDTH_CAROUSEL - 100, y_pos + 70)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "+20 ANOS DE MERCADO"
    draw.text((center_text(draw, text, fonts['highlight']), y_pos + 20), text, fill=COLOR_ACCENT, font=fonts['highlight'])

    y_pos += 90
    draw.rectangle([(100, y_pos), (WIDTH_CAROUSEL - 100, y_pos + 70)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "ENTREGAS TODO BRASIL"
    draw.text((center_text(draw, text, fonts['highlight']), y_pos + 20), text, fill=COLOR_ACCENT, font=fonts['highlight'])

    # Footer - SEM TEXTO (apenas espaço para logo)
    draw.rectangle([(0, 950), (WIDTH_CAROUSEL, HEIGHT_CAROUSEL)], fill=COLOR_PRIMARY)

    # Ícones redes sociais
    text_ig = "📷 @brindesmarceloewagner"
    draw.text((80, 975), text_ig, fill=COLOR_TEXT_LIGHT, font=fonts['small'])

    text_site = "🌐 brindesmarceloewagner.com.br"
    bbox = draw.textbbox((0, 0), text_site, font=fonts['tiny'])
    draw.text((WIDTH_CAROUSEL - (bbox[2] - bbox[0]) - 80, 980), text_site, fill=COLOR_TEXT_LIGHT, font=fonts['tiny'])

    return img

# === BANNER PARA SITE ===

def create_banner_site():
    """Banner 2000x600px para site"""
    img = Image.new('RGB', (WIDTH_BANNER, HEIGHT_BANNER), COLOR_PRIMARY)
    draw = ImageDraw.Draw(img)

    # Fontes para banner
    font_title_banner = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
    font_subtitle_banner = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
    font_body_banner = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    font_cta_banner = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)

    # Linha dourada superior
    draw.rectangle([(0, 0), (WIDTH_BANNER, 15)], fill=COLOR_ACCENT)

    # Título
    text = "JANEIRO 2026"
    x = center_text(draw, text, font_title_banner, WIDTH_BANNER)
    draw.text((x, 40), text, fill=COLOR_ACCENT, font=font_title_banner)

    text = "O MÊS DO RECOMEÇO"
    x = center_text(draw, text, font_subtitle_banner, WIDTH_BANNER)
    draw.text((x, 150), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle_banner)

    # Linha decorativa
    draw.rectangle([(WIDTH_BANNER//2 - 200, 230), (WIDTH_BANNER//2 + 200, 235)], fill=COLOR_ACCENT)

    text = "KITS CORPORATIVOS"
    x = center_text(draw, text, font_subtitle_banner, WIDTH_BANNER)
    draw.text((x, 250), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle_banner)

    # Boxes informativos lado a lado
    box_width = 400
    box_height = 100
    gap = 80
    start_x = (WIDTH_BANNER - (2 * box_width + gap)) // 2
    y_boxes = 360

    # Box 1: Kit Onboarding
    draw.rectangle([(start_x, y_boxes), (start_x + box_width, y_boxes + box_height)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "✓ KIT ONBOARDING"
    bbox = draw.textbbox((0, 0), text, font=font_body_banner)
    text_x = start_x + (box_width - (bbox[2] - bbox[0])) // 2
    draw.text((text_x, y_boxes + 30), text, fill=COLOR_TEXT_LIGHT, font=font_body_banner)

    # Box 2: Kit Volta ao Trabalho
    start_x2 = start_x + box_width + gap
    draw.rectangle([(start_x2, y_boxes), (start_x2 + box_width, y_boxes + box_height)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "✓ KIT VOLTA AO TRABALHO"
    bbox = draw.textbbox((0, 0), text, font=font_body_banner)
    text_x = start_x2 + (box_width - (bbox[2] - bbox[0])) // 2
    draw.text((text_x, y_boxes + 30), text, fill=COLOR_TEXT_LIGHT, font=font_body_banner)

    # CTA - Botão WhatsApp
    cta_y = 490

    # Botão estilizado
    button_width = 600
    button_height = 80
    button_x = (WIDTH_BANNER - button_width) // 2

    draw.rectangle([(button_x, cta_y), (button_x + button_width, cta_y + button_height)],
                   fill=COLOR_ACCENT, outline=COLOR_ACCENT, width=0)

    text = "📱 SOLICITE SEU ORÇAMENTO"
    bbox = draw.textbbox((0, 0), text, font=font_cta_banner)
    text_x = button_x + (button_width - (bbox[2] - bbox[0])) // 2
    draw.text((text_x, cta_y + 17), text, fill=COLOR_PRIMARY, font=font_cta_banner)

    # Linha dourada inferior
    draw.rectangle([(0, HEIGHT_BANNER - 15), (WIDTH_BANNER, HEIGHT_BANNER)], fill=COLOR_ACCENT)

    return img

def create_all():
    """Cria todas as artes"""

    print("🎨 Criando Carrossel (1080x1080px)...")
    carousel_slides = [
        ("slide_1_capa.png", create_carousel_slide_1()),
        ("slide_2_kit_onboarding.png", create_carousel_slide_2()),
        ("slide_3_kit_volta_trabalho.png", create_carousel_slide_3()),
        ("slide_4_credenciais.png", create_carousel_slide_4()),
    ]

    for filename, img in carousel_slides:
        path = f"/home/user/github/assets/posts/{filename}"
        img.save(path, quality=95)
        print(f"  ✅ {filename}")

    print(f"\n🌐 Criando Banner Site (2000x600px)...")
    banner = create_banner_site()
    banner_path = "/home/user/github/assets/posts/banner_site_2000x600.png"
    banner.save(banner_path, quality=95)
    print(f"  ✅ banner_site_2000x600.png")

    print(f"\n🎉 CONCLUÍDO!")
    print(f"📁 Carrossel: 4 slides SEM texto no rodapé (espaço para logo manual)")
    print(f"📁 Banner: 2000x600px com CTA para WhatsApp")
    print(f"\n📲 WhatsApp: (31) 3446-0908")

if __name__ == "__main__":
    create_all()
