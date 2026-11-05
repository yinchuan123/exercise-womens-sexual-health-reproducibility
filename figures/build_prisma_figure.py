"""Build the PRISMA 2020 diagram from the frozen, shareable aggregate JSON."""
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
import json
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

here = Path(__file__).resolve().parent
parser = ArgumentParser(description=__doc__)
parser.add_argument("--data", type=Path, default=here / "PRISMA_2020_FIGURE1_DATA.json")
parser.add_argument("--output", type=Path, default=here)
args = parser.parse_args()
data = json.loads(args.data.read_text())
c = data["counts"]
unknown = data["unresolved_whole_review_fields"]
assert len(unknown) == 8 and all(cell["value"] is None for cell in unknown.values())
assert c["database_members"] + c["register_members"] == c["focused_export_members"]
assert c["focused_export_members"] - c["focused_duplicates"] == c["focused_unique"]
assert c["archive_members"] - c["archive_duplicates"] - c["archive_focused_overlap"] == c["archive_net"]
assert c["focused_unique"] + c["archive_net"] == c["screening_frame"]
assert sum(c["record_routes"].values()) == c["screening_frame"]
assert c["awaiting_catalogue_reports"] == 114

matplotlib.rcParams.update({
    "font.family": "DejaVu Sans",
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
    "svg.hashsalt": "prisma-2020-figure-1",
})
width, height = 175, 208
fig = plt.figure(figsize=(width / 25.4, height / 25.4), facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, width)
ax.set_ylim(height, 0)
ax.axis("off")

ink, muted, border = "#142735", "#384955", "#617583"
pale, cold, dotted = "#EDF2F5", "#F6F8F9", "#778692"
objects = []


def text(x, y, message, *, size=8.5, bold=False, align="left", color=ink, rotation=0,
         bounds=None):
    t = ax.text(
        x, y, message, ha=align, va="center", color=color, fontsize=size,
        fontweight="bold" if bold else "normal", rotation=rotation,
    )
    if bounds is not None:
        objects.append((t, bounds))


def box(x, y, w, h, lines, *, style="solid", fill="white", head=True, centered=False):
    linestyle = "-" if style == "solid" else (0, (3, 2))
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill,
                           edgecolor=border if style == "solid" else dotted,
                           linewidth=0.75, linestyle=linestyle, zorder=2))
    center = x + w / 2 if centered else x + 3.5
    spacing = 3.65
    start = y + (h - (len(lines)-1)*spacing) / 2
    for i, line in enumerate(lines):
        text(center, start + i * spacing, line, bold=head and i == 0,
             align="center" if centered else "left",
             bounds=(x+1.5, y+0.8, x+w-1.5, y+h-0.8))


