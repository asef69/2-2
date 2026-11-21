"""build.py - builds CSE213_TF_2024-25_Solutions.pdf into CSE 213/TF Prep/."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "mock"))
sys.path.insert(0, HERE)
OUT = os.path.abspath(os.path.join(HERE, "..", ".."))
import pdfkit  # noqa: E402
import answers2425  # noqa: E402

doc, fw = pdfkit.make_doc(os.path.join(OUT, "CSE213_TF_2024-25_Solutions.pdf"), "CSE 213 Term Final 2024-25 - Solutions",
                          "Term Final 2024-25 • Solutions", "CSE 213 • Software Engineering")
doc.build(answers2425.story(fw))
print("ok")
