import json, math, collections, itertools, sys
A='attack-sim/'
Z=1.959963984540054
def wilson(k,n):
    if n==0: return (None,None)
    p=k/n
    c=(p+Z*Z/(2*n))/(1+Z*Z/n)
    m=Z*math.sqrt(p*(1-p)/n+Z*Z/(4*n*n))/(1+Z*Z/n)
    return (max(0.0,c-m)*100,min(1.0,c+m)*100)
corpus={}
for l in open(A+'combined_corpus_round5_20261025.jsonl'):
    r=json.loads(l); corpus[r['id']]=r
CATS=['sqli','path_traversal','cmdi','xss']
CF=['config1','config2','config3a','config3b']
def load(cfg,run):
    d=json.load(open(A+f'results_combined_{cfg}_run{run}_20261025.json'))['results']
    return {r['id']:r for r in d}
R={(c,k):load(c,k) for c in CF for k in (1,2,3)}
out={}
def unb(cfg,run=1,cat=None):
    return {i for i,r in R[(cfg,run)].items() if r['blocked'] is not True and (cat is None or r['category']==cat)}
M={c:unb(c) for c in CF}
v1={}
for cat in CATS:
    m3a=unb('config3a',1,cat); m2=unb('config2',1,cat); m3b=unb('config3b',1,cat)
    v1[cat]={'M3a':sorted(m3a),'M2':sorted(m2),'M3b':sorted(m3b),'M3a_n_M2':sorted(m3a&m2),'M3a_n_M2_n_M3b':sorted(m3a&m2&m3b),'M3a_n_M3b':sorted(m3a&m3b),'M2_n_M3b':sorted(m2&m3b)}
out['V1']=v1
v2={}
for cat in CATS:
    m3a=unb('config3a',1,cat); m2=unb('config2',1,cat); m3b=unb('config3b',1,cat)
    blocked_by_3b_among_3a_miss=sorted(m3a-m3b)
    blocked_by_2_among_3a_miss=sorted(m3a-m2)
    v2[cat]={'M3a_minus_M3b':blocked_by_3b_among_3a_miss,'M3a_minus_M2':blocked_by_2_among_3a_miss,'blocked_3b_not_blocked_2_among_3a_miss':sorted((m3a-m3b)&m2),'blocked_2_not_blocked_3b_among_3a_miss':sorted((m3a-m2)&m3b),'M2_minus_M3a_(3a_blocks_2_not)':sorted(m2-m3a),'M3b_minus_M3a':sorted(m3b-m3a)}
out['V2']=v2
def tab(cfg,keyf,cats=('xss',),run=1):
    c=collections.defaultdict(lambda: collections.Counter())
    for i,r in R[(cfg,run)].items():
        if r['category'] in cats:
            c[keyf(i,r)][(r['status'],bool(r['blocked']))]+=1
    return c
v3={}
for cfg in CF:
    res=R[(cfg,1)]
    xs={i:r for i,r in res.items() if r['category']=='xss'}
    n=len(xs); k=sum(1 for r in xs.values() if r['blocked'] is True)
    bio={i:r for i,r in xs.items() if corpus[i]['campo']=='bio'}
    nb=len(bio); kb=sum(1 for r in bio.values() if r['blocked'] is True)
    entry={'n200':{'k':k,'n':n,'wilson':wilson(k,n)},'bio':{'k':kb,'n':nb,'wilson':wilson(kb,nb)}}
    by={}
    for dim in ('campo','transporte'):
        t=collections.defaultdict(collections.Counter)
        for i,r in xs.items():
            t[corpus[i][dim]][(r['status'])]+=1
        by[dim]={a:dict(b) for a,b in t.items()}
    t=collections.defaultdict(collections.Counter)
    for i,r in xs.items():
        t[(corpus[i]['transporte'],corpus[i]['campo'])][r['status']]+=1
    by['transporte_campo']={f'{a[0]}|{a[1]}':dict(b) for a,b in t.items()}
    entry['por_estrato']=by
    v3[cfg]=entry
miss3a=sorted(unb('config3a',1,'xss'))
v3['xss_no_bloqueados_3a']=[{'id':i,**{d:corpus[i][d] for d in ('contexto','vector','funcion','codificacion','transporte','campo')},'status':R[('config3a',1)][i]['status']} for i in miss3a]
out['V3']=v3
EXC=['xss_118','xss_254','xss_342']
v4={}
for cfg in CF:
    xs=[i for i,r in R[(cfg,1)].items() if r['category']=='xss' and i not in EXC]
    k=sum(1 for i in xs if R[(cfg,1)][i]['blocked'] is True); n=len(xs)
    bio=[i for i in xs if corpus[i]['campo']=='bio']
    kb=sum(1 for i in bio if R[(cfg,1)][i]['blocked'] is True)
    v4[cfg]={'n':n,'k':k,'wilson':wilson(k,n),'bio':{'n':len(bio),'k':kb,'wilson':wilson(kb,len(bio))},'excluidos_no_bloqueados':[i for i in EXC if R[(cfg,1)][i]['blocked'] is not True]}
