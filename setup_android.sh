#!/usr/bin/env bash
# Generates the Android host project and applies NIPO MUSIC's native config.
# Run once from the repository root:  bash tool/setup_android.sh
set -euo pipefail

command -v flutter >/dev/null || { echo "Flutter SDK not found on PATH"; exit 1; }

# `flutter create` must not clobber our sources.
TMP="$(mktemp -d)"
cp pubspec.yaml analysis_options.yaml "$TMP"/
cp -r lib "$TMP"/lib

flutter create --platforms=android --org com.nipo --project-name nipo_music \
  --description "NIPO MUSIC - Music. Discovered differently." .

cp "$TMP"/pubspec.yaml "$TMP"/analysis_options.yaml .
rm -rf lib && cp -r "$TMP"/lib lib
rm -f test/widget_test.dart

# Native config: permissions, media service, AudioServiceActivity
cp android_overlay/AndroidManifest.xml android/app/src/main/AndroidManifest.xml
mkdir -p android/app/src/main/kotlin/com/nipo/nipo_music
cp android_overlay/MainActivity.kt android/app/src/main/kotlin/com/nipo/nipo_music/MainActivity.kt

# flutter_secure_storage needs minSdk 23+
for f in android/app/build.gradle.kts android/app/build.gradle; do
  [ -f "$f" ] && sed -i -E 's/minSdk(Version)? ?=? ?flutter\.minSdkVersion/minSdk = 24/' "$f" || true
done
grep -n "minSdk" android/app/build.gradle* || true

flutter pub get
dart run flutter_launcher_icons
echo "Android project ready. Build with: flutter build apk --release"
