from app.domain import trace
def test_reference_cycle(ctx): # TRAP-20
    certs={'A':{**ctx['certs']['ROOT'],'parent':'B'},'B':{**ctx['certs']['ROOT'],'parent':'A'}};result=trace('A',certs);assert result['code']=='CYCLE' and result['path']==['A','B','A']
def test_revoked_chain(ctx):assert ctx['chains']['C0024']['code']=='REVOKED'
def test_root_trusted(ctx):assert ctx['chains']['ROOT']['valid'] is True
def test_missing_reference(ctx):assert trace('ABSENT',ctx['certs'])['code']=='MISSING_REFERENCE'
def test_conflicted_ancestor(ctx):assert ctx['chains']['C0022']['code']=='REFERENCE_CONFLICT'
def test_reference_expired(ctx):
    certs={'A':{**ctx['certs']['C0001'],'parent':'B'},'B':{**ctx['certs']['ROOT'],'valid_to':'2026-01-01'}};assert trace('A',certs)['code']=='REFERENCE_EXPIRED'
def test_chain_contains_parent(ctx):assert ctx['chains']['C0021']['path']==['C0021','C0001','ROOT']
def test_coverage_intersects_ancestors():
    from app.domain import coverage
    certs={'A':{'min_v':'0','max_v':'10'},'B':{'min_v':'2','max_v':'12'},'C':{'min_v':'3','max_v':'8'}}
    cov=coverage(['A','B','C'],certs);assert (str(cov['low']),str(cov['high']))==('3','8') and cov['narrowed_by']==['B','C']
def test_coverage_missing_reference_unknown(ctx):
    from app.domain import coverage
    assert coverage(['C0001','ABSENT'],ctx['certs'])['known'] is False
def test_chain_narrows_at_superior(narrowed): # TRAP-26
    cov=narrowed['chains']['C1']['coverage'];assert cov['narrowed_by']==['ROOT'] and cov['label']=='0~8'
def test_chain_narrows_at_each_level(narrowed):
    assert narrowed['chains']['G1']['coverage']['narrowed_by']==['MID','ROOT']
def test_disjoint_superior_range_empties_coverage(narrowed):
    cov=narrowed['chains']['OFF']['coverage'];assert cov['empty'] is True and cov['label']=='无覆盖'
def test_unnarrowed_chain_keeps_declared_range(narrowed):
    cov=narrowed['chains']['ROOT']['coverage'];assert cov['narrowed_by']==[] and cov['label']=='0~8'
def test_narrowing_level_in_stage_rows(narrowed):
    row=next(r for r in narrowed['stages']['5']['rows'] if r['证书']=='C1')
    assert row['收窄级']=='ROOT' and row['声明量程_V']=='0~10' and row['有效量程_V']=='0~8'
def test_narrowed_metric(narrowed):
    assert next(m for m in narrowed['stages']['5']['metrics'] if m[0]=='量程收窄')[1]==7

