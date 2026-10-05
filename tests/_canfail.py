"""Can-fail proof for tests/test_erlang_c.py.

A test suite that has only ever passed is not evidence. This mutates the suite
four ways and asserts each mutation makes it fail, then restores the file.

Run:  python _canfail.py
"""

import pathlib
import subprocess
import sys

TARGET = pathlib.Path(__file__).with_name("test_erlang_c.py")

MUTATIONS = {
    "reference recursion index pinned to N":
        ("b = (a * b) / (i + a * b)", "b = (a * b) / (n + a * b)"),
    "required_agents expected 14 -> 15":
        ('assert result["required_agents"] == 14',
         'assert result["required_agents"] == 15'),
    "service-level reference 86.70 -> 84.0":
        ("86.70, abs=5e-3", "84.0, abs=5e-3"),
    "ceiling test neutered (no raise expected)":
        ("    with pytest.raises(ValueError) as excinfo:\n"
         "        ErlangCCalculator.erlang_c(agents, intensity)\n"
         "    assert \"range error\" in str(excinfo.value), excinfo.value",
         "    ErlangCCalculator.erlang_c(agents, intensity)\n"
         "    assert True"),
    "ASL reference 10.09 -> 12.0":
        ("10.09, abs=5e-3", "12.0, abs=5e-3"),
}


def run() -> int:
    original = TARGET.read_text(encoding="utf-8")
    print(f"can-fail proof for {TARGET.name}")
    print("=" * 66)

    baseline = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header"],
        capture_output=True, text=True)
    print(f"  {'baseline (unmutated)':<44} "
          f"{'green' if baseline.returncode == 0 else 'RED'}")
    if baseline.returncode != 0:
        print("  baseline is not green; fix that before trusting this")
        return 1

    failures = 0
    try:
        for name, (anchor, replacement) in MUTATIONS.items():
            if anchor not in original:
                print(f"  {name:<44} SKIP (anchor not found)")
                continue
            TARGET.write_text(original.replace(anchor, replacement),
                              encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "--no-header"],
                capture_output=True, text=True)
            if result.returncode != 0:
                tail = [ln for ln in result.stdout.splitlines()
                        if " failed" in ln or " failed," in ln]
                detail = tail[0].strip() if tail else "failed"
                print(f"  {name:<44} fails as intended ({detail})")
            else:
                print(f"  {name:<44} *** DID NOT FAIL ***")
                failures += 1
    finally:
        TARGET.write_text(original, encoding="utf-8")

    print("=" * 66)
    print(f"{len(MUTATIONS) - failures} of {len(MUTATIONS)} mutations detected")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(run())