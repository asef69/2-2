"""Checks every numerical answer used in the ART notes.  Run: python -P verify.py  (prints PASS/FAIL)."""
import math
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import answers_asm as A
from mips_sim import CPU, s32
from traces import (b, mult_v1, mult_v2, div_v1, div_v2, f32_bits, bits_f32, custom_fp, custom_decode)

FAILS = []


def check(name, got, want, tol=1e-9):
    ok = (abs(got - want) <= tol * max(1, abs(want))) if isinstance(want, float) else got == want
    print(("PASS " if ok else "FAIL ") + name + f": {got!r}" + ("" if ok else f" (want {want!r})"))
    if not ok:
        FAILS.append(name)


print("===== Ch1 performance")
cyc_A = 10 * 2e9; check("sl20 clock B", 1.2 * cyc_A / 6 / 1e9, 4.0)
cyc_A = 10 * 4e9; check("2023-24 6(a) clock B GHz", 1.2 * cyc_A / 6 / 1e9, 8.0)
check("sl22 / 2011-12 1(c) ratio", (1.2 * 500) / (2.0 * 250), 1.2)
check("sl24 seq1 CPI", (2 * 1 + 1 * 2 + 2 * 3) / 5, 2.0); check("sl24 seq2 CPI", (4 * 1 + 1 * 2 + 1 * 3) / 6, 1.5)
# 2015-16 1(a)
ips = {k: f / c for k, (f, c) in {"P1": (3e9, 1.5), "P2": (2.5e9, 1.0), "P3": (4e9, 2.2)}.items()}
check("2015-16 1(a)(i) best", max(ips, key=ips.get), "P2")
print("   IPS", {k: round(v / 1e9, 4) for k, v in ips.items()})
for k, (f, c) in {"P1": (3e9, 1.5), "P2": (2.5e9, 1.0), "P3": (4e9, 2.2)}.items():
    print(f"   {k}: cycles {10*f:.3e}, instr {10*f/c:.4e}, new clock {f*1.2/0.7/1e9:.4f} GHz")
# 2015-16 1(b)
cyc = 500 * 1 + 50 * 5 + 100 * 5 + 50 * 2; check("2015-16 1(b) cycles", cyc, 1350)
check("2015-16 1(b) time ns", cyc / 4e9 * 1e9, 337.5); check("2015-16 1(b) CPI", round(cyc / 700, 4), 1.9286)
cyc2 = cyc - 50 * 5; check("2015-16 1(b) speedup", round(cyc / cyc2, 4), 1.2273); check("CPI new", round(cyc2 / 650, 4), 1.6923)
# 2015-16 1(c)
def par(p, cpi_a=1, cpi_ls=12):
    ar, ls, br = 2.56e9, 1.28e9, 0.256e9
    if p > 1:
        ar, ls = ar / (0.7 * p), ls / (0.7 * p)
    return (ar * cpi_a + ls * cpi_ls + br * 5) / 2e9
