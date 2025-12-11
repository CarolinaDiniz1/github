#!/usr/bin/env python3
"""
Script para criar carrossel corporativo elegante para Instagram - VERSÃO 3 (FINAL)
Post: Kits Onboarding e Volta ao Trabalho 2026
Correções finais: Formatação, ícones, logo no rodapé
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
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
        font_highlight = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
        font_logo_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_logo_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_highlight = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
        font_logo_big = ImageFont.load_default()
        font_logo_small = ImageFont.load_default()

    return font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo_big, font_logo_small

def draw_header(draw):
    """Desenha o header padrão"""
    draw.rectangle([(0, 0), (WIDTH, 380)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 370), (WIDTH, 380)], fill=COLOR_ACCENT)

def draw_footer_with_logo(draw, y_start=1000):
    """Desenha logo branca no rodapé"""
    _, _, _, _, _, _, font_logo_big, font_logo_small = load_fonts()

    # Texto "BRINDES" em branco
    text_brindes = "BRINDES"
    bbox = draw.textbbox((0, 0), text_brindes, font=font_logo_big)
    text_width_brindes = bbox[2] - bbox[0]

    # Texto "MARCELO E WAGNER" em branco
    text_mw = "MARCELO E WAGNER"
    bbox2 = draw.textbbox((0, 0), text_mw, font=font_logo_small)
    text_width_mw = bbox2[2] - bbox2[0]

    # Usar a maior largura para centralizar
    max_width = max(text_width_brindes, text_width_mw)
    x_center = (WIDTH - max_width) // 2

    # Desenhar textos
    draw.text((x_center + (max_width - text_width_brindes)//2, y_start),
              text_brindes, fill=COLOR_TEXT_LIGHT, font=font_logo_big)
    draw.text((x_center + (max_width - text_width_mw)//2, y_start + 28),
              text_mw, fill=COLOR_TEXT_LIGHT, font=font_logo_small)

def center_text(draw, text, font):
    """Centraliza texto horizontalmente"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    return x

def create_slide_1():
    """SLIDE 1: Capa principal - CORRIGIDO"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo_big, font_logo_small = load_fonts()

    # Header
    draw_header(draw)

    # Título principal
    text = "JANEIRO 2026"
    x = center_text(draw, text, font_title)
    draw.text((x, 60), text, fill=COLOR_ACCENT, font=font_title)

    # Subtítulo
    text = "O MÊS DO RECOMEÇO"
    x = center_text(draw, text, font_subtitle)
    draw.text((x, 160), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    # Linha decorativa
    draw.rectangle([(WIDTH//2 - 150, 250), (WIDTH//2 + 150, 255)], fill=COLOR_ACCENT)

    # Texto principal
    text = "KITS CORPORATIVOS"
    x = center_text(draw, text, font_subtitle)
    draw.text((x, 285), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    # Área central
    y_pos = 420

    # Grande destaque
    text = "TRANSFORME A"
    x = center_text(draw, text, font_subtitle)
    draw.text((x, y_pos), text, fill=COLOR_PRIMARY, font=font_subtitle)

    text = "PRIMEIRA IMPRESSÃO"
    x = center_text(draw, text, font_subtitle)
    draw.text((x, y_pos + 60), text, fill=COLOR_PRIMARY, font=font_subtitle)

    # Box destaque - CORRIGIDO: formatação em 2 linhas
    draw.rectangle([(80, y_pos + 150), (WIDTH - 80, y_pos + 310)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=4)

    # CORREÇÃO: Texto em 2 linhas conforme solicitado
    text = "Brindes de Alto Impacto"
    x = center_text(draw, text, font_highlight)
    draw.text((x, y_pos + 170), text, fill=COLOR_ACCENT, font=font_highlight)

    text = "para Onboarding e"
    x = center_text(draw, text, font_body)
    draw.text((x, y_pos + 220), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    text = "Volta ao Trabalho"
    x = center_text(draw, text, font_body)
    draw.text((x, y_pos + 260), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    # Footer
    draw.rectangle([(0, 820), (WIDTH, HEIGHT)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 820), (WIDTH, 830)], fill=COLOR_ACCENT)

    # Setas
    text = "→ → →"
    x = center_text(draw, text, font_highlight)
    draw.text((x, 880), text, fill=COLOR_ACCENT, font=font_highlight)

    # Logo branca no rodapé
    draw_footer_with_logo(draw, 980)

    return img

def create_slide_2():
    """SLIDE 2: Kit Onboarding"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo_big, font_logo_small = load_fonts()

    # Header
    draw_header(draw)

    text = "KIT ONBOARDING"
    x = center_text(draw, text, font_title)
    draw.text((x, 100), text, fill=COLOR_ACCENT, font=font_title)

    text = "Receba com Excelência"
    x = center_text(draw, text, font_body)
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
        draw.rectangle([(padding, y_pos + (i * 85)), (WIDTH - padding, y_pos + (i * 85) + 70)],
                       fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=2)
        draw.text((padding + 30, y_pos + (i * 85) + 20), item,
                 fill=COLOR_TEXT_LIGHT, font=font_body)

    # Footer
    draw.rectangle([(0, 840), (WIDTH, HEIGHT)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 840), (WIDTH, 850)], fill=COLOR_ACCENT)

    text = "100% PERSONALIZÁVEL"
    x = center_text(draw, text, font_highlight)
    draw.text((x, 890), text, fill=COLOR_ACCENT, font=font_highlight)

    # Setas
    text = "→ → →"
    x = center_text(draw, text, font_small)
    draw.text((x, 950), text, fill=COLOR_ACCENT, font=font_small)

    # Logo branca no rodapé
    draw_footer_with_logo(draw, 1000)

    return img

