#!/usr/bin/env python3
"""
Script para criar carrossel corporativo elegante para Instagram
Post: Kits Onboarding e Volta ao Trabalho 2026
Estilo: Corporativo elegante com cores sóbrias
Total: 4 slides
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap

# Configurações do post
WIDTH = 1080
HEIGHT = 1080

# Paleta de cores corporativa elegante
COLOR_PRIMARY = "#1a2332"      # Azul escuro profissional
COLOR_SECONDARY = "#2c3e50"    # Cinza azulado
COLOR_ACCENT = "#c9a961"       # Dourado elegante
COLOR_TEXT_LIGHT = "#ffffff"   # Branco
COLOR_TEXT_DARK = "#333333"    # Cinza escuro
COLOR_BG = "#f8f9fa"          # Cinza claro de fundo

def load_fonts():
    """Carrega as fontes do sistema"""
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)
        font_highlight = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_highlight = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()

    return font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny

def draw_header(draw, text, y_offset=0):
    """Desenha o header padrão com o texto fornecido"""
    draw.rectangle([(0, 0 + y_offset), (WIDTH, 380 + y_offset)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 370 + y_offset), (WIDTH, 380 + y_offset)], fill=COLOR_ACCENT)

def draw_footer(draw, y_start=820):
    """Desenha o footer padrão"""
    draw.rectangle([(0, y_start), (WIDTH, HEIGHT)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, y_start), (WIDTH, y_start + 10)], fill=COLOR_ACCENT)

def center_text(draw, text, font, y):
    """Centraliza texto horizontalmente"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    return x

