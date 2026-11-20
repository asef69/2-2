"""MIPS answers used verbatim in the Ch2 notes and tested by verify.py (single source of truth)."""

DOWHILE_2324 = """\
main:  addi $t0, $zero, 5      # a = 5
       addi $t1, $zero, 10     # b = 10
       addi $t2, $zero, 2      # c = 2
       addi $t3, $zero, 30     # N = 30
Loop:  sll  $t4, $t0, 2        # t4 = a << 2
       slt  $t5, $t1, $t4      # t5 = 1 if b < (a<<2), i.e. (a<<2) > b
       beq  $t5, $zero, Else   # condition false -> else part
       addi $t0, $t0, 2        # a += 2
       add  $t1, $t1, $t0      # b += a
       j    Cond
Else:  add  $t0, $t0, $t2      # a += c
       add  $t1, $t1, $t2      # b += c
Cond:  slt  $t5, $t0, $t3      # t5 = 1 if a < N
       bne  $t5, $zero, Loop   # repeat while a < N
       add  $v0, $zero, $zero  # return 0
       jr   $ra"""

FRAG1_1920 = """\
frag1: add  $s0, $zero, $zero  # sum = 0
       addi $s1, $zero, 100    # x = 100
Loop:  slti $t0, $s1, -5       # t0 = 1 if x < -5
       bne  $t0, $zero, Exit   # leave when !(x >= -5)
       add  $s0, $s0, $s1      # sum = sum + x
       addi $s1, $s1, -1       # x = x - 1
       j    Loop
Exit:  jr   $ra"""

FRAG2_1920 = """\
frag2: lui  $t0, 2             # t0 = 0x0002_0000 = 131072
       ori  $t0, $t0, 3        # t0 = 131075 (too big for a 16-bit immediate)
       add  $t0, $s1, $t0      # t0 = y + 131075
       slt  $t1, $t0, $s0      # t1 = 1 if (y + 131075) < x
       beq  $t1, $zero, Skip
       addi $s0, $zero, 1      # x = 1
Skip:  jr   $ra"""

FRAG3_1920 = """\
frag3: lui  $t0, 8             # t0 = 0x0008_0000
       ori  $t0, $t0, 12       # t0 = 0x0008_000C = 131075 x 4 = 524300
       add  $t0, $t0, $s2      # t0 = &A[131075]
       lw   $t1, 0($t0)        # t1 = A[131075]
       addi $s0, $t1, 5        # x = A[131075] + 5
       jr   $ra"""

FRAG_2223_305 = """\
frag:  lui  $t0, 2             # t0 = 131072
       ori  $t0, $t0, 3        # t0 = 131075
       add  $t0, $t2, $t0      # t0 = y + 131075
       slt  $t3, $t0, $t1      # t3 = 1 if y + 131075 < x
       beq  $t3, $zero, Skip
       addi $t1, $zero, 8      # x = 8
Skip:  jr   $ra"""

TESTFUNC_2021 = """\
testFunc: add  $s1, $zero, $zero   # i = 0
          add  $s2, $zero, $zero   # result = 0
Loop:     slt  $t0, $a1, $s1       # t0 = 1 if b < i, i.e. i > b
          beq  $t0, $zero, Skip
          add  $s2, $s2, $a2       # result += c
Skip:     addi $s1, $s1, 1         # i++
          slt  $t0, $s1, $a0       # t0 = 1 if i < a
          bne  $t0, $zero, Loop    # do ... while (i < a)
          add  $v0, $s2, $zero     # return result
          jr   $ra"""

FUN_2223 = """\
fun:   bne  $a1, $zero, L1     # b != 0 -> recursive cases
       add  $v0, $zero, $zero  # return 0
       jr   $ra
L1:    addi $sp, $sp, -8       # frame for $ra and a
       sw   $ra, 4($sp)
       sw   $a0, 0($sp)        # save a (needed after the 2nd call)
       sra  $t0, $a1, 1        # t0 = b / 2   (b >= 0 assumed)
       bne  $t0, $zero, L2
       sll  $a0, $a0, 2        # arg1 = a * 4
       sra  $a1, $a1, 3        # arg2 = b / 8
       jal  fun                # v0 = fun(a*4, b/8)
       j    Done
L2:    add  $a0, $a0, $a0      # arg1 = a + a
       sra  $a1, $a1, 2        # arg2 = b / 4
       jal  fun                # v0 = fun(a+a, b/4)
       lw   $t1, 0($sp)        # t1 = original a
       add  $v0, $v0, $t1      # v0 = fun(...) + a
Done:  lw   $ra, 4($sp)
       addi $sp, $sp, 8
       jr   $ra"""

