# Instagram Auto-Poster para LinkedIn e Threads

Sistema de automação que monitora seus posts do Instagram e automaticamente replica o conteúdo no LinkedIn e Threads.

## Funcionalidades

- ✅ Monitora automaticamente novos posts do Instagram
- ✅ Posta automaticamente no LinkedIn
- ✅ Posta automaticamente no Threads
- ✅ Faz download automático de imagens/vídeos
- ✅ Adapta legendas para cada plataforma
- ✅ Execução agendada ou sob demanda
- ✅ Logs detalhados de todas as operações

## Requisitos

- Python 3.8 ou superior
- Contas ativas no Instagram, LinkedIn e Threads
- Credenciais de acesso para cada plataforma

## Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd github
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais

Copie o arquivo de exemplo e configure suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas credenciais:

```env
# Instagram Credentials
INSTAGRAM_USERNAME=seu_usuario_instagram
INSTAGRAM_PASSWORD=sua_senha_instagram

# LinkedIn Credentials
LINKEDIN_EMAIL=seu_email_linkedin
LINKEDIN_PASSWORD=sua_senha_linkedin

# Threads Credentials (usa as mesmas do Instagram)
THREADS_USERNAME=seu_usuario_instagram
THREADS_PASSWORD=sua_senha_instagram

# Configurações
CHECK_INTERVAL_MINUTES=30
LAST_POST_FILE=last_post.json
```

## Uso

### Modo Agendado (Recomendado)

Executa continuamente, verificando novos posts a cada X minutos:

```bash
python main.py
```

O intervalo de verificação é definido pela variável `CHECK_INTERVAL_MINUTES` no arquivo `.env` (padrão: 30 minutos).

### Modo Execução Única

Verifica uma única vez e encerra:

```bash
python main.py --once
```

Útil para testes ou execução via cron.

## Estrutura do Projeto

```
github/
├── main.py                 # Script principal
├── config.py              # Configurações e variáveis de ambiente
├── instagram_client.py    # Cliente do Instagram
├── linkedin_client.py     # Cliente do LinkedIn
├── threads_client.py      # Cliente do Threads
├── requirements.txt       # Dependências Python
├── .env                   # Credenciais (não commitado)
├── .env.example          # Exemplo de credenciais
├── .gitignore            # Arquivos ignorados pelo git
├── last_post.json        # Rastreamento do último post processado
├── temp/                 # Diretório temporário para downloads
└── instagram_autoposter.log  # Arquivo de logs
```

## Como Funciona

1. **Autenticação**: O sistema faz login no Instagram, LinkedIn e Threads
2. **Monitoramento**: Verifica periodicamente o post mais recente do Instagram
3. **Detecção**: Compara com o último post processado
4. **Download**: Faz download da mídia (imagem/vídeo)
5. **Formatação**: Adapta a legenda para cada plataforma
6. **Postagem**: Envia para LinkedIn e Threads
7. **Registro**: Salva o ID do post processado

## Adaptação de Legendas

O sistema adapta automaticamente as legendas para cada plataforma:

### LinkedIn
- Limita hashtags a no máximo 3 (tom mais profissional)
- Adiciona nota: "📸 Compartilhado do Instagram"

### Threads
- Mantém estilo casual
- Adiciona nota: "🔄 Auto-postado do Instagram"

## Limitações Conhecidas

### LinkedIn

Para postar no LinkedIn de forma totalmente automatizada, é necessário:

1. Criar uma aplicação em [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Obter credenciais OAuth 2.0
3. Implementar o fluxo de autenticação OAuth

A implementação atual usa métodos simplificados que podem precisar de ajustes.

### Threads

A API oficial do Threads ainda está em desenvolvimento pela Meta. Opções alternativas:

1. Aguardar a API oficial completa
2. Usar ferramentas de terceiros (Buffer, Hootsuite)
3. Implementação manual via automação de navegador

## Logs

Todos os eventos são registrados em:

- **Console**: Saída em tempo real
- **Arquivo**: `instagram_autoposter.log`

Níveis de log:
- INFO: Operações normais
- WARNING: Avisos (ex: login falhou)
- ERROR: Erros (ex: falha ao postar)

## Segurança

⚠️ **IMPORTANTE**:

- **NUNCA** commite o arquivo `.env` com suas credenciais
- Use senhas fortes e únicas
- Considere usar tokens de API quando disponíveis
- Revise os logs regularmente

## Solução de Problemas

### Erro de Login

```
Erro ao fazer login no Instagram: Challenge required
```

**Solução**: O Instagram detectou login suspeito. Faça login manualmente no app/site primeiro.

### Post não é detectado

```
Post já foi processado anteriormente
```

**Solução**: Delete o arquivo `last_post.json` para reprocessar posts.

### Erro de dependências

```
ModuleNotFoundError: No module named 'instagrapi'
```

**Solução**: Execute `pip install -r requirements.txt`

## Execução em Servidor

### Usando systemd (Linux)

Crie um arquivo `/etc/systemd/system/instagram-autoposter.service`:

```ini
[Unit]
Description=Instagram Auto-Poster
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/caminho/para/github
ExecStart=/usr/bin/python3 /caminho/para/github/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ative e inicie:

```bash
sudo systemctl enable instagram-autoposter
sudo systemctl start instagram-autoposter
sudo systemctl status instagram-autoposter
```

### Usando Docker

Crie um `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Execute:

```bash
docker build -t instagram-autoposter .
docker run -d --name autoposter instagram-autoposter
```

## Desenvolvimento

### Executar em modo debug

Edite `main.py` e mude o nível de log:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Altere de INFO para DEBUG
    ...
)
```

### Testar sem postar

Comente as linhas de postagem em `main.py` para testar sem realmente postar:

```python
# linkedin_success = self.linkedin.post_content(linkedin_caption, media_path)
# threads_success = self.threads.post_with_image(threads_caption, media_path)
```

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Licença

Este projeto é fornecido "como está", sem garantias de qualquer tipo.

## Suporte

Para problemas ou dúvidas:

1. Verifique a seção de Solução de Problemas
2. Revise os logs em `instagram_autoposter.log`
3. Abra uma issue no repositório

## Roadmap

- [ ] Suporte completo à API oficial do LinkedIn
- [ ] Suporte à API oficial do Threads quando disponível
- [ ] Interface web para configuração
- [ ] Suporte a múltiplas contas
- [ ] Agendamento de posts
- [ ] Análise de métricas
- [ ] Suporte a Stories

---

Desenvolvido com ❤️ para automação de redes sociais
