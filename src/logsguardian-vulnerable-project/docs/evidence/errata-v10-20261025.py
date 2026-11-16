import json, re, urllib.parse, collections
A='attack-sim/'
corpus=[json.loads(l) for l in open(A+'combined_corpus_round5_20261025.jsonl')]
xs=[c for c in corpus if c['category']=='xss']
recs=[json.loads(l)['transaction'] for l in open(A+'waf-audit-20261025/audit-config3b-run1-20261025.jsonl') if l.strip()]
xr=[r for r in recs if r['request']['method']=='POST' and r['request']['uri'] in ('/posts','/profile')]
def body_len(c):
    t=c['transporte']; campo=c['campo']; f=c['forma_enviada']
    if t=='urlencoded':
        if c['codificacion'] in ('url_single','url_double'):
            data=f"{urllib.parse.quote(campo,safe='')}={f}".encode()
        else:
            data=urllib.parse.urlencode({campo:f}).encode()
        return len(data)
    if t=='multipart':
        b='----lsgxssboundary20261025'
        s=f'--{b}\r\nContent-Disposition: form-data; name="{campo}"\r\n\r\n{f}\r\n--{b}--\r\n'
        return len(s.encode('utf-8',errors='replace'))
    return len(json.dumps({campo:f}).encode('utf-8'))
CT={'urlencoded':'application/x-www-form-urlencoded','multipart':'multipart/form-data','json':'application/json'}
def esc(v):
    return v.replace('\\','\\\\') if False else ''.join(ch if (32<=ord(ch)<127) else f'\\x{ord(ch):02x}' for ch in v)
def expected_arg(c):
    f=c['forma_enviada']
    if c['transporte']=='urlencoded':
        return urllib.parse.unquote_plus(f) if c['codificacion'] in ('url_single','url_double') else f
    return f
aligned=0; len_ok=0; ct_ok=0; uri_ok=0
res=[]
for c,r in zip(xs,xr):
    h=r['request']['headers']
    ok_len=int(h.get('Content-Length','-1'))==body_len(c)
    ok_ct=h.get('Content-Type','').split(';')[0]==CT[c['transporte']]
    ok_uri=r['request']['uri']==c['endpoint']
    len_ok+=ok_len; ct_ok+=ok_ct; uri_ok+=ok_uri; aligned+=1
    val=None
    for m in r.get('messages',[]):
        mm=re.search(r"\(Value: `(.*)' \)\s*$",m['details']['match'],re.S)
        if mm and 'ARGS:' in m['details']['match']:
            val=mm.group(1); break
    exp=esc(expected_arg(c))
    trunc=False
    cmpval=val
    if val is not None:
        mt=re.search(r' \((\d+) characters omitted\)$',val)
        if mt:
            trunc=True
            cmpval=val[:mt.start()]
    if val is None:
        igual=None
    elif trunc:
        igual=exp.startswith(cmpval)
    else:
        igual=(val==exp)
    res.append({'id':c['id'],'transporte':c['transporte'],'ok_len':ok_len,'ok_ct':ok_ct,'ok_uri':ok_uri,'valor_registrado':val,'valor_esperado_escapado':exp,'truncado_en_log':trunc,'valor_igual':igual})
summary={'n_corpus_xss':len(xs),'n_registros_auditoria_xss':len(xr),'alineados':aligned,'content_length_coincide':len_ok,'content_type_coincide':ct_ok,'uri_coincide':uri_ok}
by=collections.defaultdict(lambda:[0,0,0,0])
for x in res:
    t=by[x['transporte']]; t[0]+=1
    if x['valor_igual'] is True: t[1]+=1
    if x['valor_igual'] is None: t[2]+=1
    if x['truncado_en_log']: t[3]+=1
summary['valor_arg_igual_por_transporte']={k:{'n':v[0],'iguales_o_prefijo_igual_si_truncado':v[1],'sin_valor_en_log':v[2],'truncados_en_log':v[3]} for k,v in by.items()}
mism=[x for x in res if x['valor_igual'] is False]
summary['ejemplos_distintos']=mism[:6]
summary['muestra_por_transporte']={t:[x for x in res if x['transporte']==t and x['valor_igual']][:3] for t in CT}
json.dump({'resumen':summary,'detalle':res},open('docs/evidence/errata-v10-20261025.json','w'),ensure_ascii=False,indent=1)
print(json.dumps({k:v for k,v in summary.items() if k not in ('muestra_por_transporte',)},ensure_ascii=False,indent=1)[:3500])
