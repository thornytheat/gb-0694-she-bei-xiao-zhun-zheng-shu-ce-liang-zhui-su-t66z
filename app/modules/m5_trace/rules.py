from app.domain import trace,coverage,coverage_label
def apply(ctx):
    chains={};rows=[]
    for key in sorted(ctx['certs']):
        outcome=trace(key,ctx['certs'])
        # A metadata conflict in any ancestor breaks the proof chain.
        if any(ctx['certs'].get(node,{}).get('conflicted') for node in outcome['path']):outcome['valid']=False;outcome['code']='REFERENCE_CONFLICT'
        cov=coverage(outcome['path'],ctx['certs']);cov['label']=coverage_label(cov);outcome['coverage']=cov;chains[key]=outcome
        own=ctx['certs'][key]
        rows.append({'证书':key,'溯源路径':' → '.join(outcome['path']),'声明量程_V':own['min_v']+'~'+own['max_v'],'有效量程_V':cov['label'],'收窄级':','.join(cov['narrowed_by']) or '—','原因码':outcome['code'],'状态':'可追溯' if outcome['valid'] else '中断'})
    ctx['chains']=chains
    return {'rows':rows,'metrics':[['可追溯',sum(r['valid'] for r in chains.values()),'份'],['中断',sum(not r['valid'] for r in chains.values()),'份'],['量程收窄',sum(bool(r['coverage']['narrowed_by']) for r in chains.values()),'份']]}
