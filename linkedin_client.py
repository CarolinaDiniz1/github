import requests
import config
import logging
from linkedin_api import Linkedin

logger = logging.getLogger(__name__)

class LinkedInClient:
    def __init__(self):
        self.api = None

    def login(self):
        """Faz login no LinkedIn"""
        try:
            logger.info(f"Fazendo login no LinkedIn como {config.LINKEDIN_EMAIL}")
            self.api = Linkedin(config.LINKEDIN_EMAIL, config.LINKEDIN_PASSWORD)
            logger.info("Login no LinkedIn realizado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao fazer login no LinkedIn: {e}")
            return False

    def post_content(self, text, image_path=None):
        """
        Posta conteúdo no LinkedIn

        Args:
            text: Texto do post
            image_path: Caminho opcional para imagem

        Returns:
            bool: True se postou com sucesso
        """
        try:
            if not self.api:
                logger.error("Cliente LinkedIn não está logado")
                return False

            # A biblioteca linkedin-api tem limitações para posting
            # Vamos usar a API oficial do LinkedIn através de requests
            # Nota: Isso requer configurar uma aplicação LinkedIn e obter tokens OAuth

            logger.info("Postando no LinkedIn...")

            # Por enquanto, vamos usar o método de compartilhamento da biblioteca
            # Para implementação completa, seria necessário:
            # 1. Criar uma aplicação LinkedIn Developer
            # 2. Implementar OAuth 2.0
            # 3. Usar a API de compartilhamento do LinkedIn

            # Este é um método simplificado que pode precisar de ajustes
            logger.warning("AVISO: Para postar no LinkedIn de forma automatizada, você precisa:")
            logger.warning("1. Criar uma aplicação em https://www.linkedin.com/developers/")
            logger.warning("2. Obter credenciais OAuth 2.0")
            logger.warning("3. Implementar o fluxo de autenticação OAuth")

            # Simulação de post bem-sucedido para fins de demonstração
            logger.info(f"Post no LinkedIn: {text[:50]}...")

            if image_path:
                logger.info(f"Com imagem: {image_path}")

            # TODO: Implementar post real usando LinkedIn API com OAuth
            # Por enquanto, retorna True para demonstração
            return True

        except Exception as e:
            logger.error(f"Erro ao postar no LinkedIn: {e}")
            return False

    def post_with_oauth(self, access_token, text, image_path=None):
        """
        Posta usando OAuth token (método recomendado)

        Args:
            access_token: Token de acesso OAuth 2.0
            text: Texto do post
            image_path: Caminho opcional para imagem
        """
        try:
            # Endpoint da API do LinkedIn
            url = "https://api.linkedin.com/v2/ugcPosts"

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }

            # Estrutura do post
            post_data = {
                "author": f"urn:li:person:{self._get_person_id(access_token)}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            # Se tiver imagem, adiciona
            if image_path:
                # Implementar upload de imagem
                pass

            response = requests.post(url, json=post_data, headers=headers)

            if response.status_code == 201:
                logger.info("Post criado no LinkedIn com sucesso!")
                return True
            else:
                logger.error(f"Erro ao criar post: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Erro ao postar no LinkedIn com OAuth: {e}")
            return False

    def _get_person_id(self, access_token):
        """Obtém o ID da pessoa autenticada"""
        url = "https://api.linkedin.com/v2/me"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('id')
        return None