def create_slide_3():
    """SLIDE 3: Kit Volta ao Trabalho"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo_big, font_logo_small = load_fonts()

    # Header
    draw_header(draw)

    text = "KIT VOLTA AO"
    x = center_text(draw, text, font_title)
    draw.text((x, 80), text, fill=COLOR_ACCENT, font=font_title)

    text = "TRABALHO"
    x = center_text(draw, text, font_title)
    draw.text((x, 160), text, fill=COLOR_ACCENT, font=font_title)

    text = "Reengaje seu Time"
    x = center_text(draw, text, font_body)
    draw.text((x, 270), text, fill=COLOR_TEXT_LIGHT, font=font_body)

    draw.rectangle([(WIDTH//2 - 180, 330), (WIDTH//2 + 180, 335)], fill=COLOR_ACCENT)

    # Conteúdo central
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
        draw.text((padding + 30, y_pos + (i * 85) + 20), item,
                 fill=COLOR_TEXT_LIGHT, font=font_body)

    # Footer
    draw.rectangle([(0, 840), (WIDTH, HEIGHT)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 840), (WIDTH, 850)], fill=COLOR_ACCENT)

    text = "FORTALEÇA O ENGAJAMENTO"
    x = center_text(draw, text, font_highlight)
    draw.text((x, 890), text, fill=COLOR_ACCENT, font=font_highlight)

    # Setas
    text = "→ → →"
    x = center_text(draw, text, font_small)
    draw.text((x, 950), text, fill=COLOR_ACCENT, font=font_small)

    # Logo branca no rodapé
    draw_footer_with_logo(draw, 1000)

    return img

def create_slide_4():
    """SLIDE 4: Credenciais e CTA - CORRIGIDO"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    font_title, font_subtitle, font_body, font_highlight, font_small, font_tiny, font_logo_big, font_logo_small = load_fonts()

    # Header
    draw_header(draw)

    text = "POR QUE ESCOLHER"
    x = center_text(draw, text, font_subtitle)
    draw.text((x, 60), text, fill=COLOR_TEXT_LIGHT, font=font_subtitle)

    text = "BRINDES"
    x = center_text(draw, text, font_subtitle)
    draw.text((x, 125), text, fill=COLOR_ACCENT, font=font_subtitle)

    text = "MARCELO E WAGNER?"
    x = center_text(draw, text, font_subtitle)
    draw.text((x, 185), text, fill=COLOR_ACCENT, font=font_subtitle)

    draw.rectangle([(WIDTH//2 - 250, 260), (WIDTH//2 + 250, 265)], fill=COLOR_ACCENT)

    # CORREÇÃO: Box bem formatado para "Especialistas em Grandes Agências"
    draw.rectangle([(80, 290), (WIDTH - 80, 380)],
                   fill=COLOR_ACCENT, outline=COLOR_ACCENT, width=3)

    text = "Especialistas em"
    x = center_text(draw, text, font_highlight)
    draw.text((x, 310), text, fill=COLOR_PRIMARY, font=font_highlight)

    text = "Grandes Agências"
    x = center_text(draw, text, font_highlight)
    draw.text((x, 350), text, fill=COLOR_PRIMARY, font=font_highlight)

    # Credenciais
    y_pos = 410

    # Box 1
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 75)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "+10.000 CLIENTES"
    x = center_text(draw, text, font_highlight)
    draw.text((x, y_pos + 22), text, fill=COLOR_ACCENT, font=font_highlight)

    # Box 2
    y_pos += 95
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 75)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "+20 ANOS DE MERCADO"
    x = center_text(draw, text, font_highlight)
    draw.text((x, y_pos + 22), text, fill=COLOR_ACCENT, font=font_highlight)

    # Box 3
    y_pos += 95
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 75)],
                   fill=COLOR_SECONDARY, outline=COLOR_ACCENT, width=3)
    text = "ENTREGAS TODO BRASIL"
    x = center_text(draw, text, font_highlight)
    draw.text((x, y_pos + 22), text, fill=COLOR_ACCENT, font=font_highlight)

    # Footer com CTA
    draw.rectangle([(0, 740), (WIDTH, HEIGHT)], fill=COLOR_PRIMARY)
    draw.rectangle([(0, 740), (WIDTH, 750)], fill=COLOR_ACCENT)

    text = "COMECE 2026 COM O PÉ DIREITO!"
    x = center_text(draw, text, font_body)
    draw.text((x, 765), text, fill=COLOR_ACCENT, font=font_body)

    draw.rectangle([(150, 820), (WIDTH - 150, 825)], fill=COLOR_ACCENT)

    # CORREÇÃO: Adicionar ÍCONES reais (usando caracteres Unicode)
    # WhatsApp
    text = "📱 (31) 3446-0908"
    x = center_text(draw, text, font_highlight)
    draw.text((x, 845), text, fill=COLOR_TEXT_LIGHT, font=font_highlight)

    # Instagram e Site com ícones
    y_contact = 910

    # Instagram (ícone)
    text_ig = "📷 @brindesmarceloewagner"
    draw.text((80, y_contact), text_ig, fill=COLOR_TEXT_LIGHT, font=font_small)

    # Site (ícone)
    text_site = "🌐 brindesmarceloewagner.com.br"
    bbox = draw.textbbox((0, 0), text_site, font=font_tiny)
    text_width = bbox[2] - bbox[0]
    draw.text((WIDTH - text_width - 80, y_contact + 5), text_site, fill=COLOR_TEXT_LIGHT, font=font_tiny)

    # Localização
    text_loc = "📍 Belo Horizonte/MG"
    x = center_text(draw, text_loc, font_small)
    draw.text((x, 960), text_loc, fill=COLOR_TEXT_LIGHT, font=font_small)

    # Logo branca no rodapé
    draw_footer_with_logo(draw, 1010)

    return img

