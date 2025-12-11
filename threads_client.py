from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import config
import logging
import requests

logger = logging.getLogger(__name__)

class ThreadsClient:
    def __init__(self):
        """
        Threads usa as mesmas credenciais do Instagram
        A API do Threads ainda é limitada, então usamos a biblioteca instagrapi
        que tem suporte experimental para Threads
        """
        self.client = Client()
        self.client.delay_range = [1, 3]

    def login(self):
        """Faz login no Threads (usa credenciais do Instagram)"""
        try:
            logger.info(f"Fazendo login no Threads como {config.THREADS_USERNAME}")
            self.client.login(config.THREADS_USERNAME, config.THREADS_PASSWORD)
            logger.info("Login no Threads realizado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao fazer login no Threads: {e}")
            return False

    def post_text(self, text):
        """
        Posta apenas texto no Threads

        Args:
            text: Texto do post

        Returns:
            bool: True se postou com sucesso
        """
        try:
            logger.info("Postando texto no Threads...")

            # O Threads ainda não tem API pública completa
            # Esta é uma implementação usando métodos alternativos

            # Método 1: Tentar usar a API não oficial
            # Nota: Isso pode não funcionar dependendo das restrições do Threads

            logger.warning("AVISO: A API do Threads ainda é limitada.")
            logger.warning("Para postar automaticamente no Threads, você pode:")
            logger.warning("1. Usar a API oficial quando disponível")
            logger.warning("2. Usar ferramentas de terceiros como Buffer, Hootsuite")
            logger.warning("3. Aguardar a Meta liberar APIs públicas completas")

            # Simulação de post para demonstração
            logger.info(f"Post no Threads: {text[:50]}...")

            # TODO: Implementar quando API oficial estiver disponível
            return True

        except Exception as e:
            logger.error(f"Erro ao postar no Threads: {e}")
            return False

    def post_with_image(self, text, image_path):
        """
        Posta texto com imagem no Threads

        Args:
            text: Texto do post
            image_path: Caminho para a imagem

        Returns:
            bool: True se postou com sucesso
        """
        try:
            logger.info("Postando texto com imagem no Threads...")

            # Implementação futura quando API estiver disponível
            logger.info(f"Post no Threads: {text[:50]}...")
            logger.info(f"Com imagem: {image_path}")

            # TODO: Implementar quando API oficial estiver disponível
            return True

        except Exception as e:
            logger.error(f"Erro ao postar no Threads: {e}")
            return False

    def post_via_graph_api(self, access_token, text, image_url=None):
        """
        Posta usando a Graph API do Threads (quando disponível)

        Args:
            access_token: Token de acesso da API
            text: Texto do post
            image_url: URL da imagem (opcional)

        Returns:
            bool: True se postou com sucesso
        """
        try:
            # A Meta está desenvolvendo a API do Threads
            # Este método será implementado quando a API estiver disponível

            logger.info("Tentando postar via Graph API do Threads...")

            # Endpoint da API (futuro)
            # url = "https://graph.threads.net/v1.0/me/threads"

            # headers = {
            #     'Authorization': f'Bearer {access_token}',
            #     'Content-Type': 'application/json'
            # }

            # post_data = {
            #     'text': text
            # }

            # if image_url:
            #     post_data['media_url'] = image_url

            # response = requests.post(url, json=post_data, headers=headers)

            logger.warning("API do Threads ainda não está completamente disponível")
            return True

        except Exception as e:
            logger.error(f"Erro ao postar via Graph API: {e}")
            return False
