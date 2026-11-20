"""All grammars of the CFG note, verified against their language definitions (cfg_tools.CFG)."""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg_tools import CFG, verify, ambiguous_witness


def blocks(w, pat):
    return re.fullmatch(pat, w) is not None


def cnt(w, c):
    return w.count(c)


G, PR = {}, {}
G["am_bn"] = (CFG({"S": ["aSb", "aAb"], "A": ["aA", "a"]}, "S"), "ab",
              lambda w: (m := re.fullmatch(r"(a*)(b+)", w)) is not None and len(m.group(1)) > len(m.group(2)))
G["pal"] = (CFG({"P": ["0P0", "1P1", "0", "1", ""]}, "P"), "01", lambda w: w == w[::-1])
G["pal_even_01a"] = (CFG({"P": ["0P0", "1P1", "aPa", ""]}, "P"), "01a", lambda w: w == w[::-1] and len(w) % 2 == 0)
G["0s1any"] = (CFG({"S": ["A1B"], "A": ["0A", ""], "B": ["0B", "1B", ""]}, "S"), "01", lambda w: blocks(w, r"0*1[01]*"))
G["eq_ab"] = (CFG({"S": ["aSbS", "bSaS", ""]}, "S"), "ab", lambda w: cnt(w, "a") == cnt(w, "b"))
G["eq_01"] = (CFG({"S": ["0S1S", "1S0S", ""]}, "S"), "01", lambda w: cnt(w, "0") == cnt(w, "1"))
G["0n1m0m1n"] = (CFG({"S": ["0S1", "T"], "T": ["1T0", ""]}, "S"), "01",
                 lambda w: any(w == "0" * n + "1" * m + "0" * m + "1" * n for n in range(len(w) + 1) for m in range(len(w) + 1)))
G["n_m+k"] = (CFG({"S": ["aSc", "T"], "T": ["aTb", ""]}, "S"), "abc",
              lambda w: (m := re.fullmatch(r"(a*)(b*)(c*)", w)) is not None and len(m.group(1)) == len(m.group(2)) + len(m.group(3)))
G["n_2m+3k"] = (CFG({"S": ["aaaSc", "T"], "T": ["aaTb", ""]}, "S"), "abc",
                lambda w: (m := re.fullmatch(r"(a*)(b*)(c*)", w)) is not None and len(m.group(1)) == 2 * len(m.group(2)) + 3 * len(m.group(3)))
G["n_m_2n"] = (CFG({"S": ["aSb", "aSbb", ""]}, "S"), "ab",
               lambda w: (m := re.fullmatch(r"(a*)(b*)", w)) is not None and len(m.group(1)) <= len(m.group(2)) <= 2 * len(m.group(1)))
G["0n1n_1n0n"] = (CFG({"S": ["A", "B"], "A": ["0A1", ""], "B": ["1B0", ""]}, "S"), "01",
                  lambda w: blocks(w, r"(0*)(1*)") and cnt(w, "0") == cnt(w, "1") or blocks(w, r"1*0*") and cnt(w, "0") == cnt(w, "1"))
