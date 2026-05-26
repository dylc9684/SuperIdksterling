#!/bin/zsh
set -u

cd "$(dirname "$0")" || exit 1

echo "Peanut Butter Stick Quest level music generator"
echo "Project: $(pwd)"
echo
echo "This generates only the five non-boss background music tracks:"
echo "  assets/audio/level1_meadow_theme.mp3"
echo "  assets/audio/level2_cave_theme.mp3"
echo "  assets/audio/level3_plains_theme.mp3"
echo "  assets/audio/level4_cloud_theme.mp3"
echo "  assets/audio/level5_castle_theme.mp3"
echo
echo "Drop your own boss fight MP3 files here when ready:"
echo "  assets/audio/level3_boss_theme.mp3"
echo "  assets/audio/level5_castle_boss_theme.mp3"
echo
echo "Paste a NEW ElevenLabs API key below. The key will only be used for this run."
echo "It will not be written into supermario.html or saved anywhere."
printf "API key: "
read -r ELEVENLABS_API_KEY
export ELEVENLABS_API_KEY

if [[ -z "$ELEVENLABS_API_KEY" ]]; then
  echo
  echo "No key entered. Stopping."
  echo "Press Return to close this window."
  read -r _
  exit 1
fi

PYTHON_BIN="python3"
if [[ -x "/Users/dylancheng/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" ]]; then
  PYTHON_BIN="/Users/dylancheng/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
fi

echo
echo "Generating non-boss level music only..."
"$PYTHON_BIN" generate_audio_elevenlabs.py --level-music-only
status=$?

echo
if [[ $status -eq 0 ]]; then
  echo "Done. Level music files are in assets/audio."
  echo "Reload supermario.html after the files finish generating."
else
  echo "Generation finished with at least one failed file. Check the messages above."
  echo "Common causes: no ElevenLabs credits, music API unavailable, network blocked, or a rejected prompt."
  echo "You can run this command again; completed files will be skipped."
fi

echo "Press Return to close this window."
read -r _
exit $status