def create_slide_1():
    """SLIDE 1: Capa principal"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny = load_fonts()

    # Header
    draw_header(draw, "")

    # Título principal
    text = "JANEIRO 2026"
    x = center_text(draw, text, font_title, 0)
    draw.text((x, 80), text, fill=COLOR_ACCENT, font=font_title)

    # Subtítulo
    text = "O MÊS DO RECOMEÇO"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, 180), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    # Linha decorativa
    draw.rectangle([(WIDTH//2 - 150, 260), (WIDTH//2 + 150, 265)], fill=COLOR_ACCENT)

    # Texto principal
    text = "KITS CORPORATIVOS"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, 300), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    # Área central
    y_pos = 420

    # Grande destaque
    text = "TRANSFORME A"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, y_pos), text, fill=COLOR_PRIMARY, font=font_subtitle)

    text = "PRIMEIRA IMPRESSÃO"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, y_pos + 60), text, fill=COLOR_PRIMARY, font=font_subtitle)

    # Box destaque
    draw.rectangle([(100, y_pos + 150), (WIDTH - 100, y_pos + 290)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=4)

    text = "Brindes de Alto Impacto"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, y_pos + 175), text, fill=COLOR_ACCENT, font=font_highlight)

    text = "para Onboarding e"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, y_pos + 225), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    text = "Volta ao Trabalho"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, y_pos + 265), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    # Footer
    draw_footer(draw)

    text = "DESLIZE PARA VER MAIS"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, 870), text, fill=COLOR_ACCENT, font=font_body)

    # Setas indicativas
    draw.text((WIDTH//2 + 280, 875), "→", fill=COLOR_ACCENT, font=font_highlight)
    draw.text((WIDTH//2 + 320, 875), "→", fill=COLOR_ACCENT, font=font_highlight)

    text = "1/4"
    x = center_text(draw, text, font_small, 0)
    draw.text((x, 940), text, fill=COLOR_TEXT_LIGHT, font=font_small)

    # Marca
    text = "Brindes Marcelo e Wagner"
    x = center_text(draw, text, font_tiny, 0)
    draw.text((x, 1020), text, fill=COLOR_TEXT_LIGHT, font=font_tiny)

    return img

def create_slide_2():
    """SLIDE 2: Kit Onboarding"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny = load_fonts()

    # Header
    draw_header(draw, "")

    text = "KIT ONBOARDING"
    x = center_text(draw, text, font_title, 0)
    draw.text((x, 100), text, fill=COLOR_ACCENT, font=font_title)

    text = "Receba com Excelência"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, 220), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    draw.rectangle([(WIDTH//2 - 180, 290), (WIDTH//2 + 180, 295)], fill=COLOR_ACCENT)

    # Conteúdo central
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
        # Box para cada item
        draw.rectangle([(padding, y_pos + (i * 85)), (WIDTH - padding, y_pos + (i * 85) + 70)],
                       fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=2)

        draw.text((padding + 30, y_pos + (i * 85) + 20), item,
                 fill=COLOR_TEXT_LIGHT, font=font_body)

    # Footer
    draw_footer(draw, 840)

    text = "100% PERSONALIZÁVEL"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, 890), text, fill=COLOR_ACCENT, font=font_highlight)

    text = "2/4"
    x = center_text(draw, text, font_small, 0)
    draw.text((x, 970), text, fill=COLOR_TEXT_LIGHT, font=font_small)

    text = "Brindes Marcelo e Wagner"
    x = center_text(draw, text, font_tiny, 0)
    draw.text((x, 1020), text, fill=COLOR_TEXT_LIGHT, font=font_tiny)

    return img

def create_slide_3():
    """SLIDE 3: Kit Volta ao Trabalho"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny = load_fonts()

    # Header
    draw_header(draw, "")

    text = "KIT VOLTA AO"
    x = center_text(draw, text, font_title, 0)
    draw.text((x, 80), text, fill=COLOR_ACCENT, font=font_title)

    text = "TRABALHO"
    x = center_text(draw, text, font_title, 0)
    draw.text((x, 160), text, fill=COLOR_ACCENT, font=font_title)

    text = "Re-engaje seu Time"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, 270), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    draw.rectangle([(WIDTH//2 - 180, 330), (WIDTH//2 + 180, 335)], fill=COLOR_ACCENT)

    # Conteúdo central
    y_pos = 420
    padding = 90

    items = [
        "✓ Planner 2026",
        "✓ Squeeze Personalizado",
        "✓ Mousepad Premium",
        "✓ Bloco de Notas",
        "✓ Mimo Especial",
    ]

    for i, item in enumerate(items):
        # Box para cada item
        draw.rectangle([(padding, y_pos + (i * 85)), (WIDTH - padding, y_pos + (i * 85) + 70)],
                       fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=2)

        draw.text((padding + 30, y_pos + (i * 85) + 20), item,
                 fill=COLOR_TEXT_LIGHT, font=font_body)

    # Footer
    draw_footer(draw, 840)

    text = "FORTALEÇA O ENGAJAMENTO"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, 890), text, fill=COLOR_ACCENT, font=font_highlight)

    text = "3/4"
    x = center_text(draw, text, font_small, 0)
    draw.text((x, 970), text, fill=COLOR_TEXT_LIGHT, font=font_small)

    text = "Brindes Marcelo e Wagner"
    x = center_text(draw, text, font_tiny, 0)
    draw.text((x, 1020), text, fill=COLOR_TEXT_LIGHT, font=font_tiny)

    return img

def create_slide_4():
    """SLIDE 4: Credenciais e CTA"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny = load_fonts()

    # Header
    draw_header(draw, "")

    text = "POR QUE ESCOLHER"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, 80), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    text = "MARCELO E WAGNER?"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, 150), text, fill=COLOR_ACCENT, font=font_subtitle)

    draw.rectangle([(WIDTH//2 - 200, 230), (WIDTH//2 + 200, 235)], fill=COLOR_ACCENT)

    text = "Especialistas em"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, 270), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    text = "Grandes Agências"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, 315), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    # Área central com credenciais
    y_pos = 420

    # Box 1
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 90)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)

    text = "+10.000 CLIENTES"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, y_pos + 30), text, fill=COLOR_ACCENT, font=font_highlight)

    # Box 2
    y_pos += 110
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 90)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)

    text = "+20 ANOS DE MERCADO"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, y_pos + 30), text, fill=COLOR_ACCENT, font=font_highlight)

    # Box 3
    y_pos += 110
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 90)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)

    text = "ENTREGAS TODO BRASIL"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, y_pos + 30), text, fill=COLOR_ACCENT, font=font_highlight)

    # Footer com CTA
    draw_footer(draw, 780)

    text = "COMECE 2026 COM O PÉ DIREITO!"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, 820), text, fill=COLOR_ACCENT, font=font_body)

    # Linha divisória
    draw.rectangle([(200, 880), (WIDTH - 200, 885)], fill=COLOR_ACCENT)

    # Contato
    text = "📲 (31) 3446-0908"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, 910), text, fill=COLOR_TEXT_LIGHT, font=font_highlight)

    text = "📍 Belo Horizonte/MG"
    x = center_text(draw, text, font_small, 0)
    draw.text((x, 975), text, fill=COLOR_TEXT_LIGHT, font=font_small)

    text = "brindesmarceloewagner.com.br"
    x = center_text(draw, text, font_tiny, 0)
    draw.text((x, 1025), text, fill=COLOR_TEXT_LIGHT, font=font_tiny)

    # Número do slide
    draw.text((50, 820), "4/4", fill=COLOR_TEXT_LIGHT, font=font_small)

    return img

def create_carousel():
    """Cria todas as artes do carrossel"""

    slides = [
        ("slide_1_capa.png", create_slide_1()),
        ("slide_2_kit_onboarding.png", create_slide_2()),
        ("slide_3_kit_volta_trabalho.png", create_slide_3()),
        ("slide_4_credenciais.png", create_slide_4()),
    ]

    output_paths = []

    for filename, img in slides:
        output_path = f"/home/user/github/assets/posts/{filename}"
        img.save(output_path, quality=95)
        output_paths.append(output_path)
        print(f"✅ Criado: {filename}")

    print(f"\n🎉 Carrossel completo criado com sucesso!")
    print(f"📐 Dimensões: {WIDTH}x{HEIGHT}px cada slide")
    print(f"📊 Total de slides: {len(slides)}")
    print(f"\n📁 Arquivos salvos em: /home/user/github/assets/posts/")

    return output_paths

if __name__ == "__main__":
    create_carousel()