t = {p: par(p) for p in (1, 2, 4)}
print("   2015-16 1(c) times", {p: round(v, 4) for p, v in t.items()}, "speedups", round(t[1] / t[2], 4), round(t[1] / t[4], 4))
check("2015-16 1(c) t1", t[1], 9.6); check("t4", round(t[4], 4), 3.84)
print("   doubled arith CPI", {p: round(par(p, 2), 4) for p in (1, 2, 4)})
cpi_ls = (t[4] * 2e9 - 2.56e9 - 0.256e9 * 5) / 1.28e9; check("2015-16 1(c)(iii) CPI ls", round(cpi_ls, 4), 3.0)
# MIPS rating 2015-16 2(a) / 2013-14 5(d)
check("MIPS A", 4e9 / 1 / 1e6, 4000.0); check("MIPS B", round(4e9 / 1.1 / 1e6, 2), 3636.36)
check("time A", 10e9 * 1 / 4e9, 2.5); check("time B", 8e9 * 1.1 / 4e9, 2.2)
# 2013-14 5(b)
n = {"A": 20, "B": 40, "C": 100, "D": 40}
c1 = 20 * 1 + 40 * 2 + 100 * 3 + 40 * 4; c2 = 200 * 2
check("2013-14 5(b) P1 cycles", c1, 560); check("P2", c2, 400)
print("   times ns", round(c1 / 3, 3), c2 / 2, "ratio", round((c2 / 2) / (c1 / 3), 4))
# 2016-17 5(c)
c = 40 * 1 + 80 * 1 + 90 * 3 + 15 * 2; check("2016-17 5(c) cycles M", c, 420); check("time s", c * 1e6 / 3e9, 0.14)
check("FP cycles needed for 2x", c / 2 - (80 + 270 + 30), -170.0)
c3 = 40 * 1.2 + 80 * 1.2 + 90 * 2.7 + 15 * 1.8; check("2016-17 5(c)(iii) cycles", round(c3, 6), 414.0)
print("   new time", c3 * 1e6 / 3e9, "improvement %", round((420 - c3) / 420 * 100, 3))
# 2014-15 5(b) / 2018-19 7(b)
c = 160 * 2 + 110 * 1 + 10 * 5 + 16 * 2; check("FP/INT/LS/BR cycles M", c, 512)
check("2014-15 time 2GHz", c * 1e6 / 2e9, 0.256); check("2018-19 time 4GHz", c * 1e6 / 4e9, 0.128)
check("FP CPI for 2x", (256 - 192) / 160, 0.4); check("LS remaining for 2x", 256 - (320 + 110 + 32), -206)
c4 = 160 * 1.6 + 110 * 1.15 + 10 * 4 + 16 * 2.3; check("2018-19 7(b)(iv) cycles", round(c4, 6), 459.3)
print("   (iv) time", c4 * 1e6 / 4e9, "reduction %", round((512 - c4) / 512 * 100, 3), "speedup", round(512 / c4, 4))
# 2017-18 5(a)
p1 = 40 * 1.2 + 10 * 2 + 16 * 2.5; p2 = 12 * 1.2 + 13 * 2 + 40 * 2.5
check("2017-18 P1 cycles", p1, 108.0); check("P2 cycles", round(p2, 6), 140.4); check("ratio", round(p2 / p1, 4), 1.3)
check("B cycles for 2x", p1 / 2 - (48 + 40), -34.0)
# 2021-22 8(a)
a, bb, cc = 50000, 120000, 30000
q1 = a * 3 + bb * 3 + cc * 2; q2 = a * 2 + bb * 4 + cc * 1
check("2021-22 P1 cycles", q1, 570000); check("P2 cycles", q2, 610000)
t1, t2 = q1 / 2.7e9, q2 / 3.5e9
print("   times us", round(t1 * 1e6, 3), round(t2 * 1e6, 3), "P2/P1 speed", round(t1 / t2, 4))
check("C cycles for 2x in P2", q2 / 2 - (a * 2 + bb * 4), -275000.0)
# 2022-23 305 6(d)
N = 1.2e6; mix = (0.20, 0.25, 0.40, 0.15)
k1 = sum(N * m * c for m, c in zip(mix, (2, 1, 3, 2))); k2 = sum(N * m * c for m, c in zip(mix, (2, 3, 2, 3)))
check("2022-23 6(d) P1 cycles", round(k1), 2580000); check("P2 cycles", round(k2), 2880000)
t1, t2 = k1 / 2.7e9, k2 / 3.2e9
print("   times ms", round(t1 * 1e3, 4), round(t2 * 1e3, 4), "ratio", round(t1 / t2, 4))
check("Amdahl limit 40%", round(1 / (1 - 0.4), 4), 1.6667)
# 2020-21 12(a)
check("2020-21 12(a) CPI A", round((2 * 3 + 1 * 1 + 4 * 2 + 2 * 4) / 9, 4), 2.5556)
check("CPI B", (3 * 3 + 2 * 1 + 3 * 2 + 2 * 4) / 10, 2.5)
# 2019-20 1(a)
cA = 4 + 4 + 5 + 5 + 2; cB = 5 + 5 + 6 + 6 + 3
check("2019-20 1(a) A ns", cA / 2, 10.0); check("B ns", cB / 2.5, 10.0)
# Amdahl family
check("sl26 4x n", 80 / (25 - 20), 16.0)
check("2011-12 1(d) speedup", round(10 / (5 / 5 + 5), 4), 1.6667)
check("2021-22 5(b) speedup", round(1 / (0.02 + 0.98 / 24), 4), 16.4384); check("limit", 1 / 0.02, 50.0)
check("2012-13 6(a)(i) %", round(10 / 210 * 100, 3), 4.762); check("(ii) INT cut %", 42 / 80 * 100, 52.5)
# SPEC
ex = [236, 375, 208, 133, 337, 105, 340, 2, 379, 119, 195, 86]
ref = [9770, 9650, 8050, 9120, 10490, 9330, 12100, 20720, 22130, 6250, 7020, 6900]
r = [rf / e for rf, e in zip(ref, ex)]
gm = math.exp(sum(map(math.log, r)) / len(r))
print("   2016-17 5(b) ratios", [round(x, 2) for x in r], "GM", round(gm, 2))
ex6 = [None, 527, 586, 109, 470, 275]; ref6 = [9770, 10490, 12100, 20720, 7020, 6900]
prod = math.prod(rf / e for rf, e in zip(ref6[1:], ex6[1:]))
r1 = 28.74 ** 6 / prod; T1 = 9770 / r1
print("   2020-21 11(a) ratio1", round(r1, 3), "T1", round(T1, 2))

