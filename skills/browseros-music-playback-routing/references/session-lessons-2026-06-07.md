# Session lessons — BrowserOS music playback routing

Date: 2026-06-07

## What mattered in this session

- For visible playback, BrowserOS is the only correct route. Camofox is background/scraping only.
- Do not trust a stale or unrelated browser target id as proof of what the human sees.
- After navigation, verify the physical BrowserOS window title with `wmctrl -lG`.
- For music discovery, use the current year and favor titles containing `Official Video`, `Official Music Video`, `Clipe Oficial`, or `Vídeo Oficial`.
- For playlists, prefer collections of official videos from the artist/label; reject audio-only, lyric, live, topic, and reupload results.
- Validate playback directly in the page: `video.paused === false`, `muted === false`, `volume > 0`, and `document.fullscreenElement === true` when fullscreen is requested.
- If the player opens paused, force play with the keyboard (`k`) or `video.play()` before answering.
- If fullscreen is missing, press `f` and re-check before concluding.

## Practical search terms that worked

- `{year} {genre} official video`
- `{year} {genre} clipe oficial`
- `{year} gospel official music video`
- `{year} rock brasileiro clipe oficial`
- `{year} top {genre} playlist official video`

## Notes

This file is session-specific and should stay short. The durable instructions live in `SKILL.md`.
