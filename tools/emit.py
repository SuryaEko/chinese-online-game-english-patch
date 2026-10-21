import json,sys
S,OUT=sys.argv[1],sys.argv[2]
d=json.load(open(S+'/final.json',encoding='utf-8'))
def esc(s): return s.replace('\\','\\\\').replace('=','\\=').replace('\r','\\r').replace('\n','\\n')
lines=[]
for z,e in d.items():
    z=z.strip();e=e.strip()
    if not z: continue
    lines.append(esc(z)+'='+esc(e))
open(OUT,'w',encoding='utf-8',newline='\n').write('\n'.join(lines)+'\n')
print(len(lines))
