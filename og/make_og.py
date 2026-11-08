"""Build og/og.html (1200x627 link-preview card); render with og/render.sh."""
import itertools, pathlib

OBS = [166.5, 132.8, 130.5, 129.5, 128.3, 60.9, 14.3]     # ethyl benzoate 13C, CDCl3
H   = [0.42, 0.62, 0.36, 1.0, 0.94, 0.66, 0.70]
OFF = [7.8, -5.6, 6.4, -7.2, 4.1, -9.3, 6.8]               # a partly trained prediction
PH  = [0.62, 0.80, 0.55, 0.90, 0.70, 0.66, 0.84]
pred = [o + d for o, d in zip(OBS, OFF)]

W, Hh, pl, pr = 452, 300, 18, 18
top, bot, amp, axis = 128, 168, 92, 268
X = lambda ppm: pl + (200 - ppm) / 200 * (W - pl - pr)

os_, ps = sorted(OBS), sorted(pred)
mae = sum(abs(p - o) for p, o in zip(ps, os_)) / 7
best = min(sum(abs(pred[i] - os_[k]) for k, i in enumerate(pm)) for pm in itertools.permutations(range(7))) / 7
assert abs(mae - best) < 1e-9

g = []
for p in range(0, 201, 10):
    x = round(X(p)) + .5
    g.append(f'<line x1="{x}" y1="10" x2="{x}" y2="{axis}" stroke="#D2D5CE" stroke-width="1" opacity=".6"/>')
g.append(f'<line x1="{pl}" y1="{top}.5" x2="{W-pr}" y2="{top}.5" stroke="#5A626C" opacity=".55"/>')
g.append(f'<line x1="{pl}" y1="{bot}.5" x2="{W-pr}" y2="{bot}.5" stroke="#5A626C" opacity=".55"/>')
mid = (top + bot) / 2
for o, p in zip(os_, ps):
    x1, x2 = X(o), X(p)
    g.append(f'<path d="M{x1:.1f},{top} C{x1:.1f},{mid} {x2:.1f},{mid} {x2:.1f},{bot}" fill="none" stroke="#2340C4" stroke-width="1.4" opacity=".6"/>')
for v, h in zip(OBS, H):
    g.append(f'<line x1="{X(v):.1f}" y1="{top}" x2="{X(v):.1f}" y2="{top-amp*h:.1f}" stroke="#14171C" stroke-width="2.2"/>')
for v, h in zip(pred, PH):
    y = bot + amp * h * .9
    g.append(f'<line x1="{X(v):.1f}" y1="{bot}" x2="{X(v):.1f}" y2="{y:.1f}" stroke="#2340C4" stroke-width="2.2"/>')
    g.append(f'<circle cx="{X(v):.1f}" cy="{y:.1f}" r="3.6" fill="#2340C4"/>')
g.append(f'<line x1="{pl}" y1="{axis}.5" x2="{W-pr}" y2="{axis}.5" stroke="#5A626C"/>')
for t in (200, 150, 100, 50, 0):
    x = X(t)
    g.append(f'<line x1="{x:.1f}" y1="{axis}" x2="{x:.1f}" y2="{axis+4}" stroke="#5A626C"/>')
    if t: g.append(f'<text x="{x:.1f}" y="{axis+18}" text-anchor="middle">{t}</text>')
g.append(f'<text x="{W-pr}" y="{axis+18}" text-anchor="end">δ / ppm</text>')
g.append(f'<text x="{pl}" y="22">OBSERVED · UNASSIGNED</text>')
g.append(f'<text x="{pl}" y="{axis-8}">PREDICTED</text>')
svg = f'<svg viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" font-family="JetBrains Mono" font-size="10.5" fill="#5A626C" letter-spacing=".04em">' + "".join(g) + "</svg>"

html = (pathlib.Path(__file__).with_name("og.template.html").read_text()
        .replace("{{SVG}}", svg).replace("{{MAE}}", f"{mae:.2f}").replace("{{BEST}}", f"{best:.2f}"))
pathlib.Path(__file__).with_name("og.html").write_text(html)
print(f"MAE {mae:.2f} = brute force {best:.2f}")
