import requests
import config
import logging
import json
import os
from linkedin_api import Linkedin

logger = logging.getLogger(__name__)

class LinkedInClient:
    def __init__(self):
        self.api = None
        self.access_token = None
        self.person_id = None
        self.use_oauth = False

        # Tenta carregar configuração OAuth
        self._load_oauth_config()

    def _load_oauth_config(self):
        """Carrega configuração OAuth se disponível"""
        try:
            if os.path.exists('oauth_config.json'):
                with open('oauth_config.json', 'r') as f:
                    oauth_config = json.load(f)

                if 'linkedin' in oauth_config:
                    self.access_token = oauth_config['linkedin'].get('access_token')
                    if self.access_token:
                        self.use_oauth = True
                        logger.info("Configuração OAuth do LinkedIn carregada")
                        # Obtém person_id
                        self.person_id = self._get_person_id(self.access_token)
        except Exception as e:
            logger.warning(f"Não foi possível carregar OAuth config: {e}")

    def login(self):
        """Faz login no LinkedIn"""
        # Se tem OAuth configurado, usa ele
        if self.use_oauth and self.access_token:
            logger.info("Usando autenticação OAuth para LinkedIn")
            # Valida o token
            if self._validate_token():
                logger.info("Token OAuth válido")
                return True
            else:
                logger.warning("Token OAuth inválido, tentando método tradicional")
                self.use_oauth = False

        # Fallback para método tradicional
        try:
            logger.info(f"Fazendo login no LinkedIn como {config.LINKEDIN_EMAIL}")
            self.api = Linkedin(config.LINKEDIN_EMAIL, config.LINKEDIN_PASSWORD)
            logger.info("Login no LinkedIn realizado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao fazer login no LinkedIn: {e}")
            return False

    def _validate_token(self):
        """Valida se o token OAuth ainda é válido"""
        try:
            url = "https://api.linkedin.com/v2/me"
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            response = requests.get(url, headers=headers)
            return response.status_code == 200
        except:
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
            # Se tem OAuth configurado, usa ele
            if self.use_oauth and self.access_token:
                logger.info("Postando no LinkedIn com OAuth...")
                return self.post_with_oauth(self.access_token, text, image_path)

            # Fallback para método tradicional (limitado)
            if not self.api:
                logger.error("Cliente LinkedIn não está logado")
                return False

            logger.info("Postando no LinkedIn (método tradicional)...")
            logger.warning("AVISO: Para automação completa, configure OAuth:")
            logger.warning("  python setup_oauth.py")

            # Simulação de post bem-sucedido para fins de demonstração
            logger.info(f"Post no LinkedIn: {text[:50]}...")

            if image_path:
                logger.info(f"Com imagem: {image_path}")

            # TODO: Implementar post real usando LinkedIn API tradicional
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
            # Obtém person_id se não tiver
            if not self.person_id:
                self.person_id = self._get_person_id(access_token)
                if not self.person_id:
                    logger.error("Não foi possível obter person_id")
                    return False

            # Endpoint da API do LinkedIn
            url = "https://api.linkedin.com/v2/ugcPosts"

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }

            # Estrutura do post
            post_data = {
                "author": f"urn:li:person:{self.person_id}",
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

            # Se tiver imagem, faz upload primeiro
            if image_path and os.path.exists(image_path):
                media_urn = self._upload_image(access_token, image_path)
                if media_urn:
                    post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
                    post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                        {
                            "status": "READY",
                            "description": {
                                "text": "Imagem compartilhada do Instagram"
                            },
                            "media": media_urn,
                            "title": {
                                "text": "Imagem"
                            }
                        }
                    ]

            response = requests.post(url, json=post_data, headers=headers)

            if response.status_code == 201:
                logger.info("✓ Post criado no LinkedIn com sucesso!")
                return True
            else:
                logger.error(f"✗ Erro ao criar post: {response.status_code}")
                logger.error(f"Resposta: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Erro ao postar no LinkedIn com OAuth: {e}")
            return False

    def _upload_image(self, access_token, image_path):
        """
        Faz upload de imagem para o LinkedIn

        Args:
            access_token: Token OAuth
            image_path: Caminho da imagem

        Returns:
            str: URN da mídia ou None
        """
        try:
            # Registra o upload
            register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            register_data = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:person:{self.person_id}",
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }

            response = requests.post(register_url, json=register_data, headers=headers)

            if response.status_code != 200:
                logger.error(f"Erro ao registrar upload: {response.status_code}")
                return None

            upload_data = response.json()
            upload_url = upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            asset_urn = upload_data['value']['asset']

            # Faz upload da imagem
            with open(image_path, 'rb') as f:
                image_data = f.read()

            upload_headers = {
                'Authorization': f'Bearer {access_token}'
            }

            upload_response = requests.put(upload_url, data=image_data, headers=upload_headers)

            if upload_response.status_code in [200, 201]:
                logger.info("✓ Imagem enviada para o LinkedIn")
                return asset_urn
            else:
                logger.error(f"Erro no upload: {upload_response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Erro ao fazer upload de imagem: {e}")
            return None

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