out['V4']=v4
v5={}
three=['sqli','path_traversal','cmdi']
m3a3={i for i in M['config3a'] if corpus[i]['category'] in three}
m23={i for i in M['config2'] if corpus[i]['category'] in three}
m3b3={i for i in M['config3b'] if corpus[i]['category'] in three}
v5={'n_payloads':sum(1 for i in corpus if corpus[i]['category'] in three),'3a_no_bloquea':len(m3a3),'3b_bloquea_de_esos':len(m3a3-m3b3),'2_bloquea_de_esos':len(m3a3-m23),'3a_no_bloquea_por_cat':{c:len({i for i in m3a3 if corpus[i]['category']==c}) for c in three},'bloqueados_por_3b_por_cat':{c:len({i for i in m3a3-m3b3 if corpus[i]['category']==c}) for c in three},'bloqueados_por_2_por_cat':{c:len({i for i in m3a3-m23 if corpus[i]['category']==c}) for c in three}}
out['V5']=v5
v5all={'3a_no_bloquea':len(M['config3a']),'3b_bloquea_de_esos':len(M['config3a']-M['config3b']),'2_bloquea_de_esos':len(M['config3a']-M['config2'])}
out['V5_800']=v5all
agg={'libreria_sola(c2)':sum(1 for r in R[('config2',1)].values() if r['blocked'] is True),'waf_solo(3a)':sum(1 for r in R[('config3a',1)].values() if r['blocked'] is True),'combinacion(3b)':sum(1 for r in R[('config3b',1)].values() if r['blocked'] is True)}
agg['aporte_waf_sobre_libreria(3b-c2)']=agg['combinacion(3b)']-agg['libreria_sola(c2)']
agg['aporte_libreria_sobre_waf(3b-3a)']=agg['combinacion(3b)']-agg['waf_solo(3a)']
agg['union_c2_3a']=len({i for i in corpus if R[('config2',1)][i]['blocked'] is True or R[('config3a',1)][i]['blocked'] is True})
agg['por_cat']={cat:{c:sum(1 for i,r in R[(c,1)].items() if r['category']==cat and r['blocked'] is True) for c in CF} for cat in CATS}
out['agregados']=agg
v9={}
tot=0; flips=0; flipids=collections.defaultdict(list)
for cfg in CF:
    for i in corpus:
        vs=[R[(cfg,k)][i]['blocked'] for k in (1,2,3)]
        tot+=3
        if len(set(vs))>1:
            flips+=1; flipids[cfg].append(i)
v9={'payload_corridas':tot,'payloads_con_veredicto_distinto':flips,'ids':dict(flipids),'comparaciones_pares_run':len(CF)*len(corpus)*2}
out['V9']=v9
json.dump(out,open('docs/evidence/errata-v1-v5-v9-20261025.json','w'),ensure_ascii=False,indent=1)
print(json.dumps({'V1':{c:{k:(len(v) if isinstance(v,list) else v) for k,v in d.items()} for c,d in v1.items()}},indent=0))
for c in CATS: print(c,'M3a&M2&M3b',v1[c]['M3a_n_M2_n_M3b'],'M3a&M2',v1[c]['M3a_n_M2'],'M3b',v1[c]['M3b'])
print('V2 cmdi blocked 3b not 2 among 3a-miss:',v2['cmdi']['blocked_3b_not_blocked_2_among_3a_miss'],'| blocked 2 not 3b:',v2['cmdi']['blocked_2_not_blocked_3b_among_3a_miss'])
print('V2 others',{c:(v2[c]['blocked_3b_not_blocked_2_among_3a_miss'],v2[c]['blocked_2_not_blocked_3b_among_3a_miss']) for c in CATS})
print(json.dumps(v5)); print(json.dumps(v5all)); print(json.dumps(agg)); print(json.dumps(v9))
for cfg in CF: print('V3',cfg,v3[cfg]['n200'],v3[cfg]['bio'])
print(json.dumps(v3['xss_no_bloqueados_3a'],ensure_ascii=False))
print('V4',json.dumps(v4))
