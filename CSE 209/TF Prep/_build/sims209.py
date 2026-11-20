"""Small simulators used to compute (and check) every worked example in the general-steps PDF."""


def pipe(instrs, fwd=True, split=True):
    """5-stage MIPS pipeline, branch decided in ID, predict-not-taken, in-order, RAW hazards only.
    instr = dict(txt, op in alu|lw|sw|br, dst, srcs (needed at EX / ID for br), dsrcs (store data), taken)
    Returns list of dicts with idf (first ID cycle), ex, fetch, stalls; plus totals."""
    res = []
    for i, ins in enumerate(instrs):
        if i == 0:
            idf, fetch = 2, 1
        else:
            p = res[-1]
            if p["taken"]:
                idf = p["ex"] + 1
                fetch = idf - 1
            else:
                idf = p["ex"]
                fetch = p["idf"]
        ex = idf + 1
        srcs = list(ins.get("srcs", []))
        if not fwd:
            srcs += list(ins.get("dsrcs", []))
        for s in srcs:
            j = None
            for k in range(i - 1, -1, -1):
                if res[k]["dst"] == s and s not in (None, "$zero"):
                    j = k
                    break
            if j is None:
                continue
            pj = res[j]
            if ins["op"] == "br":
                if fwd:
                    need_id = pj["ex"] + (2 if pj["op"] == "lw" else 1)
                else:
                    need_id = pj["ex"] + (2 if split else 3)
                ex = max(ex, need_id + 1)
            else:
                if fwd:
                    need = pj["ex"] + (2 if pj["op"] == "lw" else 1)
                else:
                    need = pj["ex"] + (3 if split else 4)
                ex = max(ex, need)
        r = dict(ins)
        r.update(idf=idf, ex=ex, fetch=fetch, stalls=ex - (idf + 1), taken=bool(ins.get("taken")))
        res.append(r)
    n = len(res)
    stalls = sum(r["stalls"] for r in res)
    pen = sum(1 for r in res if r["taken"])
    total = res[-1]["ex"] + 2
    assert total == n + 4 + stalls + pen, (total, n, stalls, pen)
    return res, dict(n=n, stalls=stalls, penalty=pen, total=total)


def I(txt, op, dst=None, srcs=(), dsrcs=(), taken=False):
    return dict(txt=txt, op=op, dst=dst, srcs=list(srcs), dsrcs=list(dsrcs), taken=taken)


def cache(seq, block_bytes, nsets, ways=1, unit="byte"):
    """Set-associative LRU cache trace. seq = addresses (byte addresses if unit=='byte', else word/unit addresses
    with block_bytes meaning words per block). Returns (rows, final)."""
    sets = [[] for _ in range(nsets)]  # list of (tag) in LRU order, most recent last
    rows, hits = [], 0
    for a in seq:
        blk = a // block_bytes
        s = blk % nsets
        tag = blk // nsets
        st = sets[s]
        if tag in st:
            st.remove(tag)
            st.append(tag)
            hit, note = True, ""
            hits += 1
        else:
            note = ""
            if len(st) >= ways:
                old = st.pop(0)
                note = f"replaces block {old * nsets + s} (tag {old})"
            st.append(tag)
            hit = False
        rows.append(dict(addr=a, blk=blk, idx=s, tag=tag, hit=hit, note=note))
    return rows, sets, hits


def tlb(vas, page_bits, entries, pt):
    """Fully associative LRU TLB. pt: dict vpn -> ppn (missing = not in memory)."""
    t = []  # list of vpn, LRU first
    rows = []
    for va in vas:
        vpn, off = va >> page_bits, va & ((1 << page_bits) - 1)
        if vpn in t:
            t.remove(vpn)
            t.append(vpn)
            rows.append(dict(va=va, vpn=vpn, off=off, res="TLB hit", ppn=pt[vpn], pa=(pt[vpn] << page_bits) | off, tlb=list(t)))
            continue
        if vpn in pt:
            if len(t) >= entries:
                t.pop(0)
            t.append(vpn)
            rows.append(dict(va=va, vpn=vpn, off=off, res="TLB miss, page-table hit", ppn=pt[vpn], pa=(pt[vpn] << page_bits) | off, tlb=list(t)))
        else:
            rows.append(dict(va=va, vpn=vpn, off=off, res="TLB miss, page fault", ppn=None, pa=None, tlb=list(t)))
    return rows


def predictor(outcomes, bits=1, init=0):
    """outcomes: list of 1 (taken)/0. 1-bit: state = last outcome. 2-bit saturating counter 0..3, predict taken if >=2."""
    st = init
    miss = 0
    for o in outcomes:
        pred = (st >= 1) if bits == 1 else (st >= 2)
        if bits == 1:
            if int(pred) != o:
                miss += 1
            st = o
        else:
            if int(pred) != o:
                miss += 1
            st = min(3, st + 1) if o else max(0, st - 1)
    return miss
