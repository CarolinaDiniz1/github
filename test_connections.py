#!/usr/bin/env python3
"""
Script de teste de conexões

Testa as conexões com Instagram, LinkedIn e Threads
para verificar se as credenciais estão configuradas corretamente.
"""

import json
import os
import sys
import logging
from pathlib import Path

# Importa os clientes
import config
from instagram_client import InstagramClient
from linkedin_client import LinkedInClient
from threads_client import ThreadsClient

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ConnectionTester:
    """Testa conexões com as plataformas"""

    def __init__(self):
        self.results = {
            'instagram': {'status': 'not_tested', 'message': ''},
            'linkedin': {'status': 'not_tested', 'message': ''},
            'threads': {'status': 'not_tested', 'message': ''}
        }

    def test_instagram(self):
        """Testa conexão com Instagram"""
        print("\n" + "=" * 60)
        print("TESTANDO INSTAGRAM")
        print("=" * 60)

        try:
            if not config.INSTAGRAM_USERNAME or not config.INSTAGRAM_PASSWORD:
                self.results['instagram'] = {
                    'status': 'error',
                    'message': 'Credenciais não configuradas no .env'
                }
                print("✗ Credenciais não configuradas")
                return False

            print(f"Usuário: {config.INSTAGRAM_USERNAME}")
            print("Tentando fazer login...")

            client = InstagramClient()
            if client.login():
                print("✓ Login realizado com sucesso!")

                # Tenta obter informações do usuário
                print("Obtendo informações do perfil...")
                try:
                    user_id = client.client.user_id_from_username(config.INSTAGRAM_USERNAME)
                    user_info = client.client.user_info(user_id)

                    print(f"✓ Perfil encontrado:")
                    print(f"  - Nome: {user_info.full_name}")
                    print(f"  - Seguidores: {user_info.follower_count}")
                    print(f"  - Seguindo: {user_info.following_count}")
                    print(f"  - Posts: {user_info.media_count}")

                    self.results['instagram'] = {
                        'status': 'success',
                        'message': 'Conectado com sucesso',
                        'user_info': {
                            'username': config.INSTAGRAM_USERNAME,
                            'full_name': user_info.full_name,
                            'followers': user_info.follower_count,
                            'posts': user_info.media_count
                        }
                    }
                    return True
                except Exception as e:
                    print(f"✓ Login OK, mas erro ao obter perfil: {e}")
                    self.results['instagram'] = {
                        'status': 'warning',
                        'message': f'Login OK, erro ao obter perfil: {str(e)}'
                    }
                    return True
            else:
                self.results['instagram'] = {
                    'status': 'error',
                    'message': 'Falha no login'
                }
                print("✗ Falha no login")
                return False

        except Exception as e:
            self.results['instagram'] = {
                'status': 'error',
                'message': str(e)
            }
            print(f"✗ Erro: {e}")
            return False

    def test_linkedin(self):
        """Testa conexão com LinkedIn"""
        print("\n" + "=" * 60)
        print("TESTANDO LINKEDIN")
        print("=" * 60)

        try:
            # Verifica se tem OAuth configurado
            oauth_config = self.load_oauth_config()

            if oauth_config and 'linkedin' in oauth_config:
                print("✓ Configuração OAuth encontrada")
                access_token = oauth_config['linkedin'].get('access_token')

                if access_token:
                    print("Testando access token...")

                    # Testa o token fazendo uma chamada à API
                    import requests
                    headers = {
                        'Authorization': f'Bearer {access_token}'
                    }
                    response = requests.get('https://api.linkedin.com/v2/me', headers=headers)

                    if response.status_code == 200:
                        user_data = response.json()
                        print("✓ Token válido!")
                        print(f"  - ID: {user_data.get('id')}")
                        print(f"  - Nome: {user_data.get('localizedFirstName')} {user_data.get('localizedLastName')}")

                        self.results['linkedin'] = {
                            'status': 'success',
                            'message': 'OAuth configurado e funcionando',
                            'user_info': {
                                'id': user_data.get('id'),
                                'name': f"{user_data.get('localizedFirstName')} {user_data.get('localizedLastName')}"
                            }
                        }
                        return True
                    elif response.status_code == 401:
                        print("✗ Token expirado ou inválido")
                        print("Execute: python setup_oauth.py")
                        self.results['linkedin'] = {
                            'status': 'error',
                            'message': 'Token expirado - execute setup_oauth.py'
                        }
                        return False
                    else:
                        print(f"✗ Erro na API: {response.status_code}")
                        self.results['linkedin'] = {
                            'status': 'error',
                            'message': f'Erro na API: {response.status_code}'
                        }
                        return False
            else:
                # Tenta método tradicional
                if not config.LINKEDIN_EMAIL or not config.LINKEDIN_PASSWORD:
                    print("✗ OAuth não configurado e credenciais .env não encontradas")
                    print("\nPara configurar OAuth:")
                    print("  python setup_oauth.py")
                    self.results['linkedin'] = {
                        'status': 'error',
                        'message': 'OAuth não configurado - execute setup_oauth.py'
                    }
                    return False

                print(f"Email: {config.LINKEDIN_EMAIL}")
                print("Tentando login tradicional...")

                client = LinkedInClient()
                if client.login():
                    print("✓ Login realizado!")
                    print("\n⚠ AVISO: Para automação completa, configure OAuth:")
                    print("  python setup_oauth.py")

                    self.results['linkedin'] = {
                        'status': 'warning',
                        'message': 'Login OK, mas OAuth recomendado'
                    }
                    return True
                else:
                    print("✗ Falha no login")
                    self.results['linkedin'] = {
                        'status': 'error',
                        'message': 'Falha no login'
                    }
                    return False

        except Exception as e:
            self.results['linkedin'] = {
                'status': 'error',
                'message': str(e)
            }
            print(f"✗ Erro: {e}")
            return False

    def test_threads(self):
        """Testa conexão com Threads"""
        print("\n" + "=" * 60)
        print("TESTANDO THREADS")
        print("=" * 60)

        try:
            if not config.THREADS_USERNAME or not config.THREADS_PASSWORD:
                print("✗ Credenciais não configuradas no .env")
                print("(Threads usa as mesmas credenciais do Instagram)")
                self.results['threads'] = {
                    'status': 'error',
                    'message': 'Credenciais não configuradas'
                }
                return False

            print(f"Usuário: {config.THREADS_USERNAME}")
            print("Tentando fazer login...")

            client = ThreadsClient()
            if client.login():
                print("✓ Login realizado!")
                print("\n⚠ NOTA: A API do Threads ainda é limitada")
                print("Posts podem não funcionar até a API oficial ser lançada")

                self.results['threads'] = {
                    'status': 'warning',
                    'message': 'Login OK, mas API limitada'
                }
                return True
            else:
                print("✗ Falha no login")
                self.results['threads'] = {
                    'status': 'error',
                    'message': 'Falha no login'
                }
                return False

        except Exception as e:
            self.results['threads'] = {
                'status': 'error',
                'message': str(e)
            }
            print(f"✗ Erro: {e}")
            return False

    def load_oauth_config(self):
        """Carrega configuração OAuth"""
        try:
            if os.path.exists('oauth_config.json'):
                with open('oauth_config.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar oauth_config.json: {e}")
        return None

    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "=" * 60)
        print("RESUMO DOS TESTES")
        print("=" * 60)

        status_symbols = {
            'success': '✓',
            'warning': '⚠',
            'error': '✗',
            'not_tested': '?'
        }

        for platform, result in self.results.items():
            status = result['status']
            symbol = status_symbols.get(status, '?')
            message = result.get('message', '')

            print(f"\n{platform.upper()}:")
            print(f"  {symbol} Status: {status}")
            if message:
                print(f"  Mensagem: {message}")

        print("\n" + "=" * 60)

        # Conta sucessos
        success_count = sum(1 for r in self.results.values() if r['status'] in ['success', 'warning'])
        total_count = len(self.results)

        print(f"\nPlataformas funcionando: {success_count}/{total_count}")

        if success_count == total_count:
            print("\n🎉 Todas as plataformas estão configuradas!")
        elif success_count > 0:
            print("\n⚠ Algumas plataformas precisam de configuração")
        else:
            print("\n✗ Nenhuma plataforma está configurada corretamente")

        print()

    def run_all_tests(self):
        """Executa todos os testes"""
        print("\n╔" + "=" * 58 + "╗")
        print("║" + " " * 15 + "TESTE DE CONEXÕES" + " " * 25 + "║")
        print("╚" + "=" * 58 + "╝")

        # Verifica se .env existe
        if not os.path.exists('.env'):
            print("\n✗ Arquivo .env não encontrado!")
            print("\nPara criar:")
            print("  cp .env.example .env")
            print("  # Edite o .env com suas credenciais")
            return False

        self.test_instagram()
        self.test_linkedin()
        self.test_threads()
        self.print_summary()

        # Salva resultados
        self.save_results()

        return all(r['status'] in ['success', 'warning'] for r in self.results.values())

    def save_results(self):
        """Salva resultados dos testes"""
        try:
            with open('test_results.json', 'w') as f:
                json.dump(self.results, f, indent=2)
            print("Resultados salvos em test_results.json")
        except Exception as e:
            logger.error(f"Erro ao salvar resultados: {e}")


def main():
    """Função principal"""
    tester = ConnectionTester()

    if len(sys.argv) > 1:
        # Testa plataforma específica
        platform = sys.argv[1].lower()

        if platform == 'instagram':
            tester.test_instagram()
        elif platform == 'linkedin':
            tester.test_linkedin()
        elif platform == 'threads':
            tester.test_threads()
        else:
            print(f"Plataforma desconhecida: {platform}")
            print("Use: instagram, linkedin ou threads")
            sys.exit(1)
    else:
        # Testa todas
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