print("===== ALU designs (exhaustive 4-bit simulation)")


def run_alu(fX, fY, fC1, fmask, sel_bits, n=4, sub=False):
    def go(sel, A, B):
        c = fC1(sel)
        out = 0
        for i in range(n):
            ai, bi = (A >> i) & 1, (B >> i) & 1
            x, y = fX(sel, ai, bi), fY(sel, ai, bi)
            z = c & fmask(sel)
            out |= (x ^ y ^ z) << i
            if sub:
                c = ((1 - x) & y) | ((1 - x) & z) | (y & z)
            else:
                c = (x & y) | (x & z) | (y & z)
        return out
    return go


def test_alu(name, go, spec, n=4):
    ok = True
    for sel, fn in spec.items():
        for A_ in range(16):
            for B_ in range(16):
                if go(sel, A_, B_) != fn(A_, B_) & 15:
                    ok = False
    check(name, ok, True)


NOT = lambda v: 1 - v
S = lambda sel, k: (sel >> k) & 1
# 2023-24 5(b): S2 S1 S0
go = run_alu(lambda s, a, bb: a | (S(s, 2) & NOT(S(s, 1)) & bb),
             lambda s, a, bb: S(s, 1) | (NOT(S(s, 2)) & NOT(bb ^ S(s, 0))),
             lambda s: NOT(S(s, 2)) & (S(s, 1) ^ S(s, 0)), lambda s: NOT(S(s, 2)), 3)
spec = {0: lambda A, B: A - B - 1, 1: lambda A, B: A + B + 1, 2: lambda A, B: A, 3: lambda A, B: A - 1,
        4: lambda A, B: A | B, 5: lambda A, B: A | B, 6: lambda A, B: ~A, 7: lambda A, B: ~A}
test_alu("2023-24 5(b)", go, spec)
# 2022-23 11(d)
go = run_alu(lambda s, a, bb: (a ^ (NOT(S(s, 2)) & NOT(S(s, 1)))) | (S(s, 2) & NOT(S(s, 1)) & NOT(bb)),
             lambda s, a, bb: NOT(bb ^ (S(s, 1) ^ (NOT(S(s, 2)) & S(s, 0)))),
             lambda s: NOT(S(s, 2)) & S(s, 1) & S(s, 0), lambda s: NOT(S(s, 2)), 3)
spec = {0: lambda A, B: -A - B - 2, 1: lambda A, B: B + (~A), 2: lambda A, B: A + B, 3: lambda A, B: A - B,
        4: lambda A, B: A & B, 5: lambda A, B: A & B, 6: lambda A, B: A ^ B, 7: lambda A, B: A ^ B}
test_alu("2022-23 11(d)", go, spec)
# 2022-23 305 5(b) parallel subtractors  F = X - Y - Bin
go = run_alu(lambda s, a, bb: (a ^ (NOT(S(s, 2)) & S(s, 1))) | (S(s, 2) & S(s, 1) & NOT(bb)),
             lambda s, a, bb: bb ^ (S(s, 0) | (S(s, 2) & S(s, 1))),
             lambda s: NOT(S(s, 2)) & (S(s, 1) ^ S(s, 0)), lambda s: NOT(S(s, 2)), 3, sub=True)
