"""
Cliente alternativo para Threads usando a API oficial da Meta

A Meta lançou a API do Threads em 2024. Este cliente usa a API oficial.
"""

import requests
import logging
import os
import json
import config

logger = logging.getLogger(__name__)


class ThreadsGraphAPIClient:
    """Cliente para postar no Threads usando a Graph API oficial"""

    def __init__(self):
        self.access_token = None
        self.user_id = None
        self._load_config()

    def _load_config(self):
        """Carrega configuração da Graph API"""
        try:
            if os.path.exists('oauth_config.json'):
                with open('oauth_config.json', 'r') as f:
                    oauth_config = json.load(f)

                if 'threads' in oauth_config:
                    self.access_token = oauth_config['threads'].get('access_token')
                    self.user_id = oauth_config['threads'].get('user_id')
        except Exception as e:
            logger.warning(f"Não foi possível carregar config do Threads: {e}")

    def login(self):
        """Valida se tem acesso configurado"""
        if self.access_token and self.user_id:
            logger.info("Configuração da Threads Graph API encontrada")
            return True
        else:
            logger.warning("Threads Graph API não configurada")
            logger.warning("Para configurar:")
            logger.warning("1. Crie uma app em https://developers.facebook.com/")
            logger.warning("2. Ative Threads API")
            logger.warning("3. Obtenha o access token")
            logger.warning("4. Execute: python setup_oauth.py")
            return False

    def create_post(self, text, image_url=None):
        """
        Cria um post no Threads

        Args:
            text: Texto do post
            image_url: URL pública da imagem (opcional)

        Returns:
            bool: True se postou com sucesso
        """
        try:
            if not self.access_token or not self.user_id:
                logger.error("Threads API não configurada")
                return False

            # Endpoint da Threads API
            url = f"https://graph.threads.net/v1.0/{self.user_id}/threads"

            params = {
                'media_type': 'TEXT' if not image_url else 'IMAGE',
                'text': text,
                'access_token': self.access_token
            }

            if image_url:
                params['image_url'] = image_url

            # Cria o container de mídia
            logger.info("Criando container de mídia no Threads...")
            response = requests.post(url, params=params)

            if response.status_code == 200:
                creation_id = response.json().get('id')
                logger.info(f"Container criado: {creation_id}")

                # Publica o post
                publish_url = f"https://graph.threads.net/v1.0/{self.user_id}/threads_publish"
                publish_params = {
                    'creation_id': creation_id,
                    'access_token': self.access_token
                }

                logger.info("Publicando post no Threads...")
                publish_response = requests.post(publish_url, params=publish_params)

                if publish_response.status_code == 200:
                    post_id = publish_response.json().get('id')
                    logger.info(f"✓ Post publicado no Threads com sucesso! ID: {post_id}")
                    return True
                else:
                    logger.error(f"Erro ao publicar: {publish_response.status_code}")
                    logger.error(f"Resposta: {publish_response.text}")
                    return False
            else:
                logger.error(f"Erro ao criar container: {response.status_code}")
                logger.error(f"Resposta: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Erro ao postar no Threads: {e}")
            return False
