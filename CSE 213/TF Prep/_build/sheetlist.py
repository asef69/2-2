"""sheetlist.py pdf outprefix [--per 12] [--cols 3] [--dpi 50] [--pages 1,2,5-9]  -> contact sheets of 'final build' pages"""
import sys, pymupdf, re
args=sys.argv[1:]; pdf, pre = args[0], args[1]
opt=dict(per=12, cols=3, dpi=50); pages=None
for k in ('per','cols','dpi'):
    if '--'+k in args: opt[k]=int(args[args.index('--'+k)+1])
if '--pages' in args:
    pages=[]
    for part in args[args.index('--pages')+1].split(','):
        a,_,b=part.partition('-'); pages+=list(range(int(a),int(b or a)+1))
d=pymupdf.open(pdf)
def title(i):
    lines=[l.strip() for l in d[i-1].get_text().split('\n') if l.strip() and 'Nafis' not in l and 'Lecturer' not in l]
    return lines[0] if lines else ''
if pages is None:
    n=d.page_count; pages=[]
    for i in range(1,n+1):
        if i==n: pages.append(i); continue
        t1=d[i-1].get_text(); t2=d[i].get_text()
        # build step if next page has same title and contains all of this page's text tokens
        w1={x for x in t1.split() if not x.isdigit()}; w2={x for x in t2.split() if not x.isdigit()}
        if title(i)==title(i+1) and w1<=w2:
            # also check images grow: compare pixmap difference small? keep simple
            continue
        pages.append(i)
print(len(pages), pages)
for s in range(0,len(pages),opt['per']):
    chunk=pages[s:s+opt['per']]
    pix=[d[i-1].get_pixmap(dpi=opt['dpi']) for i in chunk]
    w=max(p.width for p in pix); h=max(p.height for p in pix); cols=opt['cols']; rows=(len(pix)+cols-1)//cols
    out=pymupdf.open(); pg=out.new_page(width=cols*w,height=rows*(h+18))
    for k,(i,px) in enumerate(zip(chunk,pix)):
        x,y=(k%cols)*w,(k//cols)*(h+18)
        pg.insert_image(pymupdf.Rect(x,y+16,x+px.width,y+16+px.height),pixmap=px)
        pg.insert_text((x+4,y+12),f"p{i}",fontsize=12,color=(0.8,0,0))
    fn=f"{pre}_{s//opt['per']+1:02d}.png"; pg.get_pixmap(dpi=72).save(fn); print(fn)
