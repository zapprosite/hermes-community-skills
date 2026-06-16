---
name: browseros-mcp-control
description: >
  Use quando a tarefa mencionar BrowserOS, navegador agentico, automacao web,
  controle de abas, formularios, paginas autenticadas, screenshots, extracao
  de pagina, ou "controle o browser". Usa o MCP local do BrowserOS via Hermes.
version: 1.0.0
platforms: [linux]
metadata:
  display-name: BrowserOS MCP Control
  enabled: "true"
  hermes:
    tags: [browseros, browser, mcp, automation, tabs, screenshots]
    category: browser
    requires_toolsets: [browseros, vision, computer_use]
    related_skills: [browseros-webapp-qa, browseros-research-extraction, browseros-hermes-sre, hermes-browser-routing, hermes-browser-unified-guide]
---

# BrowserOS MCP Control

Use o BrowserOS como browser agentico principal quando a tarefa envolver interacao web real. No Hermes, as ferramentas do MCP BrowserOS aparecem prefixadas como `mcp_browseros_<tool>`.

## Estado operacional

- Servico: `browseros-hermes.service`
- Health: `curl -fsS http://127.0.0.1:9000/health`
- MCP: `http://127.0.0.1:9000/mcp`
- CDP interno do BrowserOS: `127.0.0.1:9100`
- Perfil persistente Hermes: `/home/will/.hermes/browseros-profile`
- Log: `/home/will/.hermes/logs/browseros-hermes.log`

Nao coloque chave MiniMax dentro do BrowserOS para uso do Hermes. O cerebro continua no Hermes (`MiniMax-M3`), visao fica em `auxiliary.vision` local (`qwen2.5-vl-7b-instruct`), e BrowserOS e apenas o atuador/observador web via MCP.

## Loop padrao

1. Observe primeiro:
   - `mcp_browseros_get_active_page`
   - `mcp_browseros_list_pages`
   - `mcp_browseros_take_snapshot` ou `mcp_browseros_take_enhanced_snapshot`
2. Escolha a menor acao segura:
   - navegacao: `mcp_browseros_navigate_page`, `mcp_browseros_new_page`
   - clique por elemento: `mcp_browseros_click`
   - clique por coordenada: `mcp_browseros_click_at`
   - texto: `mcp_browseros_fill`, `mcp_browseros_type_at`, `mcp_browseros_press_key`
3. Verifique imediatamente com novo snapshot, conteudo, screenshot ou console.
4. So encadeie a proxima acao depois de confirmar o estado.

## Verificacao de audio e playback visivel

Quando a tarefa for abrir/mostrar um video ou audio para o humano, nao basta ver a aba carregada:

- Confirme que o elemento de midia esta tocando de verdade (`video.paused === false` ou estado equivalente da pagina).
- Confirme fullscreen/tela inteira quando a experiencia for visual.
- Confirme o audio do stream no mixer do sistema antes de dizer que ficou mudo ou resolvido.
- Se o BrowserOS parecer sem som, verifique o stream de audio do proprio navegador no PipeWire/PulseAudio antes de mexer no volume global.
- Para navegadores Chromium/Chrome/BrowserOS, o stream pode aparecer como `Chromium` ou `browseros`; ajuste mute e volume do stream ativo, nao apenas o sink global.

## Escolha de ferramenta

Use snapshots para navegacao e elementos interativos. Use `get_page_content` quando o objetivo for ler/resumir conteudo. Use `get_dom` ou `search_dom` quando precisar de seletor, atributo, estado escondido ou conteudo que nao aparece no snapshot.

Use `take_screenshot` quando layout visual importar. Se o screenshot precisar de interpretacao semantica, passe a imagem para `vision_analyze` usando a visao local do Hermes.

Use `computer_use` apenas quando aparecer dialogo do sistema, seletor de arquivo nativo, permissao fora do DOM, janela externa ou falha que o MCP nao consiga enxergar.

Use Chrome CDP legado (`browser_cdp`) apenas para casos de protocolo baixo nivel nao cobertos pelo BrowserOS MCP.

## Regras de seguranca

- Nao automatize login com 2FA/captcha; peca intervencao manual quando necessario.
- Nao exponha tokens, cookies ou API keys em respostas.
- Confirme antes de submeter formularios que enviam dados, fazem compra, disparam email, publicam conteudo ou alteram contas.
- Para tarefas destrutivas, primeiro mostre o plano de acao e aguarde confirmacao.

## Recuperacao

Se uma ferramenta falhar ou o MCP parecer desconectado:

```bash
systemctl --user status browseros-hermes --no-pager
curl -fsS http://127.0.0.1:9000/health
tail -80 /tmp/browseros-hermes.log
systemctl --user restart browseros-hermes
```

Depois de reiniciar, repita `list_pages` e `take_snapshot` antes de continuar.
