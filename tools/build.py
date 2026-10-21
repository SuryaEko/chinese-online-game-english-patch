import json,re,glob,sys
S=sys.argv[1]
k=json.load(open(S+'/todo.json',encoding='utf-8'))
tr={}
for f in sorted(glob.glob(S+'/tr/b*.txt')):
    for ln in open(f,encoding='utf-8'):
        ln=ln.rstrip('\n')
        if not ln: continue
        i,_,t=ln.partition('|')
        tr[int(i)]=t.replace('<NL>','\n')
out={};missing=[];bad=[]
han=re.compile('[\u3400-\u9fff]')
for i,z in enumerate(k):
    if i not in tr:
        if z.startswith('错误代码') or z.startswith('Steam错误代码'):
            tr[i]=z.replace('Steam错误代码','Steam Error Code').replace('错误代码','Error Code')
        else:
            missing.append(i); continue
    e=tr[i]
    if han.search(e): bad.append((i,'han'))
    if re.findall(r'<[^>]*>',z)!=re.findall(r'<[^>]*>',e) and re.findall(r'<(?!NL)[^>]*>',z)!=re.findall(r'<[^>]*>',e): bad.append((i,'tags'))
    if re.findall(r'\{\d+\}',z)!=re.findall(r'\{\d+\}',e): bad.append((i,'fmt'))
    out[z]=e
json.dump(out,open(S+'/final.json','w',encoding='utf-8'),ensure_ascii=False)
print('translated',len(out),'missing',len(missing),'flags',len(bad))
print('MISSING:',[(i,k[i][:25]) for i in missing][:120])
print('BAD:',[(i,w,k[i][:30]) for i,w in bad][:60])
