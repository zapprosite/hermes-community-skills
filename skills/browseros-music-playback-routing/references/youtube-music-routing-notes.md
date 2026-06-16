# YouTube music/video routing notes

Session-learned patterns for visible playback tasks in BrowserOS.

## What worked

- Use the live system date (`date +%F`) before searching.
- For music/video tasks, search by year + genre + `official video`, `official music video`, `clipe oficial`, `vídeo oficial`, or `playlist oficial`.
- For channel requests, navigate to the channel's `/videos` page and sort by newest (`sort=dd`) or use the visible "Mais recentes" list.
- Validate the target by reading the actual page text and latest entries, not by trusting a channel name that looks similar.
- For visible playback, the BrowserOS window must be the physical desktop window; a CDP tab existing by itself is not enough.

## Pitfalls

- Do not confuse BrowserOS with Camofox for visible playback.
- Do not assume `Play all` is enough; verify the player actually started and that `video.paused === false`.
- Do not stop after opening a good-looking playlist title if its first items are audio-only, live, lyric, or reuploads.
- For fullscreen, verify the player shows the exit-fullscreen state or `document.fullscreenElement === true`.

## Useful selectors / checks

- Playback state: `document.querySelector('video')?.paused`
- Volume state: `document.querySelector('video')?.muted`, `document.querySelector('video')?.volume`
- Fullscreen state: `document.fullscreenElement`
- Latest uploads list: channel page `/videos?view=0&sort=dd&flow=grid`

## Query patterns

- `site:youtube.com <channel> videos newest`
- `<channel> youtube videos latest`
- `<year> <genre> official music video playlist`
- `<genre> <country> <year> clipe oficial`