POW_1819 = """\
fun:   bne  $a1, $zero, L1     # b != 0 -> recursive cases
       add  $v0, $zero, $zero  # return 0 (as printed; for a^b use addi $v0, $zero, 1)
       jr   $ra
L1:    addi $sp, $sp, -8
       sw   $ra, 4($sp)
       sw   $a0, 0($sp)        # save a
       andi $t0, $a1, 1        # t0 = b % 2  (b >= 0)
       mul  $a0, $a0, $a0      # arg1 = a * a
       srl  $a1, $a1, 1        # arg2 = b / 2
       bne  $t0, $zero, Odd    # decide BEFORE the call ($t0 is not preserved)
       jal  fun                # even: return fun(a*a, b/2)
       j    Done
Odd:   jal  fun                # odd: fun(a*a, b/2) * a
       lw   $t1, 0($sp)
       mul  $v0, $v0, $t1
Done:  lw   $ra, 4($sp)
       addi $sp, $sp, 8
       jr   $ra"""

FIB_2122 = """\
fib:   slti $t0, $a0, 2        # n < 2 ?  (n = 0 -> 0, n = 1 -> 1)
       beq  $t0, $zero, Rec
       add  $v0, $a0, $zero    # return n
       jr   $ra
Rec:   addi $sp, $sp, -12      # room for $ra, n, fib(n-1)
       sw   $ra, 8($sp)
       sw   $a0, 4($sp)
       addi $a0, $a0, -1
       jal  fib                # v0 = fib(n-1)
       sw   $v0, 0($sp)        # keep it across the next call
       lw   $a0, 4($sp)
       addi $a0, $a0, -2
       jal  fib                # v0 = fib(n-2)
       lw   $t1, 0($sp)
       add  $v0, $v0, $t1      # fib(n-1) + fib(n-2)
       lw   $ra, 8($sp)
       addi $sp, $sp, 12
       jr   $ra"""

F_NESTED_2223 = """\
f:     addi $sp, $sp, -8       # frame: $ra and c+d
       sw   $ra, 4($sp)
       add  $t0, $a2, $a3      # t0 = c + d
       sw   $t0, 0($sp)        # $t0 is not preserved across a call
       jal  func               # v0 = func(a, b)   (a, b already in $a0, $a1)
       add  $a0, $v0, $zero    # arg1 = func(a, b)
       lw   $a1, 0($sp)        # arg2 = c + d
       jal  func               # v0 = func(func(a,b), c+d)
       lw   $ra, 4($sp)
       addi $sp, $sp, 8
       jr   $ra"""

SUM_1314 = """\
sum:   slti $t0, $a0, 1        # n <= 0 ?
       beq  $t0, $zero, Rec
       add  $v0, $zero, $zero  # return 0
       jr   $ra
Rec:   addi $sp, $sp, -8
       sw   $ra, 4($sp)
       sw   $a0, 0($sp)
       addi $a0, $a0, -1
       jal  sum                # v0 = sum(n-1)
       lw   $a0, 0($sp)
       lw   $ra, 4($sp)
       addi $sp, $sp, 8
       add  $v0, $a0, $v0      # n + sum(n-1)
       jr   $ra"""

RECURSESUM_1415 = """\
recurseSum:
       slti $t0, $a0, 1        # blank 1: slti
       beq  $t0, $zero, Recurse
       add  $v0, $zero, $zero
       jr   $ra                # blank 2: $ra
Recurse:
       addi $sp, $sp, -8       # blank 3: -8
       sw   $ra, 4($sp)        # blank 4: 4($sp)
       sw   $a0, 0($sp)        # blank 5: $a0
       addi $a0, $a0, -1
       jal  recurseSum
       lw   $a0, 0($sp)        # blank 6: $a0
       lw   $ra, 4($sp)        # blank 7: 4($sp)
       addi $sp, $sp, 8        # blank 8: the whole line
       add  $v0, $a0, $v0      # blank 9: $v0
       jr   $ra                # blank 10: $ra"""

