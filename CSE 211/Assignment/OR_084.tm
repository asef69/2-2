#! start s
#! end halt
#! fill B

s X X R s
s Y Y R s
s 0 X R a0
s 1 Y R a1
s c c R b0

a0 0 0 R a0
a0 1 1 R a0
a0 c c R p0
a1 0 0 R a1
a1 1 1 R a1
a1 c c R p1

p0 X X R p0
p0 Y Y R p0
p0 0 X R r0
p0 1 Y R r1
p0 c c R r0
p1 X X R p1
p1 Y Y R p1
p1 0 X R r1
p1 1 Y R r1
p1 c c R r1

b0 X X R b0
b0 Y Y R b0
b0 0 X R r0
b0 1 Y R r1
b0 c c L clean

r0 0 0 R r0
r0 1 1 R r0
r0 c c R r0
r0 B 0 L back
r1 0 0 R r1
r1 1 1 R r1
r1 c c R r1
r1 B 1 L back

back 0 0 L back
back 1 1 L back
back X X L back
back Y Y L back
back c c L back
back B B R s

clean X 0 L clean
clean Y 1 L clean
clean 0 0 L clean
clean 1 1 L clean
clean c c L clean
clean B B R halt
