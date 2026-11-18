import pytest
from app.config import SAMPLE
from app.pipeline import calculate
NARROWED_CSV = """cert,device,alias,parent,valid_from,valid_to,minimum,maximum,unit,revoked,measured_at,value,measure_unit,version
ROOT,REF-001,标准源,,2025-01-01,2028-01-01,0,8,V,no,2026-06-01,5,V,1
C1,D1,仪器1,ROOT,2026-01-01,2027-01-01,0,10,V,no,2026-06-01,5,V,1
C2,D2,仪器2,ROOT,2026-01-01,2027-01-01,0,10,V,no,2026-06-01,9,V,1
C3,D3,仪器3,ROOT,2026-01-01,2027-01-01,0,10,V,no,2026-06-01,11,V,1
MID,REF-002,中间标准,ROOT,2026-01-01,2027-01-01,0,9,V,no,2026-06-01,5,V,1
G1,D4,仪器4,MID,2026-01-01,2027-01-01,0,10,V,no,2026-06-01,8.5,V,1
G2,D5,仪器5,MID,2026-01-01,2027-01-01,0,10,V,no,2026-06-01,7,V,1
OFF,REF-003,偏移标准,ROOT,2026-01-01,2027-01-01,20,30,V,no,2026-06-01,25,V,1
"""
@pytest.fixture
def raw(): return SAMPLE.read_text(encoding='utf-8-sig')
@pytest.fixture
def ctx(): return calculate()
@pytest.fixture
def narrowed_csv(): return NARROWED_CSV
@pytest.fixture
def narrowed(): return calculate(NARROWED_CSV)
@pytest.fixture
def client(tmp_path,monkeypatch):
    monkeypatch.setenv('APP_DB',str(tmp_path/'db.sqlite3'))
    from app.main import app
    app.config['TESTING']=True
    return app.test_client()