def create_carousel():
    """Cria todas as artes do carrossel - VERSÃO 3 (FINAL)"""

    slides = [
        ("slide_1_capa_v3.png", create_slide_1()),
        ("slide_2_kit_onboarding_v3.png", create_slide_2()),
        ("slide_3_kit_volta_trabalho_v3.png", create_slide_3()),
        ("slide_4_credenciais_v3.png", create_slide_4()),
    ]

    output_paths = []

    for filename, img in slides:
        output_path = f"/home/user/github/assets/posts/{filename}"
        img.save(output_path, quality=95)
        output_paths.append(output_path)
        print(f"✅ Criado: {filename}")

    print(f"\n🎉 Carrossel VERSÃO FINAL (V3) criado com sucesso!")
    print(f"📐 Dimensões: {WIDTH}x{HEIGHT}px cada slide")
    print(f"📊 Total de slides: {len(slides)}")
    print(f"\n✅ CORREÇÕES APLICADAS:")
    print(f"   ✓ Slide 1: Texto reformatado em 2 linhas corretas")
    print(f"   ✓ Slide 4: Box 'Especialistas' bem formatado")
    print(f"   ✓ Slide 4: Ícones incluídos (WhatsApp, Instagram, Site)")
    print(f"   ✓ Todos: Logo branca no rodapé")
    print(f"\n📁 Arquivos salvos em: /home/user/github/assets/posts/")

    return output_paths

if __name__ == "__main__":
    create_carousel()