G["three1"] = (CFG({"S": ["X1X1X1X"], "X": ["0X", "1X", ""]}, "S"), "01", lambda w: cnt(w, "1") >= 3)
G["two1"] = (CFG({"S": ["X1X1X"], "X": ["0X", "1X", ""]}, "S"), "01", lambda w: cnt(w, "1") >= 2)
G["one0one1"] = (CFG({"S": ["X0X1X", "X1X0X"], "X": ["0X", "1X", ""]}, "S"), "01", lambda w: "0" in w and "1" in w)
G["aibjck"] = (CFG({"S": ["ABC"], "A": ["aA", ""], "B": ["bB", ""], "C": ["cC", ""]}, "S"), "abc", lambda w: blocks(w, r"a*b*c*"))
G["same_ends"] = (CFG({"S": ["0X0", "1X1", "0", "1"], "X": ["0X", "1X", ""]}, "S"), "01", lambda w: len(w) >= 1 and w[0] == w[-1])
G["odd_mid0"] = (CFG({"S": ["0S0", "0S1", "1S0", "1S1", "0"]}, "S"), "01", lambda w: len(w) % 2 == 1 and w[len(w) // 2] == "0")
G["odd"] = (CFG({"S": ["X", "XXS"], "X": ["0", "1"]}, "S"), "01", lambda w: len(w) % 2 == 1)
G["more0"] = (CFG({"A": ["E0E", "E0A"], "E": ["0E1E", "1E0E", ""]}, "A"), "01", lambda w: cnt(w, "0") > cnt(w, "1"))
G["wx"] = (CFG({"S": ["TX"], "T": ["0T0", "1T1", "#U"], "U": ["0U", "1U", ""], "X": ["0X", "1X", ""]}, "S"), "01#",
           lambda w: w.count("#") == 1 and w.split("#")[0][::-1] in w.split("#")[1])
G["pal4"] = (CFG({"S": ["00S00", "01S10", "10S01", "11S11", ""]}, "S"), "01", lambda w: w == w[::-1] and len(w) % 4 == 0)
G["paren"] = (CFG({"S": ["(S)S", ""]}, "S"), "()", lambda w: (lambda d: all(d[i] >= 0 for i in range(len(d))) and (not d or d[-1] == 0))(
    [sum(1 if c == "(" else -1 for c in w[:i + 1]) for i in range(len(w))]))


def ineq(w):
    m = re.fullmatch(r"(a*)(b*)(c*)", w)
    return m is not None and len(m.group(1)) != len(m.group(2)) + len(m.group(3))


G["i_ne_jk"] = (CFG({"S": ["S1", "S2"], "S1": ["aS1c", "A1"], "A1": ["aA1b", "A2"], "A2": ["aA2", "a"],
                     "S2": ["aS2c", "B", "D"], "B": ["bB", "bC", "cC"], "C": ["cC", ""], "D": ["aDb", "E"], "E": ["bE", "b"]}, "S"),
                "abc", ineq)
G["nonpal"] = (CFG({"R": ["XRX", "S"], "S": ["aTb", "bTa"], "T": ["XTX", "X", ""], "X": ["a", "b"]}, "R"), "ab", lambda w: w != w[::-1])
G["abScB"] = (CFG({"S": ["abScB", ""], "B": ["bB", "b"]}, "S"), "abc",
              lambda w: (m := re.fullmatch(r"((?:ab)*)((?:cb+)*)", w)) is not None and len(m.group(1)) // 2 == m.group(2).count("c"))
G["ijk_or"] = (CFG({"S": ["S1", "S2"], "S1": ["AC"], "A": ["aAb", ""], "C": ["cC", ""], "S2": ["DB"], "D": ["aD", ""], "B": ["bBc", ""]}, "S"),
               "abc", lambda w: (m := re.fullmatch(r"(a*)(b*)(c*)", w)) is not None and (len(m.group(1)) == len(m.group(2)) or len(m.group(2)) == len(m.group(3))))
G["i_j_or_i_k_pos"] = (CFG({"S": ["XC", "Y"], "X": ["aXb", "ab"], "C": ["cC", "c"], "Y": ["aYc", "aBc"], "B": ["bB", "b"]}, "S"),
                       "abc", lambda w: (m := re.fullmatch(r"(a+)(b+)(c+)", w)) is not None and (len(m.group(1)) == len(m.group(2)) or len(m.group(1)) == len(m.group(3))))
G["inherent"] = (CFG({"S": ["AB", "C"], "A": ["aAb", "ab"], "B": ["cBd", "cd"], "C": ["aCd", "aDd"], "D": ["bDc", "bc"]}, "S"), "abcd",
                 lambda w: (m := re.fullmatch(r"(a+)(b+)(c+)(d+)", w)) is not None and (
                     (len(m.group(1)) == len(m.group(2)) and len(m.group(3)) == len(m.group(4))) or
                     (len(m.group(1)) == len(m.group(4)) and len(m.group(2)) == len(m.group(3)))))
G["amb_given"] = (CFG({"S": ["AB", "C"], "A": ["aAb", "ab"], "B": ["cB", "c"], "C": ["aCc", "aDc"], "D": ["bD", "b"]}, "S"), "abc", None)
G["sloppy1"] = (CFG({"S": ["aSb", "bSc", "aS", "Sc", ""]}, "S"), "abc", None)
G["sloppy2"] = (CFG({"S0": ["S1", "S3"], "S1": ["aS1bS2c", ""], "S2": ["S2c", ""], "S3": ["aS4bS3c", ""], "S4": ["aS4", ""]}, "S0"), "abc", None)
G["aS_aSbS"] = (CFG({"S": ["aS", "aSbS", ""]}, "S"), "ab", None)
G["0A1B"] = (CFG({"S": ["0A", "1B"], "A": ["0AA", "1S", "1"], "B": ["1BB", "0S", "0"]}, "S"), "01", None)
G["E_amb"] = (CFG({"E": ["E+E", "E*E", "(E)", "a"]}, "E"), "a+*()", None)
G["E_unamb"] = (CFG({"E": ["E+T", "T"], "T": ["T*F", "F"], "F": ["(E)", "a"]}, "E"), "a+*()", None)

if __name__ == "__main__":
    ok = True
    for k, (g, sig, pred) in G.items():
        if pred is not None:
            ok &= verify(k, g, pred, sig, 8 if len(sig) <= 2 else 6)
    ijk = re.compile(r"(a*)(b*)(c*)")
    def inL_ijk(w):
        m = ijk.fullmatch(w); return m is not None and (len(m.group(1)) == len(m.group(2)) or len(m.group(2)) == len(m.group(3)))
    for k in ("sloppy1", "sloppy2"):
        g = G[k][0]
        extra = [w for w in g.gen("abc", 6) if not inL_ijk(w)][:4]
        missing = [w for w in ["abbcc", "aabbc", "bc", "ab", "abc", "c", "a", "aab", "bcc"] if inL_ijk(w) and not g.count(w)]
        print(k, "generates non-members:", extra, " misses:", missing)
    for k in ("amb_given", "aS_aSbS", "0A1B", "E_amb", "inherent", "i_j_or_i_k_pos", "ijk_or", "E_unamb", "paren", "eq_01"):
        g, sig, _ = G[k]
        print(k, "ambiguous witness:", ambiguous_witness(g, sig, 7 if len(sig) <= 3 else 5))
    print("aab trees:", G["aS_aSbS"][0].count("aab"), " a+a*a trees:", G["E_amb"][0].count("a+a*a"), G["E_unamb"][0].count("a+a*a"))
    print("abc:", G["amb_given"][0].count("abc"), " abcd:", G["inherent"][0].count("abcd"), " aabbccdd:", G["inherent"][0].count("aabbccdd"))
    E2 = CFG({"E": ["E+T", "T"], "T": ["E*F", "F"], "F": ["(E)", "a", "b"]}, "E")
    print("((a+b)*b) in 2011-12 grammar:", E2.count("((a+b)*b)"))
    D = CFG({"D": ["TL;"], "T": ["bin_"], "L": ["L,V", "V"], "V": ["I", "I=N"], "I": ["a", "b", "Ia", "Ib", "I0", "I1"], "N": ["1", "N1", "N0"]}, "D")
    print("bin_ab00=101,b1,b1;", D.count("bin_ab00=101,b1,b1;"), " bin_a=10,b=1;", D.count("bin_a=10,b=1;"))
    print("ALL OK" if ok else "FAIL")
