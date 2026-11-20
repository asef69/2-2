"""split_java.py <bundle.txt> — splits '//// FILE: X.java' sections into java/<bundle-stem>/X.java,
compiles them with javac and runs every class that has a main method."""
import os
import re
import subprocess
import sys

bundle = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
stem = os.path.splitext(os.path.basename(bundle))[0]
outdir = os.path.join(here, "java", stem)
os.makedirs(outdir, exist_ok=True)
text = open(bundle, encoding="utf-8").read()
parts = re.split(r"^//// FILE: (\S+)\s*$", text, flags=re.M)
names = []
for name, body in zip(parts[1::2], parts[2::2]):
    with open(os.path.join(outdir, name), "w", encoding="utf-8") as fh:
        fh.write(body.strip("\n") + "\n")
    names.append(name)
cls = os.path.join(outdir, "out")
r = subprocess.run(["javac", "-encoding", "UTF-8", "-implicit:none", "-sourcepath", "", "-d", cls] + names, cwd=outdir, capture_output=True, text=True)
print(r.stdout, r.stderr)
if r.returncode:
    sys.exit(1)
for n in names:
    if n == "RunTests.java" or ("RunTests.java" not in names) and "static void main" in open(os.path.join(outdir, n), encoding="utf-8").read():
        p = subprocess.run(["java", "-cp", cls, n[:-5]], capture_output=True, text=True, timeout=30)
        print("==", n, "\n" + p.stdout + p.stderr)
