import importlib.util, json, urllib.request, http.cookiejar, collections, sys, time
A='attack-sim/'
spec=importlib.util.spec_from_file_location('h',A+'run_large_corpus_fixed.py')
h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
corpus={json.loads(l)['id']:json.loads(l) for l in open(A+'combined_corpus_round5_20261025.jsonl')}
IDS=['cmdi_112','cmdi_134','cmdi_31','cmdi_38','cmdi_6']
def send(base, spec_row):
    h.BASE_URL=base
    jar=http.cookiejar.CookieJar()
    op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    op.addheaders=[('Cookie','connect.sid=s%3Afixedcookie20261025')]
    return h.do_request(op,spec_row)
open(A+'capture_direct_20261025.jsonl','w').close()
out=[]
for route,base in (('directa','http://127.0.0.1:9301'),('via_waf','http://127.0.0.1:9302')):
    for i in IDS:
        before=sum(1 for _ in open(A+'capture_direct_20261025.jsonl'))
        r=send(base,corpus[i]); time.sleep(0.3)
        rows=[json.loads(l) for l in open(A+'capture_direct_20261025.jsonl')]
        got=rows[before:]
        out.append({'ruta':route,'id':i,'status_cliente':r.get('status'),'registros_recibidos':len(got),'recibido':got[-1] if got else None})
json.dump(out,open('docs/evidence/phase2b-capture-20261025.json','w'),ensure_ascii=False,indent=1)
by=collections.defaultdict(dict)
for o in out: by[o['id']][o['ruta']]=o
res={}
for i,d in by.items():
    a=d['directa']['recibido']; b=d['via_waf']['recibido']
    if not a or not b:
        res[i]={'error':'sin captura','directa':bool(a),'via_waf':bool(b),'status_directa':d['directa']['status_cliente'],'status_via_waf':d['via_waf']['status_cliente']}; continue
    ha=collections.OrderedDict((k.lower(),v) for k,v in a['headers']); hb=collections.OrderedDict((k.lower(),v) for k,v in b['headers'])
    res[i]={'cuerpo_igual':a['raw_body']==b['raw_body'],'objetivo_igual':a['raw_target']==b['raw_target'],'solo_directa':{k:v for k,v in ha.items() if k not in hb},'solo_via_waf':{k:v for k,v in hb.items() if k not in ha},'valor_distinto':{k:[ha[k],hb[k]] for k in ha if k in hb and ha[k]!=hb[k]}}
json.dump(res,open('docs/evidence/phase2b-diff-20261025.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(res,ensure_ascii=False,indent=1))
