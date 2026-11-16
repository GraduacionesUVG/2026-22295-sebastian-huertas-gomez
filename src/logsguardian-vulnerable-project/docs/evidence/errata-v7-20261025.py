import json, hashlib
A='attack-sim/'
orig=json.load(open(A+'large_corpus_requests.json'))
if isinstance(orig,dict):
    orig=orig.get('requests') or orig.get('corpus') or list(orig.values())[0]
comb=[json.loads(l) for l in open(A+'combined_corpus_round5_20261025.jsonl')]
def canon(r):
    r={k:v for k,v in r.items() if k!='schema'}
    return json.dumps(r,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def h(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
o={r['id']:r for r in orig if r['category'] in ('sqli','path_traversal','cmdi')}
c={r['id']:r for r in comb if r['category'] in ('sqli','path_traversal','cmdi')}
res={'n_original':len(o),'n_combinado':len(c),'ids_solo_original':sorted(set(o)-set(c)),'ids_solo_combinado':sorted(set(c)-set(o))}
diff=[i for i in o if i in c and h(canon(o[i]))!=h(canon(c[i]))]
res['peticiones_con_hash_distinto']=diff
res['hash_global_original']=h('\n'.join(h(canon(o[i])) for i in sorted(o)))
res['hash_global_combinado']=h('\n'.join(h(canon(c[i])) for i in sorted(c)))
res['orden_igual']=[r['id'] for r in orig if r['category'] in ('sqli','path_traversal','cmdi')]==[r['id'] for r in comb if r['category'] in ('sqli','path_traversal','cmdi')]
res['categorias_original']={k:sum(1 for r in orig if r['category']==k) for k in sorted({r['category'] for r in orig})}
res['sha256_large_corpus_requests']=hashlib.sha256(open(A+'large_corpus_requests.json','rb').read()).hexdigest()
res['sha256_combined_corpus']=hashlib.sha256(open(A+'combined_corpus_round5_20261025.jsonl','rb').read()).hexdigest()
json.dump(res,open('docs/evidence/errata-v7-20261025.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(res,ensure_ascii=False,indent=1))
