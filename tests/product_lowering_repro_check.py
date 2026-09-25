from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from builder.product_lowering_candidate import build, EXPECTED_TAI_SHA256, EXPECTED_IPS_SHA256, BUILD_ID


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    p=argparse.ArgumentParser(description="Run the product-lowering builder twice and require deterministic exact outputs.")
    p.add_argument('--baseline-tai',required=True,type=Path)
    p.add_argument('--baseline-ips',required=True,type=Path)
    p.add_argument('--plan-dir',required=True,type=Path)
    a=p.parse_args()
    with tempfile.TemporaryDirectory() as t:
        t=Path(t)
        run1=t/'run1'; run2=t/'run2'
        run1.mkdir(); run2.mkdir()
        r1=build(a.baseline_tai,a.baseline_ips,a.plan_dir,run1)
        r2=build(a.baseline_tai,a.baseline_ips,a.plan_dir,run2)
        tai1=run1/'romfs/TAI5MSG_JP.DAT'; tai2=run2/'romfs/TAI5MSG_JP.DAT'
        ips1=run1/f'exefs/{BUILD_ID}.ips'; ips2=run2/f'exefs/{BUILD_ID}.ips'
        assert tai1.read_bytes()==tai2.read_bytes()
        assert ips1.read_bytes()==ips2.read_bytes()
        assert sha(tai1)==EXPECTED_TAI_SHA256
        assert sha(ips1)==EXPECTED_IPS_SHA256
        assert r1==r2
    print('PASS_REPRODUCIBLE_TWO_RUNS')

if __name__=='__main__':
    main()
