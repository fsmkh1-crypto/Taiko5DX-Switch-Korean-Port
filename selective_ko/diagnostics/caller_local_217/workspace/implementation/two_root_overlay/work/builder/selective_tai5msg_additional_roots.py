"""Explicit local output profile; preserves the historical V357 serializer.

Returns in-memory bytes and bounded evidence, never a product acceptance result.
"""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from builder import selective_tai5msg as codec

PROFILE = 'V357_PLUS_EXACT_ROOTS_181_307_V1'
ADMISSION_PATH = Path('selective_ko/artifacts/tai5msg_b0_additional_roots_181_307_v1/ADMISSION.json')
ADMISSION_SIZE = 967
ADMISSION_SHA256 = 'b076c74d4074b8ea2395f33c757c90dca31a78739ccaa4c8dbccc316fb6965d0'
LOCATORS = frozenset({(0, 181), (0, 307)})


class AdditionalRootError(RuntimeError):
    def __init__(self, code, detail):
        self.code = code
        super().__init__(f'{code}: {detail}')


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _require(condition, code, detail):
    if not condition:
        raise AdditionalRootError(code, detail)


def _load_admission(repo_root):
    data = (Path(repo_root) / ADMISSION_PATH).read_bytes()
    _require(len(data) == ADMISSION_SIZE and _sha(data) == ADMISSION_SHA256,
             'ADMISSION_IDENTITY', 'exact local admission required')
    obj = json.loads(data)
    _require(obj['schema'] == 'TAI5MSG_B0_ADDITIONAL_ROOTS_181_307_V1'
             and obj['profile'] == PROFILE, 'ADMISSION_PROFILE', 'profile mismatch')
    rows = obj['rows']
    locators = [(r['block'], r['local']) for r in rows]
    _require(len(rows) == 2 and len(set(locators)) == 2 and set(locators) == LOCATORS,
             'ADMISSION_MEMBERSHIP', 'only B0:181 and B0:307 permitted')
    return rows


def _check_collisions(repo_root):
    membership = codec.load_v303_membership(repo_root)
    families = {
        'V303': membership.locators,
        'V304': set(codec.load_v304_corrections(repo_root)),
        'V315': set(codec.load_v315_corrections(repo_root)),
        'V320': set(codec.load_v320_corrections(repo_root)),
        'V356': set(codec.load_v356_percent_macro_roots(repo_root)),
    }
    for family, locators in families.items():
        _require(not LOCATORS.intersection(locators), 'MUTATION_COLLISION', family)
    return membership, families


def _verify_extended(baseline_blob, output, targets, stock, selected, old_roots):
    baseline = codec.parse_tai5msg(baseline_blob)
    post = codec.parse_tai5msg(output)
    _require(len(output) == 1840393, 'OUTPUT_SIZE', 'extended size')
    _require(post.message_count == 14832, 'MESSAGE_COUNT', 'message census')
    b0 = post.blocks[0]
    _require((b0.used_end, b0.declared_size, b0.physical_filler_bytes) == (0xEA30, 0xEA40, 16),
             'B0_STRUCTURE', 'used/declared/filler')
    _require(post.blocks[32].file_offset == 0x1B4AC0, 'B32_OFFSET', 'extended offset')
    counts = {'new_roots': 0, 'historical_selected': 0, 'historical_roots': 0, 'unselected': 0}
    changed = []
    for block, (old, new) in enumerate(zip(baseline.blocks, post.blocks)):
        _require(len(old.messages) == len(new.messages), 'BLOCK_COUNT', str(block))
        _require(new.declared_size <= codec.RUNTIME_BLOCK_CAPACITY, 'CAPACITY', str(block))
        if block:
            _require(new.file_offset == old.file_offset + 64, 'BLOCK_OFFSET', str(block))
            _require(output[new.file_offset:new.file_offset + new.physical_size]
                     == baseline_blob[old.file_offset:old.file_offset + old.physical_size],
                     'UNRELATED_BLOCK_BYTES', str(block))
        for local, (before, after) in enumerate(zip(old.messages, new.messages)):
            loc = (block, local)
            if before != after:
                changed.append(loc)
            if loc in LOCATORS:
                _require(after == targets[loc], 'NEW_ROOT_VALUE', str(loc))
                counts['new_roots'] += 1
            else:
                _require(after == before, 'UNRELATED_MESSAGE', str(loc))
                if loc in selected:
                    counts['historical_selected'] += 1
                elif loc in old_roots:
                    counts['historical_roots'] += 1
                else:
                    _require(after == stock.blocks[block].messages[local], 'UNSELECTED_SOURCE', str(loc))
                    counts['unselected'] += 1
    _require(set(changed) == LOCATORS, 'CHANGED_LOCATORS', str(changed))
    _require(counts == {'new_roots': 2, 'historical_selected': 3179,
                        'historical_roots': 46, 'unselected': 11605}, 'OUTPUT_ACCOUNTING', str(counts))
    return counts


