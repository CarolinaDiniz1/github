from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import config
import logging

logger = logging.getLogger(__name__)

class InstagramClient:
    def __init__(self):
        self.client = Client()
        self.client.delay_range = [1, 3]

    def login(self):
        """Faz login no Instagram"""
        try:
            logger.info(f"Fazendo login no Instagram como {config.INSTAGRAM_USERNAME}")
            self.client.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)
            logger.info("Login no Instagram realizado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao fazer login no Instagram: {e}")
            return False

    def get_latest_post(self):
        """Obtém o post mais recente do feed do usuário"""
        try:
            user_id = self.client.user_id_from_username(config.INSTAGRAM_USERNAME)
            medias = self.client.user_medias(user_id, amount=1)

            if not medias:
                logger.warning("Nenhum post encontrado")
                return None

            latest_media = medias[0]

            post_data = {
                'id': latest_media.pk,
                'caption': latest_media.caption_text,
                'media_type': latest_media.media_type,
                'timestamp': latest_media.taken_at,
                'likes': latest_media.like_count,
                'comments': latest_media.comment_count
            }

            # Download da imagem/vídeo
            if latest_media.media_type == 1:  # Foto
                photo_path = self.client.photo_download(latest_media.pk, folder='temp')
                post_data['media_path'] = str(photo_path)
            elif latest_media.media_type == 2:  # Vídeo
                video_path = self.client.video_download(latest_media.pk, folder='temp')
                post_data['media_path'] = str(video_path)
            elif latest_media.media_type == 8:  # Carrossel
                # Para carrossel, pega a primeira mídia
                resources = latest_media.resources
                if resources:
                    if resources[0].media_type == 1:
                        photo_path = self.client.photo_download(resources[0].pk, folder='temp')
                        post_data['media_path'] = str(photo_path)
                    else:
                        video_path = self.client.video_download(resources[0].pk, folder='temp')
                        post_data['media_path'] = str(video_path)

            logger.info(f"Post obtido: {post_data['id']}")
            return post_data

        except LoginRequired:
            logger.error("Sessão expirada, fazendo login novamente")
            self.login()
            return self.get_latest_post()
        except Exception as e:
            logger.error(f"Erro ao obter último post: {e}")
            return None
