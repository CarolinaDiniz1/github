#!/usr/bin/env python3
"""
Script para criar carrossel corporativo elegante para Instagram - VERSÃO ATUALIZADA
Post: Kits Onboarding e Volta ao Trabalho 2026
Alterações: Formatação melhorada, remoção de contadores, inclusão de logo
"""

from PIL import Image, ImageDraw, ImageFont
import os

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
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        font_highlight = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_logo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_highlight = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
        font_logo = ImageFont.load_default()

    return font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo

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

def draw_logo_text(draw, font_logo, x=20, y=20):
    """Desenha logo textual da empresa"""
    # Box da logo
    draw.rectangle([(x, y), (x + 300, y + 70)], fill=COLOR_ACCENT)

    # Texto "BRINDES"
    draw.text((x + 15, y + 8), "BRINDES", fill=COLOR_PRIMARY, font=font_logo)

    # Texto "MARCELO E WAGNER"
    font_small_logo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    draw.text((x + 15, y + 40), "MARCELO E WAGNER", fill=COLOR_PRIMARY, font=font_small_logo)

def create_slide_1():
    """SLIDE 1: Capa principal - ATUALIZADA"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo = load_fonts()

    # Header
    draw_header(draw, "")

    # Título principal
    text = "JANEIRO 2026"
    x = center_text(draw, text, font_title, 0)
    draw.text((x, 60), text, fill=COLOR_ACCENT, font=font_title)

    # Subtítulo
    text = "O MÊS DO RECOMEÇO"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, 160), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    # Linha decorativa
    draw.rectangle([(WIDTH//2 - 150, 250), (WIDTH//2 + 150, 255)], fill=COLOR_ACCENT)

    # Texto principal
    text = "KITS CORPORATIVOS"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, 285), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    # Área central
    y_pos = 420

    # Grande destaque
    text = "TRANSFORME A"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, y_pos), text, fill=COLOR_PRIMARY, font=font_subtitle)

    text = "PRIMEIRA IMPRESSÃO"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, y_pos + 60), text, fill=COLOR_PRIMARY, font=font_subtitle)

    # Box destaque - REFORMATADO
    draw.rectangle([(80, y_pos + 150), (WIDTH - 80, y_pos + 330)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=4)

    # Texto dentro do box - MELHOR FORMATADO
    text = "Brindes de"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, y_pos + 165), text, fill=COLOR_ACCENT, font=font_highlight)

    text = "Alto Impacto"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, y_pos + 210), text, fill=COLOR_ACCENT, font=font_highlight)

    text = "para Onboarding e"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, y_pos + 260), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    text = "Volta ao Trabalho"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, y_pos + 295), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    # Footer - SEM contador, apenas seta
    draw_footer(draw)

    # Setas indicativas
    draw.text((WIDTH//2 - 40, 900), "→ → →", fill=COLOR_ACCENT, font=font_highlight)

    # Logo textual
    draw_logo_text(draw, font_logo, x=750, y=950)

    return img

def create_slide_2():
    """SLIDE 2: Kit Onboarding - ATUALIZADO"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo = load_fonts()

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

    # Footer - SEM contador
    draw_footer(draw, 840)

    text = "100% PERSONALIZÁVEL"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, 890), text, fill=COLOR_ACCENT, font=font_highlight)

    # Seta
    draw.text((WIDTH//2 - 40, 950), "→ → →", fill=COLOR_ACCENT, font=font_small)

    # Logo textual
    draw_logo_text(draw, font_logo, x=750, y=950)

    return img

def create_slide_3():
    """SLIDE 3: Kit Volta ao Trabalho - ATUALIZADO"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo = load_fonts()

    # Header
    draw_header(draw, "")

    text = "KIT VOLTA AO"
    x = center_text(draw, text, font_title, 0)
    draw.text((x, 80), text, fill=COLOR_ACCENT, font=font_title)

    text = "TRABALHO"
    x = center_text(draw, text, font_title, 0)
    draw.text((x, 160), text, fill=COLOR_ACCENT, font=font_title)

    # CORREÇÃO: "Reengaje" sem hífen
    text = "Reengaje seu Time"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, 270), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    draw.rectangle([(WIDTH//2 - 180, 330), (WIDTH//2 + 180, 335)], fill=COLOR_ACCENT)

    # Conteúdo central
    y_pos = 420
    padding = 90

    # ATUALIZAÇÕES: Planner → Moleskine, Mimo Especial → Caneta
    items = [
        "✓ Moleskine",
        "✓ Squeeze Personalizado",
        "✓ Mousepad Premium",
        "✓ Bloco de Notas",
        "✓ Caneta",
    ]

    for i, item in enumerate(items):
        # Box para cada item
        draw.rectangle([(padding, y_pos + (i * 85)), (WIDTH - padding, y_pos + (i * 85) + 70)],
                       fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=2)

        draw.text((padding + 30, y_pos + (i * 85) + 20), item,
                 fill=COLOR_TEXT_LIGHT, font=font_body)

    # Footer - SEM contador
    draw_footer(draw, 840)

    text = "FORTALEÇA O ENGAJAMENTO"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, 890), text, fill=COLOR_ACCENT, font=font_highlight)

    # Seta
    draw.text((WIDTH//2 - 40, 950), "→ → →", fill=COLOR_ACCENT, font=font_small)

    # Logo textual
    draw_logo_text(draw, font_logo, x=750, y=950)

    return img

def create_slide_4():
    """SLIDE 4: Credenciais e CTA - ATUALIZADO"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo = load_fonts()

    # Header
    draw_header(draw, "")

    text = "POR QUE ESCOLHER"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, 70), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    # CORREÇÃO: Nome completo da empresa
    text = "BRINDES"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, 135), text, fill=COLOR_ACCENT, font=font_subtitle)

    text = "MARCELO E WAGNER?"
    x = center_text(draw, text, font_subtitle, 0)
    draw.text((x, 195), text, fill=COLOR_ACCENT, font=font_subtitle)

    draw.rectangle([(WIDTH//2 - 250, 270), (WIDTH//2 + 250, 275)], fill=COLOR_ACCENT)

    # DESTAQUE: Especialistas em Grandes Agências
    draw.rectangle([(100, 300), (WIDTH - 100, 380)],
                   fill=COLOR_ACCENT, outline=COLOR_ACCENT, width=3)

    text = "Especialistas em"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, 312), text, fill=COLOR_PRIMARY, font=font_highlight)

    text = "Grandes Agências"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, 350), text, fill=COLOR_PRIMARY, font=font_highlight)

    # Área central com credenciais
    y_pos = 420

    # Box 1
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 80)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)

    text = "+10.000 CLIENTES"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, y_pos + 25), text, fill=COLOR_ACCENT, font=font_highlight)

    # Box 2
    y_pos += 100
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 80)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)

    text = "+20 ANOS DE MERCADO"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, y_pos + 25), text, fill=COLOR_ACCENT, font=font_highlight)

    # Box 3
    y_pos += 100
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 80)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)

    text = "ENTREGAS TODO BRASIL"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, y_pos + 25), text, fill=COLOR_ACCENT, font=font_highlight)

    # Footer com CTA
    draw_footer(draw, 760)

    text = "COMECE 2026 COM O PÉ DIREITO!"
    x = center_text(draw, text, font_body, 0)
    draw.text((x, 790), text, fill=COLOR_ACCENT, font=font_body)

    # Linha divisória
    draw.rectangle([(150, 850), (WIDTH - 150, 855)], fill=COLOR_ACCENT)

    # Contato COM ÍCONES
    # WhatsApp
    text = "📱 (31) 3446-0908"
    x = center_text(draw, text, font_highlight, 0)
    draw.text((x, 880), text, fill=COLOR_TEXT_LIGHT, font=font_highlight)

    # Localização
    text = "📍 Belo Horizonte/MG"
    bbox = draw.textbbox((0, 0), text, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text((100, 950), text, fill=COLOR_TEXT_LIGHT, font=font_small)

    # Site
    text = "🌐 brindesmarceloewagner.com.br"
    bbox = draw.textbbox((0, 0), text, font=font_tiny)
    text_width = bbox[2] - bbox[0]
    x = WIDTH - text_width - 100
    draw.text((x, 955), text, fill=COLOR_TEXT_LIGHT, font=font_tiny)

    # Logo textual no topo
    draw_logo_text(draw, font_logo, x=750, y=1000)

    return img

def create_carousel():
    """Cria todas as artes do carrossel - VERSÃO ATUALIZADA"""

    slides = [
        ("slide_1_capa_v2.png", create_slide_1()),
        ("slide_2_kit_onboarding_v2.png", create_slide_2()),
        ("slide_3_kit_volta_trabalho_v2.png", create_slide_3()),
        ("slide_4_credenciais_v2.png", create_slide_4()),
    ]

    output_paths = []

    for filename, img in slides:
        output_path = f"/home/user/github/assets/posts/{filename}"
        img.save(output_path, quality=95)
        output_paths.append(output_path)
        print(f"✅ Criado: {filename}")

    print(f"\n🎉 Carrossel ATUALIZADO criado com sucesso!")
    print(f"📐 Dimensões: {WIDTH}x{HEIGHT}px cada slide")
    print(f"📊 Total de slides: {len(slides)}")
    print(f"\n📁 Arquivos salvos em: /home/user/github/assets/posts/")
    print(f"\n✅ ALTERAÇÕES APLICADAS:")
    print(f"   - Slide 1: Texto reformatado no box azul")
    print(f"   - Todos: Removidos contadores (1/4, 2/4, etc)")
    print(f"   - Todos: Mantidas apenas setas")
    print(f"   - Todos: Logo textual incluída")
    print(f"   - Slide 3: 'Reengaje' sem hífen")
    print(f"   - Slide 3: Planner → Moleskine")
    print(f"   - Slide 3: Mimo Especial → Caneta")
    print(f"   - Slide 4: Nome completo 'BRINDES MARCELO E WAGNER'")
    print(f"   - Slide 4: Ícones WhatsApp, Site e Localização")
    print(f"   - Slide 4: Destaque para 'Especialistas em Grandes Agências'")

    return output_paths

if __name__ == "__main__":
    create_carousel()
