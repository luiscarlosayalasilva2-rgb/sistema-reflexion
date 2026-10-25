"""Hook prompt (Anexo A template) from hooks/capN/tomas.json. Every action and every dialogue line names the speaker
WITH a short visual identifier, so the video model never swaps who says what. Output: hooks/capN/prompt_hook.txt
(one line, no double quotes inside dialogue, ready for Flow)."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
refs = json.loads((Path(__file__).parent / "refs.json").read_text(encoding="utf-8"))
spec = json.loads((ROOT / "hooks" / f"cap{n}" / "tomas.json").read_text(encoding="utf-8"))
P = spec["personajes"]  # {"ZOILO": {"tag": "ZOILO", "corto": "the stocky bearded man in the black polo shirt"}, ...}
times = ["0-2.2 s", "2.2-4.4 s", "4.4-6.8 s", "6.8-10 s"]
who = lambda name: f"{name} ({P[name]['corto']})"
chars = " ".join(f"- {name}: {refs['chars'][p['tag']][p.get('var', 'scene')]}." for name, p in P.items())
lines = []
for t, m, d in zip(times, spec["momentos"], spec["dialogos"]):
    action = m
    for name in P:
        action = action.replace("{" + name + "}", who(name))
    lines.append(f"{t}: {action}: {who(d['quien'])} says, in Spanish: '{d['texto']}'")
txt = (
    "IMPORTANT: The reference image is a 4-panel STORYBOARD that only shows the order of events AND defines the exact character designs and art style. "
    "Do NOT show panels, borders, grids, split screens, captions or any text. Generate ONE single continuous video, full frame, 9:16, with no hard cuts, as one fluid take inside the same room. "
    "ART STYLE (keep it 100% consistent in every frame): 2D hand-drawn classic American superhero comic book style, flat 2D animation, NOT 3D, NOT realistic, NOT photographic. "
    "Bold black ink outlines with varied line weight, dynamic cross-hatching for shadows, cel-shaded flat colors, vivid saturated palette, Ben-Day halftone dot textures, "
    "dramatic comic lighting with strong highlights and deep shadows, expressive exaggerated facial expressions. Animated like a high-quality 2D comic motion cartoon, matching exactly the drawing style of the reference image. "
    f"SETTING: {spec['setting']}, in the same comic style. "
    "CHARACTERS: use the EXACT character designs from the reference image. Same faces, same proportions, same hair, same clothing, same colors in every single frame. "
    f"Do not redesign, age, restyle or swap any character. {chars} "
    "Each line of dialogue is spoken ONLY by the character named for it, recognizable by the description in parentheses; never give a line to the other character. "
    "ACTION AND DIALOGUE (Spanish, strong Mexican telenovela accent, natural lip-sync): PACING IS CRITICAL: the dialogue moves FAST, line after line with almost no gap, "
    "and ALL lines must finish completely before second 10. " + " ".join(lines) + " "
    f"CAMERA: Continuous fluid movement with no cuts, {spec['camara']}, ending with a slow pull-back for a dramatic final frame. "
    f"AUDIO: Emotional dialogue in Spanish with a strong Mexican accent, tense dramatic telenovela music, {spec['ambiente']}. "
    "NEGATIVE: no 3D, no CGI, no realistic or photographic look, no anime style, no style changes mid-video, no changes to faces, hair or outfits, no extra characters, "
    "no comic panels, no frame borders, no grid layout, no split screen, no speech bubbles, no subtitles, no on-screen text."
)
assert '"' not in txt, "comillas dobles: Flow las rechaza"
(ROOT / "hooks" / f"cap{n}" / "prompt_hook.txt").write_text(txt, encoding="utf-8")
print(f"prompt_hook.txt cap{n}: {len(txt)} caracteres")
print("\n".join(lines))