RSTRCOPY_1516 = """\
rstrcopy: lbu  $t0, 0($a1)     # t0 = *source
          beq  $t0, $zero, End # *source == '\\0' ?
          sb   $t0, 0($a0)     # *dest = *source
          addi $a0, $a0, 1     # dest++
          addi $a1, $a1, 1     # source++
          addi $sp, $sp, -4
          sw   $ra, 0($sp)
          jal  rstrcopy        # rstrcopy(dest, source)
          lw   $ra, 0($sp)
          addi $sp, $sp, 4
          jr   $ra
End:      sb   $zero, 0($a0)   # *dest = '\\0'
          jr   $ra"""

RSTRCOPY_MIN = """\
rcopy: lbu  $t0, 0($a1)        # t0 = *source
       sb   $t0, 0($a0)        # copy it (the final '\\0' too)
       beq  $t0, $zero, Done
       addi $a0, $a0, 1        # dest++
       addi $a1, $a1, 1        # source++
       j    rcopy              # tail call = jump, no stack frame
Done:  jr   $ra"""

SORT_1718 = """\
swap:  sll  $t1, $a1, 2        # t1 = k * 4
       add  $t1, $a0, $t1      # t1 = &v[k]
       lw   $t0, 0($t1)        # temp = v[k]
       lw   $t2, 4($t1)        # t2 = v[k+1]
       sw   $t2, 0($t1)        # v[k] = v[k+1]
       sw   $t0, 4($t1)        # v[k+1] = temp
       jr   $ra
sort:  addi $sp, $sp, -20      # save $ra, $s3..$s0
       sw   $ra, 16($sp)
       sw   $s3, 12($sp)
       sw   $s2, 8($sp)
       sw   $s1, 4($sp)
       sw   $s0, 0($sp)
       move $s2, $a0           # s2 = v
       move $s3, $a1           # s3 = n
       move $s0, $zero         # i = 0
for1:  slt  $t0, $s0, $s3      # i < n ?
       beq  $t0, $zero, exit1
       addi $s1, $s0, -1       # j = i - 1
for2:  slti $t0, $s1, 0        # j < 0 ?
       bne  $t0, $zero, exit2
       sll  $t1, $s1, 2
       add  $t2, $s2, $t1      # t2 = &v[j]
       lw   $t3, 0($t2)        # v[j]
       lw   $t4, 4($t2)        # v[j+1]
       slt  $t0, $t4, $t3      # v[j] > v[j+1] ?
       beq  $t0, $zero, exit2
       move $a0, $s2           # swap(v, j)
       move $a1, $s1
       jal  swap
       addi $s1, $s1, -1       # j -= 1
       j    for2
exit2: addi $s0, $s0, 1        # i += 1
       j    for1
exit1: lw   $s0, 0($sp)        # restore and return
       lw   $s1, 4($sp)
       lw   $s2, 8($sp)
       lw   $s3, 12($sp)
       lw   $ra, 16($sp)
       addi $sp, $sp, 20
       jr   $ra"""

SWITCH_1213 = """\
sw1:   slt  $t3, $s5, $zero    # k < 0 ?
       bne  $t3, $zero, Exit
       slti $t3, $s5, 4        # k < 4 ?
       beq  $t3, $zero, Exit
       sll  $t1, $s5, 2        # t1 = 4k
       add  $t1, $t1, $t4      # t1 = &JumpTable[k]  ($t4 = table base)
       lw   $t0, 0($t1)        # t0 = JumpTable[k]
       jr   $t0                # jump to the case
L0:    add  $s0, $s3, $s4      # case 0: f = i + j
       j    Exit
L1:    add  $s0, $s1, $s2      # case 1: f = g + h
       j    Exit
L2:    sub  $s0, $s1, $s2      # case 2: f = g - h
       j    Exit
L3:    sub  $s0, $s3, $s4      # case 3: f = i - j
Exit:  jr   $ra"""