def reconstruct_with_additional_roots(stock_blob, pc_ko_blob, repo_root, mapping_codes, *, profile):
    """Rebuild authenticated V357 in memory, then apply only two exact roots.

    No caller-supplied baseline, raw replacement buffer or arbitrary profile is accepted.
    Existing reconstruct_selective_tai5msg remains unchanged and defaults to V357.
    """
    _require(profile == PROFILE, 'OUTPUT_PROFILE', 'explicit extended profile required')
    for label, data, size, digest in (
        ('SOURCE', stock_blob, codec.STOCK_SIZE, codec.STOCK_SHA256),
        ('PC_KO', pc_ko_blob, codec.PC_KO_SIZE, codec.PC_KO_SHA256),
    ):
        _require(type(data) is bytes and len(data) == size and _sha(data) == digest,
                 label + '_IDENTITY', 'canonical whole-file input required')
    rows = _load_admission(repo_root)
    membership, families = _check_collisions(repo_root)
    stock = codec.parse_tai5msg(stock_blob)
    pc = codec.parse_tai5msg(pc_ko_blob)
    targets = {}
    for row in rows:
        loc = (row['block'], row['local'])
        source = stock.blocks[loc[0]].messages[loc[1]]
        target = pc.blocks[loc[0]].messages[loc[1]]
        _require(len(source) == row['source_length'] and _sha(source) == row['source_sha256'],
                 'MESSAGE_SOURCE_IDENTITY', str(loc))
        _require(len(target) == row['target_length'] and _sha(target) == row['target_sha256'],
                 'MESSAGE_TARGET_IDENTITY', str(loc))
        _require(source != target and len(target) - len(source) == row['delta'], 'MESSAGE_DELTA', str(loc))
        targets[loc] = target
    baseline_blob, baseline_report = codec.reconstruct_selective_tai5msg(
        stock_blob, pc_ko_blob, Path(repo_root), mapping_codes, require_diagnostic_sha=True)
    _require(_sha(baseline_blob) == codec.EXPECTED_DIAGNOSTIC_SHA256, 'BASELINE_IDENTITY', 'V357 required')
    baseline = codec.parse_tai5msg(baseline_blob)
    messages = [list(b.messages) for b in baseline.blocks]
    for (block, local), target in targets.items():
        _require(messages[block][local] == stock.blocks[block].messages[local], 'BASELINE_ROOT_SOURCE', str(local))
        messages[block][local] = target
    output, _ = codec._serialize_from_messages(baseline, messages)
    counts = _verify_extended(baseline_blob, output, targets, stock, membership.locators, families['V356'])
    return output, {
        'profile': PROFILE, 'product_accepted': False, 'stage': 'V371_PARTIAL_BLOCKED',
        'admission_sha256': ADMISSION_SHA256, 'baseline_sha256': _sha(baseline_blob),
        'source_sha256': _sha(stock_blob), 'pc_ko_sha256': _sha(pc_ko_blob),
        'output_size': len(output), 'output_sha256': _sha(output),
        'code_sha256': _sha(Path(__file__).read_bytes()),
        'serializer_code_sha256': _sha(Path(codec.__file__).read_bytes()),
        'changed_locators': [[0,181],[0,307]], 'counts': counts,
        'historical_report': asdict(baseline_report),
        'consumer_evidence': 'NOT_EXECUTED; no V371 obligation catalog change',
    }
