"""check_slides.py <combined.pdf> — verifies that every slide of every course deck is in the combined slide PDF.
Each deck is located in the combined PDF by the order of its pages; per page the text similarity is computed."""
import os, re, sys
import pymupdf

ROOT = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\CSE 213"
AN, IJ = os.path.join(ROOT, "Anindya Sir"), os.path.join(ROOT, "IJ Mam")
PP = os.path.join(ROOT, "TF Prep", "_build", "pptx_pdf")
DECKS = [  # (label, source pdf, first page in combined pdf (1-based), skipped source pages (1-based))
]


def words(t):
    return set(re.findall(r"[a-z]{3,}", t.lower().replace("ﬁ", "fi").replace("ﬀ", "ff")))


def sim(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def check(combined, plan):
    dst = pymupdf.open(combined)
    bad_total = 0
    for label, path, start, skip in plan:
        src = pymupdf.open(path)
        pages = [p for p in range(1, src.page_count + 1) if p not in skip]
        low = []
        for k, sp in enumerate(pages):
            dp = start + k
            if dp > dst.page_count:
                low.append((sp, dp, "beyond end"))
                continue
            a = words(src[sp - 1].get_text())
            b = words(dst[dp - 1].get_text())
            # ignore running header/footer words
            a -= {"nafis", "tahmid", "lecturer", "buet", "presentation", "prepared", "ayas"}
            b -= {"nafis", "tahmid", "lecturer", "buet", "presentation", "prepared", "ayas"}
            s = sim(a, b)
            if (len(a) >= 6 or len(b) >= 6) and s < 0.55:
                low.append((sp, dp, round(s, 2)))
        end = start + len(pages) - 1
        print(f"{label:38s} src {src.page_count:3d} (skipped {len(skip):2d}) -> pdf p.{start}-{end}  mismatches: {len(low)} {low[:6]}")
        bad_total += len(low)
    return bad_total
