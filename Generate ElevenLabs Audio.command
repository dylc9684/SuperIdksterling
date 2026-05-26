#!/bin/zsh
set -u

cd "$(dirname "$0")" || exit 1

echo "Peanut Butter Stick Quest ElevenLabs audio generator"
echo "Project: $(pwd)"
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
echo "Generating all sound effects and background music..."
"$PYTHON_BIN" generate_audio_elevenlabs.py --all
status=$?

echo
if [[ $status -eq 0 ]]; then
  echo "Done. Audio files are in assets/audio."
  echo "Reload supermario.html after wiring audio into the game."
else
  echo "Generation finished with at least one failed file. Check the messages above."
  echo "Common causes: no ElevenLabs credits, music API unavailable, network blocked, or a rejected prompt."
  echo "You can run this command again; completed files will be skipped."
fi

echo "Press Return to close this window."
read -r _
exit $status
