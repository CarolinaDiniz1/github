# Guia de Configuração das Plataformas

Este guia detalha como configurar cada plataforma (Instagram, LinkedIn e Threads) para automação.

## Índice

1. [Configuração do Instagram](#1-configuração-do-instagram)
2. [Configuração do LinkedIn](#2-configuração-do-linkedin)
3. [Configuração do Threads](#3-configuração-do-threads)
4. [Teste das Conexões](#4-teste-das-conexões)
5. [Resolução de Problemas](#5-resolução-de-problemas)

---

## 1. Configuração do Instagram

### Pré-requisitos
- Conta ativa do Instagram
- Acesso ao email e telefone da conta (para autenticação em dois fatores, se ativado)

### Passos

#### 1.1. Configure as credenciais

Edite o arquivo `.env`:

```env
INSTAGRAM_USERNAME=seu_usuario_instagram
INSTAGRAM_PASSWORD=sua_senha_instagram
```

#### 1.2. Considerações de Segurança

⚠️ **Importante**:

- Use uma senha forte e única
- Se tiver autenticação em dois fatores (2FA), pode ser necessário gerar um código de app
- O Instagram pode bloquear logins suspeitos - neste caso, faça login manual primeiro no app/site

#### 1.3. Teste a conexão

```bash
python test_connections.py instagram
```

### Limitações

- A API não oficial pode ter restrições de taxa (rate limiting)
- O Instagram pode requerer verificação adicional ocasionalmente
- Recomenda-se não exceder 100 ações por hora

---

## 2. Configuração do LinkedIn

O LinkedIn oferece duas formas de autenticação: **Método Tradicional** (simples mas limitado) e **OAuth 2.0** (recomendado para automação).

### Método 1: OAuth 2.0 (Recomendado)

#### 2.1. Crie uma Aplicação LinkedIn

1. Acesse [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Clique em "Create app"
3. Preencha os dados:
   - **App name**: Instagram Auto-Poster (ou nome de sua escolha)
   - **LinkedIn Page**: Selecione sua página do LinkedIn
   - **Privacy policy URL**: URL da política de privacidade (pode ser do seu site)
   - **App logo**: Upload de um logo
4. Clique em "Create app"

#### 2.2. Configure a Aplicação

1. Na aba **Auth**, anote:
   - **Client ID**
   - **Client Secret** (clique em "Show" para ver)

2. Adicione **Redirect URL**:
   ```
   http://localhost:8080/callback
   ```

3. Na aba **Products**, solicite acesso:
   - **Share on LinkedIn** (para postar conteúdo)
   - **Sign In with LinkedIn** (para autenticação)

4. Aguarde aprovação (geralmente instantânea para uso pessoal)

#### 2.3. Execute o Setup OAuth

```bash
python setup_oauth.py
```

Siga os passos:
1. Escolha opção "1. Configurar OAuth do LinkedIn"
2. Cole o **Client ID**
3. Cole o **Client Secret**
4. Uma janela do navegador abrirá
5. Faça login no LinkedIn e autorize a aplicação
6. Retorne ao terminal - a configuração será salva automaticamente

#### 2.4. Verifique a configuração

```bash
python test_connections.py linkedin
```

Se tudo estiver OK, você verá:
```
✓ Token válido!
  - ID: [seu_id]
  - Nome: [seu_nome]
```

### Método 2: Tradicional (Limitado)

⚠️ **Não recomendado** - Não permite postagem automatizada completa

Edite o arquivo `.env`:

```env
LINKEDIN_EMAIL=seu_email@exemplo.com
LINKEDIN_PASSWORD=sua_senha_linkedin
```

### Permissões Necessárias

Para postar automaticamente, você precisa das seguintes permissões OAuth:

- `w_member_social` - Escrever posts como você
- `r_liteprofile` - Ler informações básicas do perfil
- `r_emailaddress` - Ler endereço de email (para identificação)

### Estrutura do oauth_config.json

Após configurar, o arquivo terá esta estrutura:

```json
{
  "linkedin": {
    "client_id": "seu_client_id",
    "client_secret": "seu_client_secret",
    "access_token": "seu_access_token_gerado",
    "expires_in": 5184000,
    "refresh_token": "seu_refresh_token",
    "scope": "r_emailaddress,r_liteprofile,w_member_social"
  }
}
```

⚠️ **Importante**: Adicione `oauth_config.json` ao `.gitignore` (já está configurado)

---

## 3. Configuração do Threads

### Status da API

⚠️ **A API oficial do Threads ainda está em desenvolvimento pela Meta.**

### Opções Disponíveis

#### Opção 1: Usar Credenciais do Instagram (Método Atual)

O Threads usa a mesma conta do Instagram, então configure:

```env
THREADS_USERNAME=seu_usuario_instagram
THREADS_PASSWORD=sua_senha_instagram
```

**Limitações**:
- API não oficial limitada
- Funcionalidade de postagem pode não funcionar completamente
- Sujeito a mudanças pela Meta

#### Opção 2: Aguardar API Oficial

A Meta está desenvolvendo a API oficial do Threads. Quando lançada:

1. Terá suporte completo a OAuth 2.0
2. Integração similar ao Instagram Graph API
3. Funcionalidades completas de postagem

**Cronograma**: Não há data oficial ainda.

#### Opção 3: Ferramentas de Terceiros

Use plataformas que já têm integração:

- **Buffer**: https://buffer.com
- **Hootsuite**: https://hootsuite.com
- **Later**: https://later.com

Estas ferramentas têm parceria com a Meta e oferecem APIs próprias.

### Teste (Limitado)

```bash
python test_connections.py threads
```

### Executar Setup do Threads

```bash
python setup_oauth.py
```

Escolha opção "2. Configurar Threads"

---

## 4. Teste das Conexões

### Testar Todas as Plataformas

```bash
python test_connections.py
```

Saída esperada:

```
╔══════════════════════════════════════════════════════════╗
║               TESTE DE CONEXÕES                          ║
╚══════════════════════════════════════════════════════════╝

============================================================
TESTANDO INSTAGRAM
============================================================
Usuário: seu_usuario
Tentando fazer login...
✓ Login realizado com sucesso!
✓ Perfil encontrado:
  - Nome: Seu Nome
  - Seguidores: 1234
  - Seguindo: 567
  - Posts: 89

============================================================
TESTANDO LINKEDIN
============================================================
✓ Configuração OAuth encontrada
Testando access token...
✓ Token válido!
  - ID: abc123
  - Nome: Seu Nome

============================================================
TESTANDO THREADS
============================================================
Usuário: seu_usuario
Tentando fazer login...
✓ Login realizado!

⚠ NOTA: A API do Threads ainda é limitada
Posts podem não funcionar até a API oficial ser lançada

============================================================
RESUMO DOS TESTES
============================================================

INSTAGRAM:
  ✓ Status: success
  Mensagem: Conectado com sucesso

LINKEDIN:
  ✓ Status: success
  Mensagem: OAuth configurado e funcionando

THREADS:
  ⚠ Status: warning
  Mensagem: Login OK, mas API limitada

============================================================

Plataformas funcionando: 3/3

🎉 Todas as plataformas estão configuradas!
```

### Testar Plataforma Específica

```bash
python test_connections.py instagram
python test_connections.py linkedin
python test_connections.py threads
```

---

## 5. Resolução de Problemas

### Instagram

#### Erro: "Challenge required"

**Problema**: O Instagram detectou login suspeito

**Solução**:
1. Faça login manualmente no app ou site
2. Complete qualquer verificação solicitada
3. Tente novamente após 15 minutos

#### Erro: "Bad Password"

**Problema**: Senha incorreta ou credenciais inválidas

**Solução**:
1. Verifique o arquivo `.env`
2. Certifique-se que não há espaços extras
3. Se usar caracteres especiais, coloque entre aspas

#### Erro: "Two-factor authentication required"

**Problema**: 2FA está ativado

**Solução**:
1. Acesse Instagram > Settings > Security > Two-Factor Authentication
2. Gere um código de backup/app
3. Use esse código no `.env`

### LinkedIn

#### Erro: "Token expirado"

**Problema**: Access token OAuth expirou (geralmente 60 dias)

**Solução**:
```bash
python setup_oauth.py
```

Refaça a autorização OAuth.

#### Erro: "Invalid Client ID/Secret"

**Problema**: Credenciais OAuth incorretas

**Solução**:
1. Verifique no [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Copie novamente Client ID e Secret
3. Execute `python setup_oauth.py` novamente

#### Erro: "Redirect URI mismatch"

**Problema**: URL de redirect não configurada

**Solução**:
1. Acesse sua app no LinkedIn Developers
2. Vá em Auth > Authorized redirect URLs
3. Adicione: `http://localhost:8080/callback`
4. Salve e tente novamente

#### Erro 403: "Insufficient permissions"

**Problema**: Permissões OAuth não aprovadas

**Solução**:
1. Acesse sua app no LinkedIn Developers
2. Vá em Products
3. Solicite "Share on LinkedIn"
4. Aguarde aprovação (pode levar alguns minutos)

### Threads

#### "API limitada"

**Problema**: API não oficial limitada

**Solução**:
- **Temporária**: Use ferramentas de terceiros (Buffer, Hootsuite)
- **Futura**: Aguarde API oficial da Meta

#### Login falha

**Problema**: Credenciais incorretas ou API mudou

**Solução**:
1. Verifique credenciais do Instagram (Threads usa as mesmas)
2. Aguarde atualizações do código para mudanças na API

### Geral

#### Erro: "No module named 'X'"

**Problema**: Dependências não instaladas

**Solução**:
```bash
pip install -r requirements.txt
```

#### Erro: "Permission denied"

**Problema**: Arquivo sem permissão de execução

**Solução**:
```bash
chmod +x setup_oauth.py test_connections.py main.py
```

#### Logs não aparecem

**Problema**: Arquivo de log sem permissão

**Solução**:
```bash
rm instagram_autoposter.log
python main.py
```

---

## Próximos Passos

Após configurar todas as plataformas:

1. **Execute o teste completo**:
   ```bash
   python test_connections.py
   ```

2. **Teste uma execução única**:
   ```bash
   python main.py --once
   ```

3. **Inicie o modo automático**:
   ```bash
   python main.py
   ```

4. **Configure execução contínua** (opcional):
   - [Systemd](README.md#usando-systemd-linux)
   - [Docker](README.md#usando-docker)
   - Cron (para execuções periódicas)

---

## Suporte

Se encontrar problemas:

1. ✓ Verifique esta documentação
2. ✓ Revise os logs em `instagram_autoposter.log`
3. ✓ Execute `python test_connections.py` para diagnóstico
4. ✓ Consulte a seção de Resolução de Problemas
5. ✗ Abra uma issue no repositório com:
   - Descrição do problema
   - Logs relevantes (SEM credenciais!)
   - Plataforma e versão do Python

---

## Recursos Úteis

- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [LinkedIn API Documentation](https://docs.microsoft.com/en-us/linkedin/)
- [LinkedIn Developers](https://www.linkedin.com/developers/)
- [Threads API (futuro)](https://developers.facebook.com/docs/threads)
- [Meta for Developers](https://developers.facebook.com/)

---

**Última atualização**: 2025-12-11