spec = {0: lambda A, B: A - B, 1: lambda A, B: A + B, 2: lambda A, B: -A - B - 2, 3: lambda A, B: B - A,
        4: lambda A, B: A ^ B, 6: lambda A, B: A & B}
test_alu("2022-23 CSE305 5(b) subtractors", go, spec)
# 2020-21 10(b): S3 S2 S1 S0
go = run_alu(lambda s, a, bb: a | (S(s, 3) & S(s, 1) & bb),
             lambda s, a, bb: (NOT(S(s, 2)) & NOT(S(s, 1)) & (S(s, 0) | S(s, 3))) | (NOT(S(s, 2)) & S(s, 1) & bb)
             | (S(s, 2) & NOT(S(s, 1)) & NOT(bb)),
             lambda s: NOT(S(s, 3)) & NOT(S(s, 0)) & (S(s, 1) | S(s, 2)), lambda s: NOT(S(s, 3)), 4)
spec = {0: lambda A, B: A, 1: lambda A, B: A - 1, 2: lambda A, B: A + B + 1, 3: lambda A, B: A + B,
        4: lambda A, B: A - B, 5: lambda A, B: A - B - 1, 6: lambda A, B: A + 1, 7: lambda A, B: A}
for k in (8, 9): spec[k] = lambda A, B: ~A
for k in (10, 11): spec[k] = lambda A, B: A & ~B
for k in (12, 13): spec[k] = lambda A, B: ~(A ^ B)
for k in (14, 15): spec[k] = lambda A, B: A | B
test_alu("2020-21 10(b)", go, spec)
# 2019-20 2(a)
go = run_alu(lambda s, a, bb: (NOT(a) & NOT(S(s, 3) & S(s, 2) & S(s, 1) & bb)) | (S(s, 3) & NOT(S(s, 2)) & NOT(S(s, 1)) & NOT(bb)),
             lambda s, a, bb: (S(s, 1) & bb) | (S(s, 2) & NOT(bb)),
             lambda s: NOT(S(s, 3)) & S(s, 0), lambda s: NOT(S(s, 3)), 4)
spec = {0: lambda A, B: ~A, 1: lambda A, B: ~A + 1, 2: lambda A, B: ~A + B, 3: lambda A, B: ~A + B + 1,
        4: lambda A, B: ~A - B - 1, 5: lambda A, B: ~A - B, 6: lambda A, B: ~A - 1, 7: lambda A, B: ~A}
for k in (8, 9): spec[k] = lambda A, B: ~(A & B)
for k in (10, 11): spec[k] = lambda A, B: ~(A ^ B)
for k in (12, 13): spec[k] = lambda A, B: A ^ B
for k in (14, 15): spec[k] = lambda A, B: A | B
test_alu("2019-20 2(a)", go, spec)
# 2017-18 6(a)
go = run_alu(lambda s, a, bb: a | (S(s, 2) & S(s, 0) & NOT(S(s, 1) ^ bb)),
             lambda s, a, bb: (NOT(S(s, 1)) & NOT(S(s, 0)) & bb) | (S(s, 1) & NOT(S(s, 0))) | (S(s, 0) & NOT(bb) & (S(s, 2) ^ S(s, 1))),
             lambda s: 0, lambda s: NOT(S(s, 2)), 3)
spec = {0: lambda A, B: A + B, 1: lambda A, B: A, 2: lambda A, B: A - 1, 3: lambda A, B: A + (~B),
        4: lambda A, B: A ^ B, 5: lambda A, B: A & B, 6: lambda A, B: ~A, 7: lambda A, B: A | B}
test_alu("2017-18 6(a)", go, spec)
# 2018-19 5(d)
go = run_alu(lambda s, a, bb: a | (S(s, 2) & S(s, 1) & NOT(S(s, 0) ^ bb)),
             lambda s, a, bb: (NOT(S(s, 0)) & (bb ^ S(s, 1))) | (S(s, 2) & NOT(S(s, 1)) & S(s, 0)),
             lambda s: NOT(S(s, 2)) & S(s, 1) & S(s, 0), lambda s: NOT(S(s, 2)), 3)
