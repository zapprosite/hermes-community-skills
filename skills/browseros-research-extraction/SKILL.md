---
name: browseros-research-extraction
description: >
  Use quando o usuario pedir pesquisa em paginas autenticadas, extracao de
  dados, scraping assistido, coleta de links, resumo de pagina, download de
  arquivos, relatorios ou navegacao por varias abas usando BrowserOS.
version: 1.0.0
platforms: [linux]
metadata:
  display-name: BrowserOS Research Extraction
  enabled: "true"
  hermes:
    tags: [browseros, research, extraction, authenticated, reports, downloads]
    category: browser
    requires_toolsets: [browseros, web, file, vision]
    related_skills: [browseros-mcp-control, hermes-browser-routing]
---

# BrowserOS Research Extraction

Use BrowserOS quando a pesquisa exigir estado real de navegador, paginas autenticadas, historico, UI dinamica, downloads ou interacao com paginas que `web_extract` nao consegue acessar.

## Padrao de extracao

1. Abra a pagina com `mcp_browseros_new_page`.
2. Identifique a pagina ativa com `mcp_browseros_get_active_page`.
3. Use `mcp_browseros_get_page_content` para conteudo limpo em Markdown.
4. Use `mcp_browseros_get_page_links` para mapear navegacao e fontes.
5. Use `mcp_browseros_search_dom` para encontrar itens especificos.
6. Use `mcp_browseros_get_dom` apenas quando o conteudo limpo/snapshot nao bastar.
7. Para dados visuais, use `mcp_browseros_take_screenshot` e depois `vision_analyze`.

## Dados estruturados

Quando o usuario pedir tabela, JSON, CSV ou lista:

- Defina o schema mental antes de extrair.
- Leia os titulos/colunas primeiro.
- Paginar ou scrollar devagar, verificando com snapshot a cada pagina.
- Deduplicate por URL, ID, titulo ou data.
- Preserve URLs de origem para auditoria.

## Downloads

Use `mcp_browseros_download_file` quando a pagina disponibilizar arquivo. Confirme destino e nome se o usuario nao especificou. Depois valide no filesystem com ferramentas de arquivo/terminal.

## Saida

Relatorios devem incluir:

- Fontes ou URLs visitadas.
- Data/hora da coleta quando relevante.
- Lacunas e paginas que exigiram login ou falharam.
- Separacao clara entre dado observado e inferencia.

## Privacidade e limites

Nao extraia informacao pessoal sensivel alem do pedido. Nao contorne paywall, captcha ou controles de acesso. Para acoes em apps autenticados, prefira leitura e confirmacao antes de qualquer escrita.
