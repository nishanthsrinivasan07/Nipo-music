# NIPO MUSIC — *Music. Discovered differently.*

Flutter/Dart Android music app: premium dark UI, licensed streaming, local AI-style recommendations, no ads.

## ⚠️ Honest status — read first
This code was written in a sandbox **without the Flutter SDK or internet access**. It has **never been compiled, run on a device, or tested against the live Jamendo API**. Only these were verified: icon generation, and a static bracket/import check. Expect to fix a few compile errors on first build (version-dependent APIs). Treat every feature below as *implemented, untested*.

| Feature | Status |
|---|---|
| Home with personalised shelves, recently played | Implemented, untested |
| Search songs / artists / albums, search history | Implemented, untested |
| Genre playlists, mood discovery, "Surprise me" | Implemented, untested |
| Liked songs, custom playlists, favourite artists | Implemented, untested |
| Artist & album pages ("Fans also like") | Implemented, untested |
| Full-screen player, seek, shuffle, repeat | Implemented, untested |
| Queue: reorder, remove, play next, add to queue | Implemented, untested |
| Background playback, notification, lock-screen controls | Implemented via `just_audio_background`; **untested on device** |
| Local recommendation engine | Implemented, untested |
| Original icon + animated splash | Icon generated and checked; splash untested |
| Spotify integration | **Not implemented** (see below) |

## Requires third-party accounts / permissions
- **Jamendo client ID (free)** — https://devportal.jamendo.com. Without it the app shows a setup screen and cannot stream. Enter it in *Settings* (stored in Android Keystore-backed secure storage) or build with `--dart-define=JAMENDO_CLIENT_ID=...`. Nothing is hard-coded.
- **Notification permission** (Android 13+) for the media notification / lock-screen controls.
- Jamendo's API is free for non-commercial use; commercial distribution needs a Jamendo licence.

## Music source & quality
- Source: Jamendo (Creative Commons / licensed catalogue, full-length streams). Nothing is scraped or downloaded from Spotify, YouTube or Apple Music.
- Quality setting: Standard (MP3 ~96 kbps), High (MP3, default), Lossless (FLAC *if Jamendo offers it* — unverified).
- Track licence link is shown in the player.

## Spotify (not built — and why)
- The Web API can give catalogue metadata, but streaming is not available through it. Playback via the Android App Remote SDK needs the Spotify app installed, user login, and **Premium** for on-demand playback; free users hear Spotify's own ads, which NIPO MUSIC cannot remove. Spotify also restricted some discovery endpoints (e.g. recommendations, related artists) for newer apps — check current docs.
- Because I could not test OAuth or the SDK, I did not ship a fake integration. The app is fully useful without Spotify.

## Ads
NIPO MUSIC has no ads, no ad SDKs, no sponsored recommendations. Jamendo streams are served without ads by this app; a future third-party provider (e.g. Spotify free tier) could play its own ads — this would be disclosed.

## Recommendation engine (local)
`lib/recommender.dart` + `lib/store.dart`: a tag-affinity profile (likes +3, plays +0.6, listened-through +0.8, skips −0.6, onboarding genres +4, favourite artists boost). Candidates come from Jamendo tag queries; results are re-scored, de-duplicated, penalised if recently played, and limited to 3 per artist. "Similar tracks/artists" = tag overlap. All data stays on the phone.

## Build
Prereqs: Flutter stable SDK, Android SDK, JDK 17.
```bash
bash tool/setup_android.sh          # generates android/, applies manifest + icons, pub get
flutter run --dart-define=JAMENDO_CLIENT_ID=YOUR_ID     # or omit and enter it in Settings
flutter build apk --release --dart-define=JAMENDO_CLIENT_ID=YOUR_ID
# APK: build/app/outputs/flutter-apk/app-release.apk
```
Release builds use Flutter's default debug signing (installable, not Play-Store ready). Add your own keystore for publishing.

## GitHub Actions
`.github/workflows/build-apk.yml` runs the setup script, analyzes, builds the release APK and uploads it as the `nipo-music-apk` artifact. Optional repo secret: `JAMENDO_CLIENT_ID`.

## Layout
`lib/jamendo_api.dart` catalogue client · `player.dart` Media3-backed playback (just_audio) · `store.dart` local data · `recommender.dart` · `ui/` screens · `android_overlay/` native config · `tool/make_icon.py` icon generator.
