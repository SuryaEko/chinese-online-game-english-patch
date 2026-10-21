import re,struct,json,glob,os,sys
D=sys.argv[1]; OUT=sys.argv[2]
cjk=re.compile(rb'(?:[\xe3-\xe9][\x80-\xbf]{2}|\xef\xbc[\x80-\xbf]|\xef\xbd[\x80-\xbf])+')
han=re.compile('[㐀-鿿＀-￯]')
found={}
def hasHan(s): return bool(re.search('[㐀-鿿]',s))
def scan(path):
    b=open(path,'rb').read()
    n=0
    for m in cjk.finditer(b):
        s,e=m.span()
        if len(b[s:e])<6 and not (s>=4): continue
        lo=max(0,s-4096)
        for p in range(s-4,lo-1,-1):
            L=struct.unpack_from('<I',b,p)[0]
            if L<=0 or L>4096 or p+4+L<e or p+4>s: continue
            try: t=b[p+4:p+4+L].decode('utf-8')
            except: continue
            if hasHan(t) and '\x00' not in t:
                found[t]=os.path.basename(path); n+=1
            break
    return n
files=[f for f in glob.glob(D+'/*') if os.path.isfile(f) and not f.endswith(('.resS','.resource','.json','.info','.config'))]
for f in sorted(files): print(os.path.basename(f),scan(f),flush=True)
# metadata string literals
m=open(D+'/il2cpp_data/Metadata/global-metadata.dat','rb').read()
tOff,tSize,dOff,dSize=struct.unpack_from('<4I',m,8)
k=0
for i in range(tSize//8):
    L,idx=struct.unpack_from('<II',m,tOff+i*8)
    try: t=m[dOff+idx:dOff+idx+L].decode('utf-8')
    except: continue
    if hasHan(t): found.setdefault(t,'metadata'); k+=1
print('metadata',k)
json.dump(found,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('unique',len(found))
