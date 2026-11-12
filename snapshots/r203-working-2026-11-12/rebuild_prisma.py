"""Draw a single consolidated, fully numbered PRISMA diagram for final author review."""

from hashlib import sha256
import json
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
data_path = HERE / "aggregate_counts.json"
data = json.loads(data_path.read_text())
assert data["included_reports"] == 340 and data["awaiting_classification_at_cutoff_reports"] == 40
assert data["reported_randomized_strategy_groups_conservative"] == 194
assert data["principal_result_reports"] == 199 and data["companion_reports"] == 141
assert data["split_one_suspected_dependency_pair_groups"] == 195 and data["split_both_Yun_and_Khoshnab_pairs_groups"] == 196
assert data["not_retrieved_fixed"] == 499
assert data["reports_assessed"] == data["total_reports_not_included_with_source_reasons"] + 40 + 340
out = HERE / "figures/Figure_1_PRISMA.pdf"
out.parent.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(out), pagesize=(595, 950))
c.setTitle("Figure 1 Study selection")
c.setAuthor("Linwen Qiu, Kaiting Wen, Chuan Yin")
c.setSubject("Current evidence-flow under adopted source-use/counting rules after actual R201 source receipts; no whole-manuscript approval or unique-person total certificate")
ink = HexColor("#18303d")
line = HexColor("#4f626e")


def box(x, y, w, h, title, lines, fill="#ffffff", size=9.4):
    c.setFillColor(HexColor(fill))
    c.setStrokeColor(line)
    c.setLineWidth(0.8)
    c.rect(x, y, w, h, stroke=1, fill=1)
    cursor = y + h - 16
    c.setFillColor(ink)
    for text, bold in [(title, True)] + [(text, False) for text in lines]:
        font = "Helvetica-Bold" if bold else "Helvetica"
        font_size = size + 0.5 if bold else size
        c.setFont(font, font_size)
        for fragment in simpleSplit(text, font, font_size, w - 20):
            assert cursor >= y + 8, (title, text, cursor, y)
            c.drawString(x + 10, cursor, fragment)
            cursor -= font_size + 3


def arrow(points):
    c.setStrokeColor(line)
    c.setLineWidth(0.8)
    for start, end in zip(points, points[1:]):
        c.line(*start, *end)
    x0, y0 = points[-2]
    x1, y1 = points[-1]
    c.setFillColor(line)
    p = c.beginPath()
    p.moveTo(x1, y1)
    if x1 == x0:
        p.lineTo(x1 - 3, y1 + 5)
        p.lineTo(x1 + 3, y1 + 5)
    else:
        p.lineTo(x1 - 5, y1 - 3)
        p.lineTo(x1 - 5, y1 + 3)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def label(text, y, h):
    c.setFillColor(HexColor("#edf2f5"))
    c.rect(12, y, 25, h, fill=1, stroke=0)
    c.saveState()
    c.translate(28, y + h / 2)
    c.rotate(90)
    c.setFillColor(ink)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(0, 0, text)
    c.restoreState()


