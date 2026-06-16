# BrowserOS YouTube visible playback correction — 2026-06-09

## Trigger

The Senhor corrected a visible YouTube task where the URL was opened but the result was not ready for human viewing:

- Camofox had been used first, but the task required BrowserOS.
- The visible BrowserOS page was not left in PT-BR.
- The video was not left playing.
- The BrowserOS window was not maximized.

## Durable workflow

For user-visible YouTube/video tasks:

1. Use BrowserOS, not Camofox.
2. Open YouTube with PT-BR preference when no other language is requested:
   - URL hint: `hl=pt-BR&persist_hl=1`
   - validate via DOM/title where possible.
3. Focus and maximize the BrowserOS window:
   - `_NET_WM_STATE_MAXIMIZED_HORZ`
   - `_NET_WM_STATE_MAXIMIZED_VERT`
4. Start playback and validate:
   - `video.paused === false`
   - `video.muted === false`
   - `video.volume > 0`
   - `video.currentTime` advances.
5. Only then report completion.

## Practical CDP notes

BrowserOS exposes CDP on its own port in the launch log, commonly `127.0.0.1:9107`. If direct WebSocket connection is rejected with an origin 403, connect with origin suppressed or use a BrowserOS-approved control path. This is a connection technique, not a claim that CDP is broken.

## Expected final confirmation

Short and grounded:

“Corrigido, Senhor. BrowserOS está maximizado, em PT-BR, com o vídeo em play e áudio ligado.”
