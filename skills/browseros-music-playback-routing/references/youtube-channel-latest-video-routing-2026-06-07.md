# YouTube channel latest-video routing notes

Date: 2026-06-07

## Lessons from this session

- BrowserOS is the correct visible-route browser when the user can see the desktop.
- Camofox is not the visible route for the human.
- When a user says a channel name that is close to another channel name, the channel identity must be verified before playback.
- For a request like "open channel X and play the latest video", the safe flow is:
  1. search the exact channel name or handle;
  2. confirm the channel identity;
  3. open the channel's videos page sorted by newest;
  4. pick the topmost upload;
  5. validate playback and fullscreen.
- For playlists and music videos, prefer official/original uploads over audio-only, lyric, live, topic, or reuploads.
- If the player pauses or the page changes unexpectedly, revalidate before claiming success.

## Practical YouTube checks

- Check `video.paused === false`.
- Check `video.muted === false` and `video.volume > 0`.
- Check `document.fullscreenElement === true` when fullscreen was requested.
- Use the channel's `/videos` page when the user explicitly asks for the latest upload.
- Don't trust a similarly named channel without verifying the page identity.
