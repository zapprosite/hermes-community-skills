---
name: browseros-music-playback-routing
description: "Roteamento visível de música/vídeo no BrowserOS: escolhe o monitor certo, prioriza vídeos oficiais/playlist oficial, toca em tela cheia e valida áudio/playback antes de responder."
version: 1.0.0
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [browseros, music, youtube, playlists, official-video, fullscreen, audio, monitor-routing]
    category: browser
    related_skills: [browseros-mcp-control, browseros-research-extraction, monitor-aware-browser-routing]
---

# BrowserOS Music Playback Routing

Use esta skill quando o Senhor pedir para tocar música, playlist, clipe oficial ou vídeo musical de forma visível no BrowserOS.

## Objetivo

- Mostrar o conteúdo no BrowserOS visível para humano.
- Usar o monitor correto quando houver múltiplos displays.
- Priorizar vídeos oficiais, clipes oficiais e playlists compostas por vídeos originais.
- Evitar falsos positivos de Camofox ou de janelas que não mudaram no desktop físico.
- Deixar tocando em tela cheia quando a intenção for assistir.

## Fluxo padrão

1. Confirmar que a navegação é visível para humano. Se sim, a rota é BrowserOS.
2. Se houver múltiplos monitores, identificar o monitor alvo com `xrandr` e a janela real com `wmctrl` antes de agir.
3. Reusar a janela já aberta do BrowserOS; não abrir outro navegador à toa.
4. Consultar o sistema para saber a data atual e usar o ano corrente como base da busca.
5. Pesquisar usando o ano atual + gênero + termos como `official video`, `official music video`, `clipe oficial`, `vídeo oficial` ou `playlist oficial`.
6. Validar o resultado antes de tocar:
   - título com `Official Video` / `Official Music Video` / `Clipe Oficial` / `Vídeo Oficial`
   - canal do artista, selo, playlist oficial ou compilação de vídeos oficiais
   - rejeitar áudio-only, lyric video, live session, topic e reupload
7. Abrir a playlist ou o primeiro vídeo oficial realmente compatível com o pedido.
8. Garantir localização e apresentação antes de responder:
   - abrir o YouTube com idioma PT-BR quando o Senhor não pedir outro idioma (`hl=pt-BR`, `persist_hl=1`, ou validação equivalente)
   - maximizar a janela visível do BrowserOS (`_NET_WM_STATE_MAXIMIZED_HORZ` e `_NET_WM_STATE_MAXIMIZED_VERT`)
   - não confundir “abriu a URL” com “pronto para assistir”
9. Garantir reprodução:
   - vídeo não pausado (`paused === false`)
   - áudio não-mudo
   - volume acima de zero
   - se o vídeo pausar, forçar play antes de encerrar a ação
10. Garantir tela cheia quando o pedido for para assistir em fullscreen e confirmar o estado fullscreen depois de acionar o player. Se o pedido for apenas “abrir no navegador”, maximizado basta, salvo instrução contrária.
11. Responder só com a confirmação curta esperada pelo usuário.

## Channel playback flow

When the user asks for a specific channel's newest video:

- open the channel's `/videos` page with `sort=dd` or the visible newest-first list
- read the actual visible entries and choose the most recent upload from today's date context
- verify the title/channel pair matches the requested creator before playing
- prefer the first visible newest upload over older search hits

## YouTube channel workflow

Quando o usuário pedir o último vídeo de um canal:

1. Abrir a página `/videos` do canal.
2. Inspecionar o grid/lista e localizar o primeiro `watch?v=` real.
3. Abrir o watch URL diretamente no BrowserOS.
4. Forçar play e validar áudio.
5. Entrar em fullscreen quando o usuário quiser assistir.

## Pitfalls aprendidos

- Não confundir BrowserOS com Camofox: Camofox é para scraping/background/backoffice; BrowserOS é a rota visível para humano. Se o Senhor corrigir “tem que ser BrowserOS”, reabrir imediatamente no BrowserOS e validar a janela real.
- Para vídeos do YouTube visíveis ao Senhor, o padrão é PT-BR. Validar idioma/título em português quando possível; não deixar em inglês por descuido.
- Abrir a URL não basta: maximizar a janela visível do BrowserOS e iniciar playback antes de responder.
- Não confiar em um estado de carregamento como prova de reprodução. Verificar `video.paused === false`, `muted === false`, volume acima de zero e o relógio correndo.
- Em YouTube, clicar em `Play all` nem sempre basta; às vezes é melhor abrir o primeiro `watch?v=` oficial e forçar play.
- Não confiar em um estado de carregamento como prova de reprodução. Verificar `video.paused === false` e o relógio correndo.
- Em YouTube, clicar em `Play all` nem sempre basta; às vezes é melhor abrir o primeiro `watch?v=` oficial e forçar play.
- A tela cheia precisa ser confirmada por DOM/estado do player, não por suposição visual.
- Se o vídeo não for original, voltar à busca e procurar outro resultado melhor.

## Regras de seleção

- Para rock internacional, usar o top do gênero no ano atual e preferir clipes oficiais.
- Para rock brasileiro, preferir clipes oficiais nacionais e playlists com vídeos originais.
- Para qualquer gênero, se a playlist tiver título bom mas os itens forem áudio-only ou reupload, rejeitar e buscar outra.
- Se o primeiro resultado não for original, continue procurando até encontrar um resultado melhor.
- Se o nome do canal for ambíguo ou parecido com outro canal, resolver a identidade do canal antes de tocar (ex.: confirmar handle, título da página, ou página `/videos`).
- Quando o usuário pedir "o último vídeo" de um canal, abrir a página de vídeos do canal e escolher o upload mais recente visível antes de tocar.
- Se a busca retornar um canal errado mas similar, parar e corrigir a identificação em vez de tocar o vídeo errado.

## Fluxo de canal no YouTube

Quando o pedido for "abre o canal X e toca o último vídeo":

1. Pesquisar o canal exato pelo nome/handle.
2. Confirmar que o resultado bate com o canal pedido, não apenas com um nome parecido.
3. Ir para a página de vídeos do canal com ordenação por mais recentes.
4. Verificar o primeiro item visível como o upload mais recente.
5. Abrir esse vídeo e validar reprodução.
6. Só então expandir para tela cheia, se o pedido for visível para humano.

## Verificações finais

Antes de dizer que está pronto:
- a janela do BrowserOS apareceu no desktop físico
- o monitor certo está sendo usado
- o vídeo está em reprodução
- o áudio está ativo
- a tela cheia está ligada quando pedido
- para canais do YouTube, o vídeo aberto corresponde ao canal exato pedido, não a um canal parecido

## Resposta padrão

Quando o usuário pedir apenas para tocar uma playlist, responder de forma curta e direta após validar tudo.

## Referências

- `references/youtube-visible-playback-ptbr-maximized-2026-06-09.md` — correção de fluxo: BrowserOS visível, PT-BR, playback validado e janela maximizada antes de responder.
- `references/youtube-channel-latest-video-routing-2026-06-07.md`

- Quando a busca retorna playlist boa mas itens ruins, rejeitar e procurar outra; título promissor não basta.
- Se o player abrir pausado, forçar play e revalidar `paused === false` antes de responder.
- Se o fullscreen não entrou, acionar `f` e revalidar `document.fullscreenElement === true`.
- As notas detalhadas desta sessão ficam em `references/session-lessons-2026-06-07.md`.

## Resposta padrão

Quando o usuário pedir apenas para tocar uma playlist, responder de forma curta e direta após validar tudo.
