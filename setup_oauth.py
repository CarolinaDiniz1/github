#!/usr/bin/env python3
"""
Script de configuração OAuth para LinkedIn

Este script ajuda você a configurar a autenticação OAuth 2.0
com o LinkedIn para automação de posts.
"""

import json
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests

# Configurações
REDIRECT_URI = "http://localhost:8080/callback"
AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
SCOPES = ["w_member_social", "r_liteprofile", "r_emailaddress"]

# Variáveis globais para capturar o código de autorização
auth_code = None
auth_state = None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handler para capturar o callback OAuth"""

    def do_GET(self):
        global auth_code, auth_state

        # Parse a URL
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)

        if 'code' in params:
            auth_code = params['code'][0]
            auth_state = params.get('state', [None])[0]

            # Responde ao navegador
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <head><title>Autorizacao Concluida</title></head>
                <body>
                    <h1>Autorizacao concluida com sucesso!</h1>
                    <p>Voce pode fechar esta janela e voltar ao terminal.</p>
                </body>
                </html>
            """)
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <head><title>Erro</title></head>
                <body>
                    <h1>Erro na autorizacao!</h1>
                    <p>Codigo de autorizacao nao encontrado.</p>
                </body>
                </html>
            """)

    def log_message(self, format, *args):
        # Suprime logs do servidor HTTP
        pass


def get_authorization_url(client_id, state="random_state_string"):
    """Gera a URL de autorização"""
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': ' '.join(SCOPES)
    }

    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return f"{AUTHORIZATION_URL}?{query_string}"


def exchange_code_for_token(client_id, client_secret, auth_code):
    """Troca o código de autorização por um access token"""
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(TOKEN_URL, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter token: {response.status_code}")
        print(response.text)
        return None


def save_oauth_config(config):
    """Salva a configuração OAuth em arquivo"""
    with open('oauth_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("\n✓ Configuração OAuth salva em oauth_config.json")


def load_oauth_config():
    """Carrega configuração OAuth existente"""
    if os.path.exists('oauth_config.json'):
        with open('oauth_config.json', 'r') as f:
            return json.load(f)
    return {}


def setup_linkedin_oauth():
    """Processo completo de configuração OAuth para LinkedIn"""
    print("=" * 60)
    print("CONFIGURAÇÃO OAUTH - LINKEDIN")
    print("=" * 60)
    print()
    print("Antes de começar, você precisa:")
    print("1. Criar uma aplicação em https://www.linkedin.com/developers/")
    print("2. Adicionar redirect URI: http://localhost:8080/callback")
    print("3. Solicitar permissões: w_member_social")
    print()

    # Solicita credenciais
    client_id = input("Digite seu LinkedIn Client ID: ").strip()
    client_secret = input("Digite seu LinkedIn Client Secret: ").strip()

    if not client_id or not client_secret:
        print("✗ Client ID e Client Secret são obrigatórios!")
        return

    # Gera URL de autorização
    auth_url = get_authorization_url(client_id)

    print()
    print("Abrindo navegador para autorização...")
    print(f"Se não abrir automaticamente, acesse: {auth_url}")
    print()

    # Abre navegador
    webbrowser.open(auth_url)

    # Inicia servidor HTTP para capturar callback
    print("Aguardando autorização...")
    print("(Servidor rodando em http://localhost:8080)")
    print()

    server = HTTPServer(('localhost', 8080), OAuthCallbackHandler)

    # Aguarda uma requisição (o callback)
    server.handle_request()

    if auth_code:
        print("✓ Código de autorização recebido!")
        print("Trocando código por access token...")

        token_data = exchange_code_for_token(client_id, client_secret, auth_code)

        if token_data:
            print("✓ Access token obtido com sucesso!")

            # Salva configuração
            config = {
                'linkedin': {
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'access_token': token_data['access_token'],
                    'expires_in': token_data.get('expires_in'),
                    'refresh_token': token_data.get('refresh_token'),
                    'scope': token_data.get('scope')
                }
            }

            # Carrega config existente e atualiza
            existing_config = load_oauth_config()
            existing_config.update(config)
            save_oauth_config(existing_config)

            print()
            print("=" * 60)
            print("CONFIGURAÇÃO CONCLUÍDA!")
            print("=" * 60)
            print(f"Access Token: {token_data['access_token'][:20]}...")
            print(f"Expira em: {token_data.get('expires_in', 'N/A')} segundos")
            print()
            print("IMPORTANTE: Guarde o arquivo oauth_config.json em segurança!")
            print("Não compartilhe este arquivo com ninguém.")
            print()
        else:
            print("✗ Erro ao obter access token")
    else:
        print("✗ Não foi possível obter o código de autorização")


def setup_threads_config():
    """Configuração para Threads"""
    print()
    print("=" * 60)
    print("CONFIGURAÇÃO - THREADS")
    print("=" * 60)
    print()
    print("IMPORTANTE: A API oficial do Threads ainda está em desenvolvimento.")
    print()
    print("Opções disponíveis:")
    print("1. Usar a mesma autenticação do Instagram (método atual)")
    print("2. Aguardar API oficial da Meta")
    print("3. Usar ferramentas de terceiros (Buffer, Hootsuite, etc.)")
    print()
    print("Recomendação: Por enquanto, use as credenciais do Instagram")
    print("que já estão configuradas no arquivo .env")
    print()

    config = load_oauth_config()
    config['threads'] = {
        'status': 'Usando credenciais do Instagram',
        'method': 'instagram_auth',
        'note': 'API oficial em desenvolvimento'
    }
    save_oauth_config(config)


def main():
    """Função principal"""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "SETUP DE AUTENTICAÇÃO - REDES SOCIAIS" + " " * 10 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    while True:
        print("\nEscolha uma opção:")
        print("1. Configurar OAuth do LinkedIn")
        print("2. Configurar Threads")
        print("3. Ver configurações atuais")
        print("4. Sair")
        print()

        choice = input("Opção: ").strip()

        if choice == '1':
            setup_linkedin_oauth()
        elif choice == '2':
            setup_threads_config()
        elif choice == '3':
            config = load_oauth_config()
            print()
            print("=" * 60)
            print("CONFIGURAÇÕES ATUAIS")
            print("=" * 60)
            print(json.dumps(config, indent=2))
            print()
        elif choice == '4':
            print("\nEncerrando...")
            break
        else:
            print("✗ Opção inválida!")


if __name__ == "__main__":
    main()