spec = {0: lambda A, B: A + B, 1: lambda A, B: A, 2: lambda A, B: A + (~B), 3: lambda A, B: A + 1,
        4: lambda A, B: A ^ B, 5: lambda A, B: ~A, 6: lambda A, B: A & B, 7: lambda A, B: A | B}
test_alu("2018-19 5(d)", go, spec)
# Mano Table 9-4 (slides 18-20)
go = run_alu(lambda s, a, bb: a | (S(s, 2) & NOT(S(s, 1)) & NOT(S(s, 0)) & bb) | (S(s, 2) & S(s, 1) & NOT(S(s, 0)) & NOT(bb)),
             lambda s, a, bb: (S(s, 0) & bb) | (S(s, 1) & NOT(bb)),
             lambda s: (s >> 3) & 1, lambda s: NOT(S(s, 2)), 4)
# encode sel as s2 s1 s0 in bits 2..0 and Cin in bit 3
ok = True
for s2 in (0, 1):
    for s1 in (0, 1):
        for s0 in (0, 1):
            for cin in (0, 1):
                if s2 and cin:
                    continue
                sel = (cin << 3) | (s2 << 2) | (s1 << 1) | s0
                want = {(0, 0, 0, 0): lambda A, B: A, (0, 0, 0, 1): lambda A, B: A + 1, (0, 0, 1, 0): lambda A, B: A + B,
                        (0, 0, 1, 1): lambda A, B: A + B + 1, (0, 1, 0, 0): lambda A, B: A - B - 1, (0, 1, 0, 1): lambda A, B: A - B,
                        (0, 1, 1, 0): lambda A, B: A - 1, (0, 1, 1, 1): lambda A, B: A, (1, 0, 0, 0): lambda A, B: A | B,
                        (1, 0, 1, 0): lambda A, B: A ^ B, (1, 1, 0, 0): lambda A, B: A & B, (1, 1, 1, 0): lambda A, B: ~A}[(s2, s1, s0, cin)]
                for A_ in range(16):
                    for B_ in range(16):
                        ok &= go(sel, A_, B_) == want(A_, B_) & 15
check("Mano Table 9-4 equations", ok, True)

print("===== Ch2 encodings")


