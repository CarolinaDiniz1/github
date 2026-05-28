# LinkedIn Automator — Guia de Instalação

## Como instalar no Chrome

1. Abra o Chrome e acesse `chrome://extensions`
2. Ative o **Modo do desenvolvedor** (canto superior direito)
3. Clique em **"Carregar sem compactação"**
4. Selecione a pasta `linkedin-extension`
5. A extensão aparecerá na barra do Chrome

## Como usar

### Enviar Conexões
1. Abra o LinkedIn e faça uma busca de pessoas (ex.: `linkedin.com/search/results/people/`)
2. Clique no ícone da extensão
3. Aba **Conexões** → configure limite e mensagem opcional
4. Clique em **Enviar Conexões**

### Enviar Mensagens
1. Abra o LinkedIn Messaging (`linkedin.com/messaging/`) ou uma busca de pessoas
2. Aba **Mensagens** → escreva sua mensagem (use `{nome}` para personalizar)
3. Clique em **Enviar Mensagens**

### Interagir com Posts
1. Abra o feed do LinkedIn
2. Aba **Posts** → escolha a ação (curtir, comentar ou ambos)
3. Adicione comentários predefinidos (um por linha)
4. Clique em **Iniciar Interação**

### Extrair Dados
1. Abra uma busca de pessoas no LinkedIn
2. Aba **Extrair** → selecione os campos desejados e o formato (CSV ou JSON)
3. Clique em **Extrair Dados**
4. Após a extração, clique em **Baixar Arquivo**

## Configurações recomendadas

| Parâmetro | Valor seguro | Risco alto |
|---|---|---|
| Conexões/dia | ≤ 25 | > 80 |
| Mensagens/dia | ≤ 20 | > 50 |
| Delay mínimo | 3s | < 1s |
| Modo seguro | Ativado | Desativado |

> **Atenção:** O uso de automação pode violar os Termos de Serviço do LinkedIn.
> Use com responsabilidade e dentro dos limites razoáveis para evitar restrições na conta.
