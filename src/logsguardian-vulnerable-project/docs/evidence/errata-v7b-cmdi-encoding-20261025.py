import json, re, math
A='attack-sim/'
Z=1.959963984540054
def wilson(k,n):
    p=k/n
    c=(p+Z*Z/(2*n))/(1+Z*Z/n)
    m=Z*math.sqrt(p*(1-p)/n+Z*Z/(4*n*n))/(1+Z*Z/n)
    return (round(max(0.0,c-m)*100,1),round(min(1.0,c+m)*100,1))
corpus={json.loads(l)['id']:json.loads(l) for l in open(A+'combined_corpus_round5_20261025.jsonl')}
enc={i for i,c in corpus.items() if c['category']=='cmdi' and re.search(r'%[0-9A-Fa-f]{2}',c['payload'])}
cm={i for i,c in corpus.items() if c['category']=='cmdi'}
files={
 'config1_nuevo':A+'results_combined_config1_run1_20261025.json',
 'config2_nuevo':A+'results_combined_config2_run1_20261025.json',
 'config3a_nuevo':A+'results_combined_config3a_run1_20261025.json',
 'config3b_nuevo':A+'results_combined_config3b_run1_20261025.json',
 'config1_viejo_20261010':A+'results_config1-round5-20261010.json',
 'config3a_viejo_20261010':A+'results_config3a-round5-20261010.json',
 'config3b_viejo_20261010':A+'results_config3b-round5-20261010.json',
 'config2_0.1.0_tarball_viejo':A+'results_config2.json',
 'config2_0.1.1_ejecutor_original_20261010':A+'results_config2-published-0.1.1-20261010.json',
 'config2_0.1.1_ejecutor_corregido_20261010':A+'results_config2-published-0.1.1-harness-fixed-20261010.json',
}
out={'cmdi_codificados_n':len(enc),'cmdi_sin_codificar_n':len(cm)-len(enc)}
for name,f in files.items():
    try:
        d=json.load(open(f))
    except Exception as e:
        out[name]={'error':str(e)}; continue
    rows=d.get('results') if isinstance(d,dict) else d
    if rows is None: out[name]={'error':'sin results','keys':list(d.keys())}; continue
    res={r['id']:r for r in rows if isinstance(r,dict) and 'id' in r}
    ids=[i for i in cm if i in res]
    if len(ids)<200: out[name]={'error':f'solo {len(ids)} ids cmdi comparables','n_filas':len(res)}; continue
    ke=sum(1 for i in ids if i in enc and res[i].get('blocked') is True)
    kn=sum(1 for i in ids if i not in enc and res[i].get('blocked') is True)
    out[name]={'codificados':{'k':ke,'n':len(enc),'wilson':wilson(ke,len(enc))},'sin_codificar':{'k':kn,'n':len(cm)-len(enc),'wilson':wilson(kn,len(cm)-len(enc))},'total_cmdi':ke+kn}
json.dump(out,open('docs/evidence/errata-v7b-cmdi-encoding-20261025.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(out,ensure_ascii=False,indent=1))
