# BrowserOS music playback session notes

Date: 2026-06-07

## What worked

- Use BrowserOS for visible playback; do not let Camofox become the display path for the human.
- Validate the real desktop window with `wmctrl -lG` before trusting any browser result.
- When the player looks paused in the UI, force playback with video JS (`video.play()`) instead of assuming the click worked.
- For YouTube fullscreen, verify `document.fullscreenElement === true` and/or the button label changes to `Sair da tela inteira`.
- For audio, verify the active sink input is unmuted and the stream volume is non-zero before declaring success.

## Selection rules for music

- Prefer current-year results.
- Prefer official videos / official music videos / clipe oficial / vídeo oficial.
- Prefer playlists that are made of original clips, not audio-only or reupload compilations.
- Reject lyric, live, topic, and audio-only results unless the user explicitly requests them.

## Channel-latest-video workflow

When the user asks for the last video from a YouTube channel:

1. Open the channel's `/videos` page.
2. Sort by newest if the UI exposes it, otherwise inspect the grid/list directly.
3. Extract the first real `watch?v=` link that corresponds to an actual video title.
4. Open that watch URL directly in BrowserOS.
5. Force play, verify audio, and optionally fullscreen.

## Examples from this session

- Gospel 2026: a playlist with official videos was found and `CeCe Winans - Goodness of God (Official Video)` was selected as the highest-confidence result.
- Rock Brazilian: search results with `Clipe Oficial` / `Official Video` were preferred; `Pitty - Teto de Vidro (Clipe Oficial)` was used as the better fit.
- Latest channel video: `AI Coding` channel was opened via `/videos`, the first real watch link was extracted, and playback was forced in fullscreen.