def R(op, rs, rt, rd, sh, fn):
    return (op << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (sh << 6) | fn


def I(op, rs, rt, imm):
    return (op << 26) | (rs << 21) | (rt << 16) | (imm & 0xFFFF)


check("sl21 add $t0,$s1,$s2", hex(R(0, 17, 18, 8, 0, 32)), "0x2324020")
# MIPS-v22: opcode | rt | rd | rs | shamt | funct ;  I: opcode | rt | rs | imm
v22R = lambda op, rt, rd, rs: (op << 26) | (rt << 21) | (rd << 16) | (rs << 11)
v22I = lambda op, rt, rs, imm: (op << 26) | (rt << 21) | (rs << 16) | imm
for nm, w in [("add", v22R(0, 4, 2, 3)), ("addi", v22I(6, 4, 2, 1)), ("lw", v22I(5, 3, 2, 4))]:
    print(f"   v22 {nm}: {b(w,32)} = {w:#010x}")
for nm, w in [("lw $t0,4($s0)", I(35, 16, 8, 4)), ("lw $t1,8($s0)", I(35, 16, 9, 8)), ("sub $t2,$t0,$t1", R(0, 8, 9, 10, 0, 34)),
              ("sw $t2,12($s0)", I(43, 16, 10, 12))]:
    print(f"   2013-14 6(b) {nm}: {b(w,32)} = {w:#010x}")
# target addressing
check("sl53 bne offset", (80024 - 80016) // 4, 2); check("sl53 j field", 80000 // 4, 20000)
check("2018-19 7(a) beq off", (60020 - 60016) // 4, 1); check("j Exit", 60028 // 4, 15007); check("j Loop", 60000 // 4, 15000)
check("2014-15 6(c) j Exit", 6028 // 4, 1507); check("j Loop", 6000 // 4, 1500)
check("2016-17 6(a) j field", int("00000000000000000011111010", 2) * 4, 1000)
check("2020-21 12(b) bne off", (1008 - 1004) // 4, 1); check("j LX field", 131072 // 4, 32768)
check("0x20014924 bits", hex(int("00100000000000010100100100100100", 2)), "0x20014924")
check("lui/ori halves", (0x2001, 0x4924), (8193, 18724))
pc4 = 0x1FFFF000 + 4; off = (0x20014924 - pc4) // 4
check("2022-23 12(c)(iii) offset", off, 22088); check("fits 16 bits", -32768 <= off <= 32767, True)
check("2021-22 6(b)(ii) words", (0x40000000 - 0x20000004) // 4 > 32767, True)
check("2015-16 5(b) const", hex(int("00010000001111010000100100000000", 2)), "0x103d0900")
print("   0x103D =", 0x103D, " 0x0900 =", 0x0900)
d = 30500 - (5000 + 4); print("   005000/30500 decimal: offset words", d / 4)
dh = 0x30500 - (0x5000 + 4); print("   hex: offset words", dh // 4, "> 32767?", dh // 4 > 32767)
print("   sl50 lhi 61 / ori 2304:", hex((61 << 16) | 2304))
# linking 2022-23 305 5(c)
check("B text start", hex(0x00400000 + 0x150), "0x400150")
check("Y addr", hex(0x10000000 + 0x40), "0x10000040")
check("lw X off", (0x10000000 - 0x10008000) & 0xFFFF, 0x8000); check("sw Y off", hex((0x10000040 - 0x10008000) & 0xFFFF), "0x8040")
check("jal B field", hex(0x00400150 >> 2), "0x100054"); check("jal A field", hex(0x00400000 >> 2), "0x100000")
check("text size", hex(0x150 + 0x350), "0x4a0"); check("data size", hex(0x40 + 0x50), "0x90")

print("===== Ch2 MIPS programs (simulated)")


def model_dowhile():
    a, bb, c, N = 5, 10, 2, 30
    while True:
        if (a << 2) > bb:
            a += 2; bb += a
        else:
            a += c; bb += c
        if not a < N:
            return a, bb


cpu = CPU(A.DOWHILE_2324); cpu.call("main")
check("2023-24 6(b) a,b", (cpu.R("$t0"), cpu.R("$t1")), model_dowhile())
cpu = CPU(A.FRAG1_1920); cpu.call("frag1"); check("2019-20 frag1 sum", cpu.R("$s0"), sum(range(-5, 101)))
for x, y in [(131080, 4), (131079, 4), (0, -131076), (5, -131071)]:
    cpu = CPU(A.FRAG2_1920); cpu.r[16], cpu.r[17] = x, y; cpu.call("frag2")
    check(f"frag2 x={x} y={y}", cpu.R("$s0"), 1 if x > y + 131075 else x)
    cpu = CPU(A.FRAG_2223_305); cpu.r[9], cpu.r[10] = x, y; cpu.call("frag")
    check(f"2022-23 6(c) x={x} y={y}", cpu.R("$t1"), 8 if x > y + 131075 else x)
cpu = CPU(A.FRAG3_1920); base = 0x10010000; cpu.r[18] = base; cpu.sw(base + 4 * 131075, 37); cpu.call("frag3")
check("frag3", cpu.R("$s0"), 42)


def model_test(a, bb, c):
    i = res = 0
    while True:
        if i > bb:
            res += c
        i += 1
        if not i < a:
            return res


for args in [(10, 3, 5), (1, 0, 7), (5, 10, 2), (8, -2, 3)]:
    cpu = CPU(A.TESTFUNC_2021); check(f"testFunc{args}", cpu.call("testFunc", args), model_test(*args))


def fun2223(a, bb):
    if bb == 0:
        return 0
    if bb // 2 == 0:
        return fun2223(a * 4, bb // 8)
    return fun2223(a + a, bb // 4) + a


for args in [(3, 0), (3, 1), (3, 5), (2, 37), (7, 100), (1, 1000)]:
    cpu = CPU(A.FUN_2223); check(f"2022-23 9(c) fun{args}", cpu.call("fun", args), fun2223(*args))


def pw(a, bb, base0):
    if bb == 0:
        return base0
    if bb % 2 == 0:
        return pw(a * a, bb // 2, base0)
    return pw(a * a, bb // 2, base0) * a


for args in [(3, 0), (3, 5), (2, 10), (5, 3)]:
    cpu = CPU(A.POW_1819); check(f"2018-19 8(a) as printed {args}", cpu.call("fun", args), pw(*args, 0))
    cpu = CPU(A.POW_1819.replace("add  $v0, $zero, $zero  # return 0", "addi $v0, $zero, 1    #")); check(f"   base 1 → a^b {args}", cpu.call("fun", args), args[0] ** args[1])


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


for n_ in (0, 1, 2, 7, 12):
    cpu = CPU(A.FIB_2122); check(f"fib({n_})", cpu.call("fib", (n_,)), fib(n_))
src = A.F_NESTED_2223 + "\nfunc:  sll $v0, $a0, 1\n       add $v0, $v0, $a1\n       addi $t0, $zero, 999\n       jr $ra"
cpu = CPU(src); fn = lambda x, y: 2 * x + y
check("2022-23 7(c) f(3,4,5,6)", cpu.call("f", (3, 4, 5, 6)), fn(fn(3, 4), 5 + 6))
for n_ in (-3, 0, 1, 5, 20):
    cpu = CPU(A.SUM_1314); check(f"sum({n_})", cpu.call("sum", (n_,)), (n_ * (n_ + 1) // 2 if n_ > 0 else 0))
    cpu = CPU(A.RECURSESUM_1415); check(f"recurseSum({n_})", cpu.call("recurseSum", (n_,)), (n_ * (n_ + 1) // 2 if n_ > 0 else 0))
for prog, lab in ((A.RSTRCOPY_1516, "rstrcopy"), (A.RSTRCOPY_MIN, "rcopy")):
    cpu = CPU(prog); src_a, dst_a = 0x10010000, 0x10020000
    for k, ch in enumerate(b"BUET CSE\0"):
        cpu.sb(src_a + k, ch)
    for k in range(12):
        cpu.sb(dst_a + k, 0x55)
    cpu.call(lab, (dst_a, src_a))
    check(lab, bytes(cpu.lb(dst_a + k) for k in range(9)), b"BUET CSE\0")
cpu = CPU(A.SORT_1718); arr = [5, -2, 9, 0, 3, 3, -7, 11]; va = 0x10010000
for k, v in enumerate(arr):
    cpu.sw(va + 4 * k, v)
for k, v in enumerate((16, 17, 18, 19)):
    cpu.r[v] = 1000 + k
cpu.call("sort", (va, len(arr)))
check("2017-18 7(a) sort", [cpu.lw(va + 4 * k) for k in range(len(arr))], sorted(arr))
check("   $s0-$s3 restored", [cpu.r[v] for v in (16, 17, 18, 19)], [1000, 1001, 1002, 1003])
for k_ in (-1, 0, 1, 2, 3, 4):
    cpu = CPU(A.SWITCH_1213); tb = 0x10010000; cpu.r[12] = tb
    for i, L in enumerate(("L0", "L1", "L2", "L3")):
        cpu.sw(tb + 4 * i, cpu.labels[L])
    g, h, i_, j_ = 10, 4, 7, 2
    cpu.r[17], cpu.r[18], cpu.r[19], cpu.r[20], cpu.r[21], cpu.r[16] = g, h, i_, j_, k_, -99
    cpu.call("sw1")
    want = {0: i_ + j_, 1: g + h, 2: g - h, 3: i_ - j_}.get(k_, -99)
    check(f"2012-13 switch k={k_}", cpu.R("$s0"), want)

print("===== Ch3 arithmetic")
check("sl5 1000x1001", b(8 * 9, 7), "1001000")
rows, P = mult_v1(0b1000, 0b1011); check("2023-24 7(a) v1 product", b(P, 8), "01011000")
rows2, P2 = mult_v2(0b1000, 0b1011); check("v2 product", b(P2, 8), "01011000")
for r_ in rows2:
    print("   ", r_)
rows, P = mult_v2(0b0110, 0b0110); check("2016-17 8(c) 0110x0110", b(P, 8), "00100100")
check("sl15 -0.75", hex(f32_bits(-0.75)), "0xbf400000"); check("sl16", bits_f32(0xC0A00000), -5.0)
v = bits_f32(0xDF807500); print("   0xDF807500 =", v, "= -(1 + 0x7500/2^23) x 2^64 =", -(1 + 0x7500 / 2 ** 23) * 2 ** 64)
check("DF807500 exact", v, -(1 + 0x7500 / 2 ** 23) * 2 ** 64)
print("   0x7F800005 is NaN:", math.isnan(bits_f32(0x7F800005)))
# custom formats
s, E, F, u = custom_fp(-1.25, 4, 11); check("2018-19 5(b) -1.25", hex(u), "0xba00")
s, E, F, u = custom_fp(0.375, 4, 11); check("0.375", hex(u), "0x2c00")
s, E, F, u = custom_fp(0.75, 4, 11); check("2017-18 0.75", hex(u), "0x3400")
s, E, F, u = custom_fp(1.25, 4, 11); check("1.25", hex(u), "0x3a00")
s, E, F, u = custom_fp(2.0, 4, 11); check("sum 2.0", hex(u), "0x4000")
s, E, F, u = custom_fp(-0b11011 / 4 * 2, 7, 8); check("2019-20 4(a) -110.11 x 2^1", hex(u), "0xc2b0")
check("  decode", custom_decode(0xC2B0, 7, 8), -13.5)
check("2019-20 bias 7 bits", (1 << 6) - 1, 63); check("max exp", 126 - 63, 63); check("min exp", 1 - 63, -62)
check("2019-20 4(a)(iii) smallest denormal", 2.0 ** -8 * 2.0 ** -62, 2.0 ** -70)
check("2022-23 8(b) bias 12 bits", (1 << 11) - 1, 2047)
print("   2022-23 8(b): min normal 2^", 1 - 2047, " max (2-2^-19)x2^", 4094 - 2047, " min denorm 2^", -19 - 2046,
      " digits", round(19 * math.log10(2), 2))
check("2020-21 13(a) bias 7 bits", 63, (1 << 6) - 1)
print("   2020-21 13(a): min normal 2^-62, max (2-2^-24)x2^63 =", (2 - 2 ** -24) * 2 ** 63, " min denorm 2^", -24 - 62)
print("   single min", 2.0 ** -126, "max", (2 - 2 ** -23) * 2.0 ** 127, "denorm", 2.0 ** -149)
print("   double min", 2.0 ** -1022, "max", (2 - 2 ** -52) * 2.0 ** 1023, "denorm", 2.0 ** -1074)
n24 = 2 ** 24
check("2021-22 8(b) n", (float(struct.unpack('>f', struct.pack('>f', n24))[0]) == n24,
                         struct.unpack('>f', struct.pack('>f', n24 + 1))[0] == n24 + 1), (True, False))
check("  all below exact", all(struct.unpack('>f', struct.pack('>f', k))[0] == k for k in range(n24 - 1000, n24 + 1)), True)
# 2022-23 8(c) ordering
pairs = [(1.5, 2.5), (-2.0, 1.0), (-3.0, -1.0), (0.0, 1e-30)]
for f1, f2 in pairs:
    i1, i2 = f32_bits(f1), f32_bits(f2)
    print(f"   f1={f1} f2={f2}: unsigned i1<i2 {i1 < i2}, signed j1<j2 {s32(i1) < s32(i2)}")
# FP additions
check("sl18 0.5-0.4375", 0.5 - 0.4375, 0.0625); check("2016-17 7(b)", -0.25 + 0.625, 0.375)
# overflow table
for O in (0, 1):
    for SA in (0, 1):
        for SB in (0, 1):
            ovf_possible = (O == 0 and SA == SB) or (O == 1 and SA != SB)
            print(f"   O={O} SA={SA} SB={SB}: overflow possible={ovf_possible} (when SR != SA)")
# division
for dvd, dvs, n_ in [(0b101111001111, 0b110101, 6), (0b11001001, 0b1011, 4), (0b11010101, 0b1011, 4)]:
    rows, Q, Rm = div_v1(dvd, dvs, n_)
    check(f"div_v1 {dvd}/{dvs}", (Q, Rm), divmod(dvd, dvs))
print("   2022-23 1(b): 3023 / 53 =", divmod(0b101111001111, 0b110101), " hi half", 0b101111, "< 53:", 0b101111 < 53)
rows, q, rm = div_v2(0b101111001111, 0b110101, 6); check("div_v2 2022-23", (q, rm), divmod(3023, 53))
rows, q, rm = div_v2(0b0111, 0b0010, 4); check("div_v2 textbook 7/2", (q, rm), (3, 1))

print("\n", "ALL PASS" if not FAILS else f"FAILURES: {FAILS}")
