"""build.py - builds CSE213_Mock_TF_Paper.pdf and CSE213_Mock_TF_Solutions.pdf into CSE 213/TF Prep/."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.abspath(os.path.join(HERE, "..", ".."))
import pdfkit  # noqa: E402

which = sys.argv[1] if len(sys.argv) > 1 else "both"
if which in ("paper", "both"):
    import paper
    doc, fw = pdfkit.make_doc(os.path.join(OUT, "CSE213_Mock_TF_Paper.pdf"), "CSE 213 Mock Term Final", "Mock Term Final • 210 marks • 3 hours",
                              "CSE 213 • Software Engineering")
    doc.build(paper.story(fw))
    print("paper ok")
if which in ("sol", "both"):
    import solutions
    doc, fw = pdfkit.make_doc(os.path.join(OUT, "CSE213_Mock_TF_Solutions.pdf"), "CSE 213 Mock Term Final - Solutions",
                              "Mock Term Final • Model answers", "CSE 213 • Software Engineering")
    doc.build(solutions.story(fw))
    print("solutions ok")
