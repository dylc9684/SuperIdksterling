#!/usr/bin/env python3
"""
Generate game SFX and background music with ElevenLabs.

Run from Terminal:
  python3 generate_audio_elevenlabs.py

The script asks for your API key at runtime and does not save it.
Generated files are written to assets/audio/.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API_BASE = "https://api.elevenlabs.io/v1"
OUTPUT_DIR = Path(__file__).resolve().parent / "assets" / "audio"
SFX_FORMAT = "mp3_44100_128"
MUSIC_FORMAT = "mp3_44100_128"


SFX_ASSETS = [
    {
        "file": "menu_start.mp3",
        "duration": 1.0,
        "prompt": "Short cheerful arcade menu start confirmation sound, clean and punchy, no voice.",
    },
    {
        "file": "level_start.mp3",
        "duration": 1.2,
        "prompt": "Short upbeat level start jingle for a platformer game, bright and energetic, no voice.",
    },
    {
        "file": "jump.mp3",
        "duration": 0.8,
        "prompt": "Short bouncy cartoon platformer jump sound, playful, clean, no music, no voice.",
    },
    {
        "file": "double_jump.mp3",
        "duration": 0.9,
        "prompt": "Sparkly cat-like double jump sound for an arcade platformer, quick paw whoosh, no voice.",
    },
    {
        "file": "coin.mp3",
        "duration": 0.7,
        "prompt": "Bright shiny coin pickup chime for an arcade platform game, quick sparkle, no voice.",
    },
    {
        "file": "question_block.mp3",
        "duration": 0.8,
        "prompt": "Question block hit sound for a platformer, hollow pop with a tiny magical sparkle, no voice.",
    },
    {
        "file": "block_bump.mp3",
        "duration": 0.6,
        "prompt": "Solid block bump sound, short wooden brick bonk, arcade platformer effect, no voice.",
    },
    {
        "file": "powerup.mp3",
        "duration": 1.4,
        "prompt": "Magical peanut butter powerup pickup, warm rising sparkle, satisfying game sound effect.",
    },
    {
        "file": "stomp.mp3",
        "duration": 0.8,
        "prompt": "Squashy enemy stomp impact for a cartoon platformer, quick rubbery thump, no gore.",
    },
    {
        "file": "enemy_pop.mp3",
        "duration": 0.8,
        "prompt": "Small cartoon enemy pop defeat sound, soft burst and sparkle, no gore, no voice.",
    },
    {
        "file": "toilet_shell.mp3",
        "duration": 0.9,
        "prompt": "Porcelain toilet enemy retracting into shell form, ceramic clack and wobble, game sound effect.",
    },
    {
        "file": "shell_kick.mp3",
        "duration": 0.8,
        "prompt": "Kicking a sliding porcelain shell across the floor, fast ceramic scrape, arcade platformer sound.",
    },
    {
        "file": "bullet_stomp.mp3",
        "duration": 0.75,
        "prompt": "Jumping on a bullet projectile, metallic pop and bounce, cartoon arcade sound, no voice.",
    },
    {
        "file": "bullet_shoot.mp3",
        "duration": 0.8,
        "prompt": "Cartoon bullet projectile launch, quick whoosh and pop, arcade platformer sound, no gun realism.",
    },
    {
        "file": "brick_break.mp3",
        "duration": 1.1,
        "prompt": "Cracked brick block shattering into small pieces, arcade platformer sound effect.",
    },
    {
        "file": "fire_peanut_attack.mp3",
        "duration": 1.0,
        "prompt": "Small fiery peanut butter projectile whoosh, warm flame pop, game attack sound.",
    },
    {
        "file": "cat_claw.mp3",
        "duration": 0.7,
        "prompt": "Quick magical cat claw swipe attack, bright slash and paw sparkle, arcade sound effect.",
    },
    {
        "file": "rainbow_attack.mp3",
        "duration": 1.0,
        "prompt": "Rainbow peanut butter magic projectile, glittery whoosh with colorful sparkle, no voice.",
    },
    {
        "file": "hurt.mp3",
        "duration": 0.9,
        "prompt": "Player takes damage in a goofy arcade platformer, quick comedic hit sound, no voice.",
    },
    {
        "file": "respawn.mp3",
        "duration": 1.2,
        "prompt": "Arcade platformer respawn sound, soft rewind shimmer and pop, no voice.",
    },
    {
        "file": "checkpoint.mp3",
        "duration": 1.1,
        "prompt": "Checkpoint reached sound, bright flag chime and soft sparkle, arcade platformer effect.",
    },
    {
        "file": "flag_clear.mp3",
        "duration": 2.2,
        "prompt": "Level clear fanfare for a bright arcade platformer, short triumphant brass and bells.",
    },
    {
        "file": "boss_intro.mp3",
        "duration": 1.8,
        "prompt": "Boss battle intro sting, dramatic arcade hit with rising tension, no vocals.",
    },
    {
        "file": "boss_warning.mp3",
        "duration": 1.4,
        "prompt": "Boss attack warning alarm sting, tense arcade game cue, short and punchy.",
    },
    {
        "file": "boss_hit.mp3",
        "duration": 0.8,
        "prompt": "Boss takes damage, heavy arcade impact with low thump and sparkle, no voice.",
    },
    {
        "file": "boss_defeat.mp3",
        "duration": 2.4,
        "prompt": "Boss defeated explosion fanfare, arcade impact into triumphant sparkle, no voice.",
    },
    {
        "file": "von_blicky.mp3",
        "duration": 1.0,
        "prompt": "Stylized cartoon boss projectile burst, arcade pop shots, not realistic gunfire, no voice.",
    },
    {
        "file": "driveby.mp3",
        "duration": 1.6,
        "prompt": "Fast cartoon car drive-by pass sound, engine whoosh and tire squeal, arcade game style.",
    },
    {
        "file": "trashcan_throw.mp3",
        "duration": 1.0,
        "prompt": "Metal trashcan thrown through the air, clanky whoosh, cartoon arcade boss attack.",
    },
    {
        "file": "boss_slam.mp3",
        "duration": 1.5,
        "prompt": "Huge cartoon boss ground slam impact with dust and shockwave, no voice.",
    },
    {
        "file": "mayo_throw.mp3",
        "duration": 1.0,
        "prompt": "Mayonnaise squeeze bottles thrown in a cartoon boss fight, plastic whoosh, no voice.",
    },
    {
        "file": "mayo_splat.mp3",
        "duration": 0.9,
        "prompt": "Creamy mayonnaise splat on stone floor, goofy cartoon puddle sound, no voice.",
    },
    {
        "file": "hammer_pull.mp3",
        "duration": 1.0,
        "prompt": "Oversized hammer being pulled back for a boss attack, heavy wood and metal windup.",
    },
    {
        "file": "hammer_smash.mp3",
        "duration": 1.3,
        "prompt": "Oversized hammer smash impact, chunky cartoon metal and stone hit, game sound effect.",
    },
    {
        "file": "shockwave.mp3",
        "duration": 1.1,
        "prompt": "Golden ground shockwave spikes rushing outward, magical arcade impact sound, no voice.",
    },
    {
        "file": "rock_fall.mp3",
        "duration": 1.1,
        "prompt": "Stone rock falling from ceiling, rumbling whoosh, arcade platformer hazard sound.",
    },
    {
        "file": "rock_crash.mp3",
        "duration": 1.0,
        "prompt": "Falling rock crashes into floor and breaks apart, chunky stone impact, no voice.",
    },
    {
        "file": "rescue.mp3",
        "duration": 2.4,
        "prompt": "Final rescue celebration jingle, silly triumphant arcade fanfare with sparkling finish, no vocals.",
    },
]


MUSIC_ASSETS = [
    {
        "file": "level1_meadow_theme.mp3",
        "duration_ms": 20000,
        "prompt": (
            "Loopable instrumental background music for a sunny side-scrolling platformer meadow level. "
            "Upbeat, playful, bouncy drums, plucky synths, warm brass, no vocals."
        ),
    },
    {
        "file": "level2_cave_theme.mp3",
        "duration_ms": 20000,
        "prompt": (
            "Loopable instrumental background music for a cave platformer level. "
            "Mysterious but fun, marimba, soft percussion, glowing crystals, no vocals."
        ),
    },
    {
        "file": "level3_plains_theme.mp3",
        "duration_ms": 20000,
        "prompt": (
            "Loopable instrumental background music for a sunny plains platformer level before a boss fight. "
            "Adventurous, bouncy percussion, bright synth lead, no vocals."
        ),
    },
    {
        "file": "level3_boss_theme.mp3",
        "duration_ms": 20000,
        "prompt": (
            "Loopable instrumental boss battle music for a plains arena platformer fight. "
            "Original ultra-fast industrial breakcore metal energy, distorted synth bass, machine-gun drums, "
            "glitch percussion, aggressive arpeggios, cyber-gothic choir pads, tense drop, no vocals, "
            "loopable, do not copy any existing song, melody, game soundtrack, or artist."
        ),
    },
    {
        "file": "level4_cloud_theme.mp3",
        "duration_ms": 20000,
        "prompt": (
            "Loopable instrumental sky level music for a cloud platformer stage. "
            "Airy, fast, sparkling bells, light drums, heroic melody, no vocals."
        ),
    },
    {
        "file": "level5_castle_theme.mp3",
        "duration_ms": 20000,
        "prompt": (
            "Loopable instrumental castle platformer background music. "
            "Moody stone halls, lava glow, driving drums, gothic organ, no vocals."
        ),
    },
    {
        "file": "level5_castle_boss_theme.mp3",
        "duration_ms": 20000,
        "prompt": (
            "Loopable instrumental final castle boss music for a platformer game. "
            "Original final boss industrial breakcore metal theme, faster and heavier than the previous boss, "
            "distorted gothic organ, harsh synth bass, huge drums, aggressive guitars, glitchy fills, "
            "apocalyptic choir pads, no vocals, loopable, do not copy any existing song, melody, game soundtrack, or artist."
        ),
    },
]

BOSS_MUSIC_FILES = {"level3_boss_theme.mp3", "level5_castle_boss_theme.mp3"}
LEVEL_MUSIC_ASSETS = [asset for asset in MUSIC_ASSETS if asset["file"] not in BOSS_MUSIC_FILES]
BOSS_MUSIC_ASSETS = [asset for asset in MUSIC_ASSETS if asset["file"] in BOSS_MUSIC_FILES]


def post_binary(endpoint: str, api_key: str, payload: dict, output_format: str) -> bytes:
    query = urllib.parse.urlencode({"output_format": output_format})
    url = f"{API_BASE}{endpoint}?{query}"
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ElevenLabs API error {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc


def write_bytes(path: Path, data: bytes, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        print(f"skip  {path.relative_to(Path.cwd())} already exists")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print(f"wrote {path.relative_to(Path.cwd())}")


def generate_sfx(api_key: str, overwrite: bool) -> list[str]:
    print("\nGenerating SFX...")
    failures: list[str] = []
    for asset in SFX_ASSETS:
        target = OUTPUT_DIR / asset["file"]
        if target.exists() and not overwrite:
            print(f"skip  {target.relative_to(Path.cwd())} already exists")
            continue
        payload = {
            "text": asset["prompt"],
            "duration_seconds": asset["duration"],
            "prompt_influence": 0.45,
            "model_id": "eleven_text_to_sound_v2",
        }
        try:
            audio = post_binary("/sound-generation", api_key, payload, SFX_FORMAT)
            write_bytes(target, audio, overwrite=True)
        except RuntimeError as exc:
            failures.append(asset["file"])
            print(f"FAIL {asset['file']}: {exc}", file=sys.stderr)
        time.sleep(0.25)
    return failures


def generate_music(api_key: str, overwrite: bool, assets: list[dict] | None = None, label: str = "background music") -> list[str]:
    print(f"\nGenerating {label}...")
    failures: list[str] = []
    for asset in assets or MUSIC_ASSETS:
        target = OUTPUT_DIR / asset["file"]
        if target.exists() and not overwrite:
            print(f"skip  {target.relative_to(Path.cwd())} already exists")
            continue
        payload = {
            "prompt": asset["prompt"],
            "music_length_ms": asset["duration_ms"],
            "model_id": "music_v1",
            "force_instrumental": True,
        }
        try:
            audio = post_binary("/music/stream", api_key, payload, MUSIC_FORMAT)
            write_bytes(target, audio, overwrite=True)
        except RuntimeError as exc:
            failures.append(asset["file"])
            print(f"FAIL {asset['file']}: {exc}", file=sys.stderr)
        time.sleep(0.25)
    return failures


def yes_no(prompt: str, default: bool) -> bool:
    suffix = "Y/n" if default else "y/N"
    answer = input(f"{prompt} [{suffix}]: ").strip().lower()
    if not answer:
        return default
    return answer in {"y", "yes"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SFX and music for Peanut Butter Stick Quest.")
    parser.add_argument("--sfx-only", action="store_true", help="Generate only sound effects.")
    parser.add_argument("--music-only", action="store_true", help="Generate only background music.")
    parser.add_argument("--level-music-only", action="store_true", help="Generate only non-boss level background music.")
    parser.add_argument("--boss-music-only", action="store_true", help="Generate only boss fight background music.")
    parser.add_argument("--all", action="store_true", help="Generate all SFX and music without asking follow-up questions.")
    parser.add_argument("--only", help="Generate one asset by file stem, for example jump or level1_meadow_theme.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files in assets/audio.")
    args = parser.parse_args()

    mode_count = sum([args.all, args.sfx_only, args.music_only, args.level_music_only, args.boss_music_only])
    if mode_count > 1:
        print("Use --all by itself, or choose exactly one generation mode.", file=sys.stderr)
        return 2

    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        api_key = input("Paste your ElevenLabs API key: ").strip()
    if not api_key:
        print("No API key entered. Nothing generated.")
        return 1

    if args.only:
        wanted = args.only.strip().removesuffix(".mp3")
        sfx_matches = [asset for asset in SFX_ASSETS if Path(asset["file"]).stem == wanted]
        music_matches = [asset for asset in MUSIC_ASSETS if Path(asset["file"]).stem == wanted]
        if not sfx_matches and not music_matches:
            print(f"No asset named {wanted!r}.", file=sys.stderr)
            return 2
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        if sfx_matches:
            print(f"\nGenerating one SFX: {wanted}")
            asset = sfx_matches[0]
            payload = {
                "text": asset["prompt"],
                "duration_seconds": asset["duration"],
                "prompt_influence": 0.45,
                "model_id": "eleven_text_to_sound_v2",
            }
            audio = post_binary("/sound-generation", api_key, payload, SFX_FORMAT)
            write_bytes(OUTPUT_DIR / asset["file"], audio, overwrite=True)
        if music_matches:
            print(f"\nGenerating one music track: {wanted}")
            asset = music_matches[0]
            payload = {
                "prompt": asset["prompt"],
                "music_length_ms": asset["duration_ms"],
                "model_id": "music_v1",
                "force_instrumental": True,
            }
            audio = post_binary("/music/stream", api_key, payload, MUSIC_FORMAT)
            write_bytes(OUTPUT_DIR / asset["file"], audio, overwrite=True)
        print(f"\nDone. Audio folder: {OUTPUT_DIR}")
        return 0

    generate_sfx_now = True
    generate_music_now = True
    music_assets = MUSIC_ASSETS
    music_label = "background music"
    if args.all:
        pass
    elif args.sfx_only:
        generate_music_now = False
    elif args.music_only:
        generate_sfx_now = False
    elif args.level_music_only:
        generate_sfx_now = False
        music_assets = LEVEL_MUSIC_ASSETS
        music_label = "non-boss level music"
    elif args.boss_music_only:
        generate_sfx_now = False
        music_assets = BOSS_MUSIC_ASSETS
        music_label = "boss fight music"
    else:
        print("\nMusic generation can use more ElevenLabs credits than short SFX.")
        generate_sfx_now = yes_no("Generate SFX?", True)
        generate_music_now = yes_no("Generate background music too?", True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    if generate_sfx_now:
        failures.extend(generate_sfx(api_key, args.overwrite))
    if generate_music_now:
        failures.extend(generate_music(api_key, args.overwrite, music_assets, music_label))

    print(f"\nDone. Audio folder: {OUTPUT_DIR}")
    if failures:
        print("\nSome files failed:")
        for name in failures:
            print(f"  - {name}")
        print("You can rerun this command later; existing finished files will be skipped unless you use --overwrite.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