def arrow(x0, y0, x1, y1, *, dashed=False):
    ax.add_patch(FancyArrowPatch(
        (x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=7,
        shrinkA=0, shrinkB=0, color=dotted if dashed else border,
        linestyle=(0, (3, 2)) if dashed else "-", linewidth=0.8, zorder=1,
    ))


def connector(xs, ys):
    ax.plot(xs, ys, color=border, linewidth=0.75, zorder=1)


def stage(y, h, label):
    ax.add_patch(Rectangle((4, y), 17, h, facecolor=pale, edgecolor="none"))
    text(12.5, y+h/2, label, size=9.3, bold=True, align="center", rotation=90,
         bounds=(4, y, 21, y+h))


def n(value):
    return f"{value:,}"


left_x, left_w = 26, 70
right_x, right_w = 104, 67
left_mid, right_mid = left_x+left_w/2, right_x+right_w/2
stage(5, 76, "Identification")
stage(87, 83, "Screening")
stage(176, 20, "Included")

# Separate identification channels from the official new-review template.
box(left_x, 5, left_w, 12, ["Databases and registers"], fill=pale, centered=True)
box(right_x, 5, right_w, 12, ["Targeted records from earlier archive"], fill=pale, centered=True)
box(left_x, 20, left_w, 17, [
    f"Records identified (n = {n(c['focused_export_members'])})",
    f"Databases (n = {n(c['database_members'])})",
    f"Registers (n = {n(c['register_members'])})",
])
box(right_x, 20, right_w, 17, [
    "Record representations identified",
    f"(n = {n(c['archive_members'])})",
])
box(left_x, 42, left_w, 18, [
    "Duplicates removed",
    f"Duplicate representations (n = {n(c['focused_duplicates'])})",
])
box(right_x, 42, right_w, 18, [
    "Duplicates removed",
    f"Duplicates within archive (n = {n(c['archive_duplicates'])})",
    f"Overlap with focused records (n = {n(c['archive_focused_overlap'])})",
])
box(left_x, 65, left_w, 16, [
    "Unique focused record groups",
    f"(n = {n(c['focused_unique'])})",
])
box(right_x, 65, right_w, 16, [
    "Additional archival record groups",
    f"(n = {n(c['archive_net'])})",
])
for x in (left_mid, right_mid):
    for a, b in ((37, 42), (60, 65)):
        arrow(x, a, x, b)
arrow(left_mid, 81, left_mid, 87)
connector([right_mid, right_mid, left_mid+8], [81, 84, 84])
arrow(left_mid+8, 84, left_mid+8, 87)

# Verified record routing is separated from the uncertain report sequence.
box(left_x, 87, left_w, 18, [
    "Record groups in screening frame",
    f"(n = {n(c['screening_frame'])})",
])
routes = c["record_routes"]
box(right_x, 87, right_w, 31, [
    "Documented record dispositions",
    f"Exclusion route (n = {n(routes['excluded'])})",
    f"Author-adopted retention (n = {n(routes['author_retained'])})",
    f"Technical retention (n = {n(routes['technical_retained'])})",
    f"On hold at record level (n = {n(routes['hold'])})",
], fill=cold)
arrow(left_x+left_w, 96, right_x, 96)
box(right_x, 122, right_w, 10, [
    "Sequential record exclusions", "(n = unknown)",
], style="dashed", head=False)

box(left_x, 134, left_w, 12, [
    "Reports sought for retrieval (n = unknown)",
], style="dashed", head=False)
box(right_x, 134, right_w, 12, [
    "Reports not retrieved (n = unknown)",
], style="dashed", head=False)
box(left_x, 154, left_w, 16, [
    "Reports assessed for eligibility",
    "(n = unknown)",
], style="dashed")
box(right_x, 154, right_w, 16, [
    "Reports excluded, with reasons",
    "(n = unknown)",
], style="dashed")
box(left_x, 176, left_w, 20, [
    "Included studies (K = unknown)",
    "Reports of included studies (n = unknown)",
    "Unique participants (N = unknown)",
], style="dashed")
arrow(left_mid, 105, left_mid, 134, dashed=True)
arrow(left_mid, 127, right_x, 127, dashed=True)
arrow(left_x+left_w, 140, right_x, 140, dashed=True)
arrow(left_mid, 146, left_mid, 154, dashed=True)
arrow(left_x+left_w, 162, right_x, 162, dashed=True)
arrow(left_mid, 170, left_mid, 176, dashed=True)
box(right_x, 176, right_w, 20, [
    "Separate report catalogue evidence",
    f"Synthesis: {n(c['principal_reports'])} reports, {n(c['study_families'])} study families",
    f"Awaiting classification: {n(c['awaiting_catalogue_reports'])} reports",
], fill=cold)
text(4, 202.3, "Dashed boxes and arrows mark whole-review stages whose counts remain unknown.",
     size=8.3, color=muted, bounds=(3, 199.5, 172, 206))

# Detect actual glyph-box collisions in the printed dimensions before export.
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
to_data = ax.transData.inverted()
for label, (xmin, ymin, xmax, ymax) in objects:
    e = label.get_window_extent(renderer).transformed(to_data)
    if e.xmin < xmin or e.xmax > xmax or e.ymin < ymin or e.ymax > ymax:
        raise ValueError(f"Text exceeds box: {label.get_text()!r}: {e.extents}")

args.output.mkdir(parents=True, exist_ok=True)
stem = args.output / "Figure_1_PRISMA_2020"
fig.savefig(stem.with_suffix(".pdf"), metadata={
    "Title": "PRISMA 2020 study selection flow for the exercise-focused synthesis",
    "Subject": "Verified archive counts with unresolved whole-review stages",
    "CreationDate": datetime(2026, 11, 5, tzinfo=timezone.utc),
    "ModDate": datetime(2026, 11, 5, tzinfo=timezone.utc),
})
fig.savefig(stem.with_suffix(".svg"), metadata={"Date": None})
fig.savefig(stem.with_suffix(".png"), dpi=220)
