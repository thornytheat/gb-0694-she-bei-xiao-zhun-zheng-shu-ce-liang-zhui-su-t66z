def test_measurement_conservation(ctx):assert ctx['balanced'] is True
def test_bad_certificate_rejected(ctx):assert next(r for r in ctx['verdicts'] if r['证书']=='C0002')['结论']=='拒用'
def test_good_certificate_accepted(ctx):assert next(r for r in ctx['verdicts'] if r['证书']=='C0001')['结论']=='可采用'
def test_out_of_range_reason(ctx):assert 'OUT_OF_RANGE' in next(r for r in ctx['verdicts'] if r['证书']=='C0007')['原因码']
def test_expired_reason(ctx):assert next(r for r in ctx['verdicts'] if r['证书']=='END')['原因码']=='INVALID_WINDOW'
def test_verdict_source_lines(ctx):assert all(r['行号']>=2 for r in ctx['verdicts'])
def test_partition(ctx):assert sum(r['结论']=='可采用' for r in ctx['verdicts'])+sum(r['结论']=='拒用' for r in ctx['verdicts'])==42
def verdict(ctx,cert):return next(r for r in ctx['verdicts'] if r['证书']==cert)
def test_within_narrowed_coverage_kept(narrowed):assert verdict(narrowed,'C1')['结论']=='可采用' # TRAP-26
def test_beyond_superior_coverage_rejected(narrowed):
    r=verdict(narrowed,'C2');assert r['结论']=='拒用' and 'OUT_OF_COVERAGE' in r['原因码']
def test_own_range_reason_not_confused_with_coverage(narrowed):
    r=verdict(narrowed,'C3');assert 'OUT_OF_RANGE' in r['原因码'] and 'OUT_OF_COVERAGE' not in r['原因码']
def test_multilevel_narrowing_rejected(narrowed):assert 'OUT_OF_COVERAGE' in verdict(narrowed,'G1')['原因码']
def test_within_multilevel_coverage_kept(narrowed):assert verdict(narrowed,'G2')['结论']=='可采用'
def test_empty_coverage_rejected(narrowed):assert 'OUT_OF_COVERAGE' in verdict(narrowed,'OFF')['原因码']
def test_verdict_row_shows_effective_range(narrowed):assert verdict(narrowed,'C2')['有效量程_V']=='0~8'
def test_upstream_range_change_recomputes_verdicts(narrowed_csv):
    from app.pipeline import calculate
    before=calculate(narrowed_csv.replace('2028-01-01,0,8,V','2028-01-01,0,1000,V'));after=calculate(narrowed_csv)
    assert verdict(before,'C2')['结论']=='可采用' and verdict(after,'C2')['结论']=='拒用'
    assert before['manifest']['run_id']!=after['manifest']['run_id']

