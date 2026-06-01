#!/usr/bin/env python3
"""
Script para criar arte corporativa elegante para Instagram
Post: Kits Onboarding e Volta ao Trabalho
Estilo: Corporativo elegante com cores sóbrias
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

def create_instagram_post():
    """Cria a arte do Instagram"""

    # Criar imagem base
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # === SEÇÃO SUPERIOR (Header) ===
    # Retângulo superior azul escuro
    draw.rectangle([(0, 0), (WIDTH, 380)], fill=COLOR_PRIMARY)

    # Linha de acento dourada
    draw.rectangle([(0, 370), (WIDTH, 380)], fill=COLOR_ACCENT)

    # === TÍTULO PRINCIPAL ===
    try:
        # Tentar fontes do sistema
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)
        font_highlight = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_highlight = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Título "JANEIRO 2025"
    text = "JANEIRO 2025"
    bbox = draw.textbbox((0, 0), text, font=font_title)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, 60), text, fill=COLOR_ACCENT, font=font_title)

    # Subtítulo
    text = "O MÊS DO RECOMEÇO"
    bbox = draw.textbbox((0, 0), text, font=font_subtitle)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, 150), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    # Linha decorativa
    draw.rectangle([(WIDTH//2 - 150, 230), (WIDTH//2 + 150, 235)], fill=COLOR_ACCENT)

    # Destaque principal
    text = "KITS CORPORATIVOS"
    bbox = draw.textbbox((0, 0), text, font=font_subtitle)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, 270), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    # === SEÇÃO CENTRAL (Conteúdo) ===
    y_pos = 420
    padding = 80

    # Box de destaque 1
    draw.rectangle([(padding, y_pos), (WIDTH - padding, y_pos + 100)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)

    text = "✓ KIT ONBOARDING"
    draw.text((padding + 30, y_pos + 35), text, fill=COLOR_TEXT_LIGHT, font=font_highlight)

    y_pos += 130

    # Box de destaque 2
    draw.rectangle([(padding, y_pos), (WIDTH - padding, y_pos + 100)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)

    text = "✓ KIT VOLTA AO TRABALHO"
    draw.text((padding + 30, y_pos + 35), text, fill=COLOR_TEXT_LIGHT, font=font_highlight)

    y_pos += 150

    # Texto de valor
    text = "100% PERSONALIZADOS"
    bbox = draw.textbbox((0, 0), text, font=font_highlight)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, y_pos), text, fill=COLOR_PRIMARY, font=font_highlight)

    y_pos += 60

    # === SEÇÃO INFERIOR (Credenciais) ===
    # Fundo inferior
    draw.rectangle([(0, 820), (WIDTH, HEIGHT)], fill=COLOR_PRIMARY)

    # Linha dourada superior
    draw.rectangle([(0, 820), (WIDTH, 830)], fill=COLOR_ACCENT)

    # Prova social
    text = "+10.000 CLIENTES | +20 ANOS"
    bbox = draw.textbbox((0, 0), text, font=font_highlight)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, 855), text, fill=COLOR_ACCENT, font=font_highlight)

    # Especialização
    text = "Especialistas em Grandes Agências"
    bbox = draw.textbbox((0, 0), text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, 925), text, fill=COLOR_TEXT_LIGHT, font=font_small)

    # Contato
    text = "📲 (31) 3446-0908"
    bbox = draw.textbbox((0, 0), text, font=font_body)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, 980), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    # Localização
    text = "BH/MG • Entregas em todo Brasil 🚚"
    bbox = draw.textbbox((0, 0), text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, 1025), text, fill=COLOR_TEXT_LIGHT, font=font_small)

    # Salvar imagem
    output_path = "/home/user/github/assets/posts/kit_onboarding_2025.png"
    img.save(output_path, quality=95)
    print(f"✅ Arte criada com sucesso: {output_path}")
    print(f"📐 Dimensões: {WIDTH}x{HEIGHT}px (formato Instagram)")
    return output_path

if __name__ == "__main__":
    create_instagram_post()
