import json, math, collections
A='attack-sim/'
Z=1.959963984540054
def wilson(k,n):
    p=k/n
    c=(p+Z*Z/(2*n))/(1+Z*Z/n)
    m=Z*math.sqrt(p*(1-p)/n+Z*Z/(4*n*n))/(1+Z*Z/n)
    return (round(max(0.0,c-m)*100,1),round(min(1.0,c+m)*100,1))
corpus={json.loads(l)['id']:json.loads(l) for l in open(A+'combined_corpus_round5_20261025.jsonl')}
def load(cfg,run=1):
    return {r['id']:r for r in json.load(open(A+f'results_combined_{cfg}_run{run}_20261025.json'))['results']}
out={}
for cfg in ['config1','config2','config3a','config3b']:
    R=load(cfg)
    xs={i:r for i,r in R.items() if r['category']=='xss'}
    st=collections.defaultdict(collections.Counter)
    for i,r in xs.items():
        c=corpus[i]
        st[('campo',c['campo'])][r['status']]+=1
        st[('transporte',c['transporte'])][r['status']]+=1
        st[('transporte|campo',c['transporte']+'|'+c['campo'])][r['status']]+=1
    out[cfg]={'status_por_estrato':{f'{a}={b}':dict(v) for (a,b),v in sorted(st.items())}}
    dims={}
    for dim in ('contexto','vector','funcion','codificacion','transporte','campo'):
        for subset,flt in (('n200',lambda c:True),('bio64',lambda c:c['campo']=='bio')):
            t=collections.defaultdict(lambda:[0,0])
            for i,r in xs.items():
                c=corpus[i]
                if not flt(c): continue
                t[c[dim]][1]+=1
                if r['blocked'] is True: t[c[dim]][0]+=1
            dims[f'{dim}|{subset}']={v:{'k':k,'n':n,'wilson':wilson(k,n)} for v,(k,n) in sorted(t.items())}
    out[cfg]['dimensiones']=dims
    fa=collections.Counter()
    for i,r in xs.items():
        c=corpus[i]
        fa[('alert' in c['payload_raw'].lower(),r['blocked'] is True)]+=1
    out[cfg]['con_alert']={'con':[fa[(True,True)],fa[(True,True)]+fa[(True,False)]],'sin':[fa[(False,True)],fa[(False,True)]+fa[(False,False)]]}
json.dump(out,open('docs/evidence/errata-v3-strata-20261025.json','w'),ensure_ascii=False,indent=1)
for cfg in ['config1','config3a']:
    print(cfg,json.dumps(out[cfg]['status_por_estrato'],ensure_ascii=False))
print('3a codificacion n200',json.dumps(out['config3a']['dimensiones']['codificacion|n200'],ensure_ascii=False))
print('3a codificacion bio',json.dumps(out['config3a']['dimensiones']['codificacion|bio64'],ensure_ascii=False))
print('3a transporte n200',json.dumps(out['config3a']['dimensiones']['transporte|n200'],ensure_ascii=False))
print('3a campo',json.dumps(out['config3a']['dimensiones']['campo|n200'],ensure_ascii=False))
print('con alert',{c:out[c]['con_alert'] for c in out})
