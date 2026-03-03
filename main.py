#!/usr/bin/env python3
"""
Instagram Auto-Poster para LinkedIn e Threads

Este script monitora os posts do Instagram e automaticamente
replica o conteúdo no LinkedIn e Threads.
"""

import json
import logging
import os
import time
import schedule
from datetime import datetime
from pathlib import Path

import config
from instagram_client import InstagramClient
from linkedin_client import LinkedInClient
from threads_client import ThreadsClient

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_autoposter.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class InstagramAutoPoster:
    def __init__(self):
        self.instagram = InstagramClient()
        self.linkedin = LinkedInClient()
        self.threads = ThreadsClient()
        self.last_post_file = config.LAST_POST_FILE

        # Cria diretório temp se não existir
        Path('temp').mkdir(exist_ok=True)

    def load_last_post_id(self):
        """Carrega o ID do último post processado"""
        try:
            if os.path.exists(self.last_post_file):
                with open(self.last_post_file, 'r') as f:
                    data = json.load(f)
                    return data.get('last_post_id')
        except Exception as e:
            logger.error(f"Erro ao carregar último post ID: {e}")
        return None

    def save_last_post_id(self, post_id):
        """Salva o ID do último post processado"""
        try:
            data = {
                'last_post_id': post_id,
                'timestamp': datetime.now().isoformat()
            }
            with open(self.last_post_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Último post ID salvo: {post_id}")
        except Exception as e:
            logger.error(f"Erro ao salvar último post ID: {e}")

    def check_configuration(self):
        """Verifica e exibe status da configuração"""
        logger.info("=" * 60)
        logger.info("VERIFICAÇÃO DE CONFIGURAÇÃO")
        logger.info("=" * 60)

        # Verifica LinkedIn
        if os.path.exists('oauth_config.json'):
            with open('oauth_config.json', 'r') as f:
                oauth_config = json.load(f)
                if 'linkedin' in oauth_config and oauth_config['linkedin'].get('access_token'):
                    logger.info("✓ LinkedIn OAuth configurado")
                else:
                    logger.warning("⚠ LinkedIn OAuth NÃO configurado")
                    logger.warning("  Posts no LinkedIn NÃO funcionarão!")
                    logger.warning("  Execute: python setup_oauth.py")
        else:
            logger.error("✗ LinkedIn NÃO configurado")
            logger.error("  Execute: python setup_oauth.py")

        # Verifica Threads
        logger.warning("⚠ Threads: API limitada pela Meta")
        logger.warning("  Posts no Threads podem NÃO funcionar")
        logger.warning("  Recomendação: Use ferramentas de terceiros")

        logger.info("=" * 60)

    def login_all(self):
        """Faz login em todas as plataformas"""
        logger.info("=== Iniciando logins ===")

        instagram_ok = self.instagram.login()
        linkedin_ok = self.linkedin.login()
        threads_ok = self.threads.login()

        if not instagram_ok:
            logger.error("✗ Falha no login do Instagram - processo abortado")
            logger.error("Verifique as credenciais no arquivo .env")
            return False

        if not linkedin_ok:
            logger.error("✗ Falha no login do LinkedIn")
            logger.error("Posts NÃO serão enviados para o LinkedIn")
            logger.error("Execute: python setup_oauth.py")

        if not threads_ok:
            logger.warning("⚠ Falha no login do Threads")
            logger.warning("Posts NÃO serão enviados para o Threads")

        logger.info("=== Logins concluídos ===")
        return True

    def format_caption(self, caption, platform):
        """
        Formata a legenda para cada plataforma

        Args:
            caption: Legenda original do Instagram
            platform: 'linkedin' ou 'threads'

        Returns:
            str: Legenda formatada
        """
        if not caption:
            caption = ""

        # Remove hashtags excessivas para o LinkedIn (mais profissional)
        if platform == 'linkedin':
            # Mantém apenas as primeiras 3 hashtags
            words = caption.split()
            hashtags = [w for w in words if w.startswith('#')]
            if len(hashtags) > 3:
                for hashtag in hashtags[3:]:
                    caption = caption.replace(hashtag, '')

            # Adiciona nota de origem
            caption += "\n\n📸 Compartilhado do Instagram"

        elif platform == 'threads':
            # Threads permite estilo mais casual
            caption += "\n\n🔄 Auto-postado do Instagram"

        return caption.strip()

    def check_and_post(self):
        """Verifica novos posts do Instagram e replica nas outras plataformas"""
        logger.info("=== Verificando novos posts ===")

        try:
            # Obtém o último post do Instagram
            latest_post = self.instagram.get_latest_post()

            if not latest_post:
                logger.info("Nenhum post encontrado")
                return

            post_id = latest_post['id']
            last_post_id = self.load_last_post_id()

            # Verifica se já processou este post
            if post_id == last_post_id:
                logger.info(f"Post {post_id} já foi processado anteriormente")
                return

            logger.info(f"Novo post detectado: {post_id}")

            # Prepara o conteúdo
            caption = latest_post.get('caption', '')
            media_path = latest_post.get('media_path')

            logger.info(f"Caption: {caption[:100]}...")
            logger.info(f"Mídia: {media_path}")

            # Posta no LinkedIn
            linkedin_caption = self.format_caption(caption, 'linkedin')
            linkedin_success = self.linkedin.post_content(linkedin_caption, media_path)

            if linkedin_success:
                logger.info("✓ Post enviado para o LinkedIn com sucesso!")
            else:
                logger.error("✗ Falha ao postar no LinkedIn")

            # Posta no Threads
            threads_caption = self.format_caption(caption, 'threads')

            if media_path:
                threads_success = self.threads.post_with_image(threads_caption, media_path)
            else:
                threads_success = self.threads.post_text(threads_caption)

            if threads_success:
                logger.info("✓ Post enviado para o Threads com sucesso!")
            else:
                logger.error("✗ Falha ao postar no Threads")

            # Salva o ID do último post processado
            self.save_last_post_id(post_id)

            logger.info("=== Verificação concluída ===")

        except Exception as e:
            logger.error(f"Erro ao verificar e postar: {e}", exc_info=True)

    def run_once(self):
        """Executa uma verificação única"""
        logger.info("=== MODO: Execução única ===")

        # Verifica configuração primeiro
        self.check_configuration()

        if not self.login_all():
            logger.error("Falha nos logins, encerrando")
            logger.error("\nPara resolver:")
            logger.error("1. Verifique o arquivo .env com suas credenciais")
            logger.error("2. Configure OAuth: python setup_oauth.py")
            logger.error("3. Teste as conexões: python test_connections.py")
            return

        self.check_and_post()
        logger.info("Execução concluída")

    def run_scheduled(self):
        """Executa em modo agendado (verifica periodicamente)"""
        logger.info("=== MODO: Execução agendada ===")
        logger.info(f"Intervalo de verificação: {config.CHECK_INTERVAL_MINUTES} minutos")

        # Verifica configuração primeiro
        self.check_configuration()

        if not self.login_all():
            logger.error("Falha nos logins, encerrando")
            logger.error("\nPara resolver:")
            logger.error("1. Verifique o arquivo .env com suas credenciais")
            logger.error("2. Configure OAuth: python setup_oauth.py")
            logger.error("3. Teste as conexões: python test_connections.py")
            return

        # Agenda a verificação
        schedule.every(config.CHECK_INTERVAL_MINUTES).minutes.do(self.check_and_post)

        # Faz a primeira verificação imediatamente
        self.check_and_post()

        # Loop principal
        logger.info("Bot iniciado! Pressione Ctrl+C para parar.")

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Bot encerrado pelo usuário")


def main():
    """Função principal"""
    import sys

    poster = InstagramAutoPoster()

    # Verifica argumentos da linha de comando
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        poster.run_once()
    else:
        poster.run_scheduled()


if __name__ == "__main__":
    main()
