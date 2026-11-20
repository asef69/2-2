"""Tiny MIPS interpreter used only to test the assembly answers in the notes (verify.py)."""
import re

REG = {"$zero": 0, "$at": 1, "$v0": 2, "$v1": 3, "$a0": 4, "$a1": 5, "$a2": 6, "$a3": 7,
       "$gp": 28, "$sp": 29, "$fp": 30, "$ra": 31}
for i in range(8):
    REG[f"$t{i}"] = 8 + i
    REG[f"$s{i}"] = 16 + i
REG["$t8"], REG["$t9"] = 24, 25
for i in range(32):
    REG[f"${i}"] = i
M32 = 0xFFFFFFFF


def s32(x):
    x &= M32
    return x - (1 << 32) if x & 0x80000000 else x


class CPU:
    def __init__(self, src, base=0x00400000):
        self.base = base
        self.labels, self.prog = {}, []
        for line in src.split("\n"):
            line = line.split("#")[0].strip()
            if not line:
                continue
            while ":" in line:
                lab, line = line.split(":", 1)
                self.labels[lab.strip()] = base + 4 * len(self.prog)
                line = line.strip()
            if line:
                op, *rest = line.split(None, 1)
                args = [a.strip() for a in rest[0].split(",")] if rest else []
                self.prog.append((op.lower(), args))
        self.r = [0] * 32
        self.r[29] = 0x7FFFFFFC
        self.r[28] = 0x10008000
        self.mem = {}
        self.hi = self.lo = 0
        self.steps = 0

    # memory (byte addressed, big endian)
    def lb(self, a):
        return self.mem.get(a & M32, 0)

    def sb(self, a, v):
        self.mem[a & M32] = v & 0xFF

    def lw(self, a):
        assert a % 4 == 0, f"unaligned lw {a:#x}"
        return s32(sum(self.lb(a + i) << (24 - 8 * i) for i in range(4)))

    def sw(self, a, v):
        assert a % 4 == 0, f"unaligned sw {a:#x}"
        for i in range(4):
            self.sb(a + i, (v >> (24 - 8 * i)) & 0xFF)

    def R(self, name):
        return self.r[REG[name]]

    def W(self, name, v):
        n = REG[name]
        if n:
            self.r[n] = s32(v)

    def imm(self, s):
        s = s.strip()
        if s in self.labels:
            return self.labels[s]
        return int(s, 0)

    def mem_arg(self, s):
        m = re.match(r"(-?\w*)\((\$\w+)\)", s.replace(" ", ""))
        off = int(m.group(1), 0) if m.group(1) else 0
        return self.R(m.group(2)) + off

    def call(self, label, args=(), max_steps=2_000_000):
        for k, v in enumerate(args):
            self.r[4 + k] = s32(v)
        self.r[31] = 0xDEAD0000
        pc = self.labels[label]
        while pc != 0xDEAD0000:
            self.steps += 1
            assert self.steps < max_steps, "runaway"
            op, a = self.prog[(pc - self.base) // 4]
            npc = pc + 4
            if op in ("add", "addu"):
                self.W(a[0], self.R(a[1]) + self.R(a[2]))
            elif op in ("sub", "subu"):
                self.W(a[0], self.R(a[1]) - self.R(a[2]))
            elif op in ("addi", "addiu"):
                self.W(a[0], self.R(a[1]) + self.imm(a[2]))
            elif op == "and":
                self.W(a[0], self.R(a[1]) & self.R(a[2]))
            elif op == "or":
                self.W(a[0], self.R(a[1]) | self.R(a[2]))
            elif op == "nor":
                self.W(a[0], ~(self.R(a[1]) | self.R(a[2])))
            elif op == "andi":
                self.W(a[0], self.R(a[1]) & (self.imm(a[2]) & 0xFFFF))
            elif op == "ori":
                self.W(a[0], self.R(a[1]) | (self.imm(a[2]) & 0xFFFF))
            elif op == "sll":
                self.W(a[0], self.R(a[1]) << self.imm(a[2]))
            elif op == "srl":
                self.W(a[0], (self.R(a[1]) & M32) >> self.imm(a[2]))
            elif op == "sra":
                self.W(a[0], self.R(a[1]) >> self.imm(a[2]))
            elif op == "slt":
                self.W(a[0], int(self.R(a[1]) < self.R(a[2])))
            elif op == "slti":
                self.W(a[0], int(self.R(a[1]) < self.imm(a[2])))
            elif op == "lui":
                self.W(a[0], (self.imm(a[1]) & 0xFFFF) << 16)
            elif op == "mul":
                self.W(a[0], self.R(a[1]) * self.R(a[2]))
            elif op == "move":
                self.W(a[0], self.R(a[1]))
            elif op == "lw":
                self.W(a[0], self.lw(self.mem_arg(a[1])))
            elif op == "sw":
                self.sw(self.mem_arg(a[1]), self.R(a[0]))
            elif op == "lbu":
                self.W(a[0], self.lb(self.mem_arg(a[1])))
            elif op == "sb":
                self.sb(self.mem_arg(a[1]), self.R(a[0]))
            elif op == "beq":
                if self.R(a[0]) == self.R(a[1]):
                    npc = self.imm(a[2])
            elif op == "bne":
                if self.R(a[0]) != self.R(a[1]):
                    npc = self.imm(a[2])
            elif op == "j":
                npc = self.imm(a[0])
            elif op == "jal":
                self.r[31] = pc + 4
                npc = self.imm(a[0])
            elif op == "jr":
                npc = self.R(a[0]) & M32
            else:
                raise ValueError(op)
            pc = npc
        return self.r[2]