c.setFillColor(ink)
c.setFont("Helvetica-Bold", 13)
c.drawString(55, 928, "Figure 1 Study selection")
label("Identification", 670, 240)
label("Screening and eligibility", 360, 285)
label("Included", 140, 205)
sources = [
    "Databases (n = 17,574)", "PubMed / MEDLINE, 2,262", "Embase.com bibliographic records, 6,433",
    "Web of Science Core Collection, 4,420", "Cochrane CENTRAL, 2,194", "LILACS, 727",
    "CINAHL Complete (EBSCOhost), 922", "APA PsycInfo (EBSCOhost), 484", "SPORTDiscus (EBSCOhost), 132",
    "Trial registers (n = 10,937)", "Embase Registry, 683", "ClinicalTrials.gov, 8,639", "WHO ICTRP, 1,615",
    "Other identified sources (n = 980)"
]
box(55, 670, 300, 240, "Records identified (n = 29,491)", sources, fill="#f6f9fb", size=9.4)
box(380, 746, 195, 68, "Records removed", ["Duplicate representations", "(n = 7,566)"], size=9.5)
arrow([(355, 780), (380, 780)])
box(55, 580, 300, 48, "Records screened (n = 21,925)", [], size=10.5)
arrow([(205, 670), (205, 628)])
box(380, 578, 195, 50, "Records excluded", ["(n = 18,827)"], size=10)
arrow([(355, 603), (380, 603)])
box(55, 490, 300, 60, "Reports sought for retrieval (n = 3,088)", ["Linked from 3,098 candidate records*"], size=9.8)
arrow([(205, 580), (205, 550)])
box(380, 495, 195, 50, "Reports not retrieved", ["(n = 499)"], size=10)
arrow([(355, 520), (380, 520)])
box(55, 400, 300, 48, "Reports assessed for eligibility", ["(n = 2,589)"], size=10)
arrow([(205, 490), (205, 448)])
reasons = data["exclusion_reasons_existing"]
excluded_lines = [
    f"Outside active-practice scope, {reasons['INTERVENTION_OR_COMPARISON_OUTSIDE_FOCUSED_ACTIVE_PRACTICE_SCOPE']}",
    f"No eligible direct sexual result, {reasons['NO_EXTRACTABLE_DIRECT_SEXUAL_RESULT_IN_CURRENT_OWN_SOURCE']}",
    f"Ineligible or mixed design, {reasons['NONRANDOMIZED_MIXED_OR_QUALITATIVE_DESIGN']}",
    f"Not an original result report, {reasons['NOT_AN_ORIGINAL_PRIMARY_RANDOMIZED_RESULT_REPORT']}",
    f"Nonseparable population, {reasons['INELIGIBLE_OR_NONSEPARABLE_POPULATION']}",
    f"Retracted report, {reasons['RETRACTED_REPORT']}",
    "Protocols and other noncontributing report contexts, 1,701"
]
box(380, 270, 195, 210, "Reports not included (n = 2,209)", excluded_lines, size=9.0)
arrow([(355, 424), (380, 424)])
box(380, 195, 195, 58, "Reports awaiting classification", ["at the evidence cutoff (n = 40)"], fill="#faf8f2", size=9.3)
arrow([(205, 370), (365, 370), (365, 224), (380, 224)])
box(55, 250, 300, 95, "Studies included in the review", [
    "Conservative trial groups (K = 194)", "Reports of included studies (n = 340)",
    "199 principal result reports; 141 companion reports"], fill="#f0f5f7", size=9.6)
arrow([(205, 400), (205, 345)])
box(55, 140, 300, 72, "Restricted quantitative analyses", ["Trial families contributing (n = 6)", "Three comparisons, K = 2 each",
    "Includes exploratory and post-hoc analyses"], size=9.4)
arrow([(205, 250), (205, 212)])
notes = [
    "* Record-to-report reconciliation: 3,098 - 1 proceedings container + 4 additional reports - 13 redundant representations (10 alias nodes and 3 many-to-one merges) = 3,088. Details appear in S1.",
    "The included count covers complete bodily-practice programmes and defined adaptive physical-task offers. It does not identify an isolated exercise component effect.",
    "Two suspected-dependency pairs (Yun 80/150 and Khoshnab 120/60) are grouped conservatively. Splitting one or both gives 195 or 196 groups; person-level overlap is unverified. Uncertain eligibility remains in the awaiting-classification branch.",
    "Adapted from PRISMA 2020. Individual source scopes and report-level reasons are provided in S1 and S2."
]
y = 112
c.setFont("Helvetica", 8.2)
c.setFillColor(ink)
for note in notes:
    for line_text in simpleSplit(note, "Helvetica", 8.2, 520):
        c.drawString(55, y, line_text)
        y -= 10
    y -= 3
assert y > 12
c.showPage()
c.save()
result = {"file": str(out), "sha256": sha256(out.read_bytes()).hexdigest(), "page_count": 1,
    "source_counts": {"path": str(data_path), "sha256": sha256(data_path.read_bytes()).hexdigest()},
    "R195_count_policy_actually_adopted": True, "scientific_fact_gaps_remain": True, "contains_unknown_number_placeholders": False}
(HERE / "PRISMA_BUILD.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
