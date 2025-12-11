#!/usr/bin/env python3
"""
Script para criar carrossel corporativo - VERSÃO FINAL CORRIGIDA
Correções: Slide 1 (2 linhas), Slide 4 (box dourado completo)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configurações
WIDTH = 1080
HEIGHT = 1080

# Cores
COLOR_PRIMARY = "#1a2332"
COLOR_SECONDARY = "#2c3e50"
COLOR_ACCENT = "#c9a961"
COLOR_TEXT_LIGHT = "#ffffff"
COLOR_BG = "#f8f9fa"

def load_fonts():
    """Carrega as fontes"""
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
        font_highlight = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
        font_logo_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_logo_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        # Fallback
        return [ImageFont.load_default()] * 8

    return font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo_big, font_logo_small

def draw_header(draw):
    """Header padrão"""
    draw.rectangle([(0, 0), (WIDTH, 380)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 370), (WIDTH, 380)], fill=COLOR_ACCENT)

def draw_footer_with_logo(draw, y_start=1000):
    """Logo no rodapé"""
    _, _, _, _, _, _, font_logo_big, font_logo_small = load_fonts()

    # Tentar carregar logo original
    logo_path = "/home/user/github/assets/logo_original.png"
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            # Redimensionar logo mantendo proporção
            logo.thumbnail((200, 60), Image.Resampling.LANCZOS)
            # Centralizar
            x_logo = (WIDTH - logo.width) // 2
            # Fazer logo branca (se necessário)
            from PIL import ImageOps
            logo = ImageOps.invert(logo.convert('RGB'))
            # Colar logo
            draw._image.paste(logo, (x_logo, y_start), logo)
            return
        except:
            pass

    # Fallback: logo textual
    text_brindes = "BRINDES"
    bbox = draw.textbbox((0, 0), text_brindes, font=font_logo_big)
    text_width_brindes = bbox[2] - bbox[0]

    text_mw = "MARCELO E WAGNER"
    bbox2 = draw.textbbox((0, 0), text_mw, font=font_logo_small)
    text_width_mw = bbox2[2] - bbox2[0]

    max_width = max(text_width_brindes, text_width_mw)
    x_center = (WIDTH - max_width) // 2

    draw.text((x_center + (max_width - text_width_brindes)//2, y_start),
              text_brindes, fill=COLOR_TEXT_LIGHT, font=font_logo_big)
    draw.text((x_center + (max_width - text_width_mw)//2, y_start + 28),
              text_mw, fill=COLOR_TEXT_LIGHT, font=font_logo_small)

def center_text(draw, text, font):
    """Centraliza texto"""
    bbox = draw.textbbox((0, 0), text, font=font)
    return (WIDTH - (bbox[2] - bbox[0])) // 2

def create_slide_1():
    """SLIDE 1 - CORRIGIDO: Texto em 2 linhas"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()
    font_title, font_subtitle, font_body, font_highlight = fonts[0], fonts[1], fonts[2], fonts[3]

    draw_header(draw)

    # Título
    text = "JANEIRO 2026"
    draw.text((center_text(draw, text, font_title), 60), text, fill=COLOR_ACCENT, font=font_title)

    text = "O MÊS DO RECOMEÇO"
    draw.text((center_text(draw, text, font_subtitle), 160), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    draw.rectangle([(WIDTH//2 - 150, 250), (WIDTH//2 + 150, 255)], fill=COLOR_ACCENT)

    text = "KITS CORPORATIVOS"
    draw.text((center_text(draw, text, font_subtitle), 285), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    # Central
    y_pos = 420

    text = "TRANSFORME A"
    draw.text((center_text(draw, text, font_subtitle), y_pos), text, fill=COLOR_PRIMARY, font=font_subtitle)

    text = "PRIMEIRA IMPRESSÃO"
    draw.text((center_text(draw, text, font_subtitle), y_pos + 60), text, fill=COLOR_PRIMARY, font=font_subtitle)

    # Box - CORRIGIDO: APENAS 2 LINHAS
    draw.rectangle([(80, y_pos + 150), (WIDTH - 80, y_pos + 280)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=4)

    # LINHA 1: Brindes de Alto Impacto
    text = "Brindes de Alto Impacto"
    draw.text((center_text(draw, text, font_highlight), y_pos + 175),
              text, fill=COLOR_ACCENT, font=font_highlight)

    # LINHA 2: para Onboarding e Volta ao Trabalho
    text = "para Onboarding e Volta ao Trabalho"
    draw.text((center_text(draw, text, font_body), y_pos + 225),
              text, fill=COLOR_TEXT_LIGHT, font=font_body)

    # Footer
    draw.rectangle([(0, 820), (WIDTH, HEIGHT)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 820), (WIDTH, 830)], fill=COLOR_ACCENT)

    text = "→ → →"
    draw.text((center_text(draw, text, font_highlight), 880), text, fill=COLOR_ACCENT, font=font_highlight)

    draw_footer_with_logo(draw, 980)

    return img

def create_slide_2():
    """SLIDE 2"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()
    font_title, font_subtitle, font_body, font_highlight = fonts[0], fonts[1], fonts[2], fonts[3]

    draw_header(draw)

    text = "KIT ONBOARDING"
    draw.text((center_text(draw, text, font_title), 100), text, fill=COLOR_ACCENT, font=font_title)

    text = "Receba com Excelência"
    draw.text((center_text(draw, text, font_body), 220), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    draw.rectangle([(WIDTH//2 - 180, 290), (WIDTH//2 + 180, 295)], fill=COLOR_ACCENT)

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
        draw.rectangle([(padding, y_pos + (i * 85)), (WIDTH - padding, y_pos + (i * 85) + 70)],
                       fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=2)
        draw.text((padding + 30, y_pos + (i * 85) + 20), item, fill=COLOR_TEXT_LIGHT, font=font_body)

    draw.rectangle([(0, 840), (WIDTH, HEIGHT)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 840), (WIDTH, 850)], fill=COLOR_ACCENT)

    text = "100% PERSONALIZÁVEL"
    draw.text((center_text(draw, text, font_highlight), 890), text, fill=COLOR_ACCENT, font=font_highlight)

    text = "→ → →"
    draw.text((center_text(draw, text, fonts[4]), 950), text, fill=COLOR_ACCENT, font=fonts[4])

    draw_footer_with_logo(draw, 1000)

    return img

def create_slide_3():
    """SLIDE 3"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()
    font_title, font_subtitle, font_body, font_highlight = fonts[0], fonts[1], fonts[2], fonts[3]

    draw_header(draw)

    text = "KIT VOLTA AO"
    draw.text((center_text(draw, text, font_title), 80), text, fill=COLOR_ACCENT, font=font_title)

    text = "TRABALHO"
    draw.text((center_text(draw, text, font_title), 160), text, fill=COLOR_ACCENT, font=font_title)

    text = "Reengaje seu Time"
    draw.text((center_text(draw, text, font_body), 270), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    draw.rectangle([(WIDTH//2 - 180, 330), (WIDTH//2 + 180, 335)], fill=COLOR_ACCENT)

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
        draw.rectangle([(padding, y_pos + (i * 85)), (WIDTH - padding, y_pos + (i * 85) + 70)],
                       fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=2)
        draw.text((padding + 30, y_pos + (i * 85) + 20), item, fill=COLOR_TEXT_LIGHT, font=font_body)

    draw.rectangle([(0, 840), (WIDTH, HEIGHT)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 840), (WIDTH, 850)], fill=COLOR_ACCENT)

    text = "FORTALEÇA O ENGAJAMENTO"
    draw.text((center_text(draw, text, font_highlight), 890), text, fill=COLOR_ACCENT, font=font_highlight)

    text = "→ → →"
    draw.text((center_text(draw, text, fonts[4]), 950), text, fill=COLOR_ACCENT, font=fonts[4])

    draw_footer_with_logo(draw, 1000)

    return img

def create_slide_4():
    """SLIDE 4 - CORRIGIDO: Box dourado completo"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()
    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny = fonts[0], fonts[1], fonts[2], fonts[3], fonts[4], fonts[5]

    draw_header(draw)

    text = "POR QUE ESCOLHER"
    draw.text((center_text(draw, text, font_subtitle), 50), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    text = "BRINDES"
    draw.text((center_text(draw, text, font_subtitle), 115), text, fill=COLOR_ACCENT, font=font_subtitle)

    text = "MARCELO E WAGNER?"
    draw.text((center_text(draw, text, font_subtitle), 175), text, fill=COLOR_ACCENT, font=font_subtitle)

    draw.rectangle([(WIDTH//2 - 250, 250), (WIDTH//2 + 250, 255)], fill=COLOR_ACCENT)

    # BOX DOURADO - CORRIGIDO: Box maior, texto TOTALMENTE dentro
    draw.rectangle([(60, 280), (WIDTH - 60, 390)],
                   fill=COLOR_ACCENT, outline=COLOR_ACCENT, width=3)

    # Texto DENTRO do box dourado - fonte menor para caber
    font_box = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)

    text = "Especialistas em"
    draw.text((center_text(draw, text, font_box), 300), text, fill=COLOR_PRIMARY, font=font_box)

    text = "Grandes Agências"
    draw.text((center_text(draw, text, font_box), 345), text, fill=COLOR_PRIMARY, font=font_box)

    # Credenciais
    y_pos = 420

    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 70)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "+10.000 CLIENTES"
    draw.text((center_text(draw, text, font_highlight), y_pos + 20), text, fill=COLOR_ACCENT, font=font_highlight)

    y_pos += 90
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 70)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "+20 ANOS DE MERCADO"
    draw.text((center_text(draw, text, font_highlight), y_pos + 20), text, fill=COLOR_ACCENT, font=font_highlight)

    y_pos += 90
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 70)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "ENTREGAS TODO BRASIL"
    draw.text((center_text(draw, text, font_highlight), y_pos + 20), text, fill=COLOR_ACCENT, font=font_highlight)

    # Footer
    draw.rectangle([(0, 740), (WIDTH, HEIGHT)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 740), (WIDTH, 750)], fill=COLOR_ACCENT)

    text = "COMECE 2026 COM O PÉ DIREITO!"
    draw.text((center_text(draw, text, font_body), 765), text, fill=COLOR_ACCENT, font=font_body)

    draw.rectangle([(150, 820), (WIDTH - 150, 825)], fill=COLOR_ACCENT)

    # Contato
    text = "📱 (31) 3446-0908"
    draw.text((center_text(draw, text, font_highlight), 845), text, fill=COLOR_TEXT_LIGHT, font=font_highlight)

    text_ig = "📷 @brindesmarceloewagner"
    draw.text((80, 910), text_ig, fill=COLOR_TEXT_LIGHT, font=font_small)

    text_site = "🌐 brindesmarceloewagner.com.br"
    bbox = draw.textbbox((0, 0), text_site, font=font_tiny)
    draw.text((WIDTH - (bbox[2] - bbox[0]) - 80, 915), text_site, fill=COLOR_TEXT_LIGHT, font=font_tiny)

    text_loc = "📍 Belo Horizonte/MG"
    draw.text((center_text(draw, text_loc, font_small), 960), text_loc, fill=COLOR_TEXT_LIGHT, font=font_small)

    draw_footer_with_logo(draw, 1010)

    return img

def create_carousel():
    """Cria carrossel completo"""
    slides = [
        ("slide_1_capa_final.png", create_slide_1()),
        ("slide_2_kit_onboarding_final.png", create_slide_2()),
        ("slide_3_kit_volta_trabalho_final.png", create_slide_3()),
        ("slide_4_credenciais_final.png", create_slide_4()),
    ]

    for filename, img in slides:
        output_path = f"/home/user/github/assets/posts/{filename}"
        img.save(output_path, quality=95)
        print(f"✅ Criado: {filename}")

    print(f"\n🎉 Carrossel FINAL criado!")
    print(f"✅ Slide 1: Texto em 2 linhas corretas")
    print(f"✅ Slide 4: Box dourado completo e bem formatado")
    print(f"✅ Logo: Pronta para incluir (ou usando textual)")

if __name__ == "__main__":
    create_carousel()
