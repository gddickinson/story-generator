"""Web interface tests: every exported endpoint answers, the static build is complete, and the JS engine tests pass.

Run: python -m pytest -q tests/test_web.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from storygen.web.app import STATIC, STATIC_ENDPOINTS, app  # noqa: E402

client = TestClient(app)


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200 and "static/main.js" in r.text


@pytest.mark.parametrize("path", STATIC_ENDPOINTS)
def test_endpoint(path):
    r = client.get("/api" + path)
    assert r.status_code == 200, r.text
    assert r.json() is not None


def test_static_build(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert (tmp_path / "site" / "index.html").read_text().count("APP_STATIC") == 1
    for path in STATIC_ENDPOINTS:
        assert (tmp_path / "site" / "api" / (path.strip("/") + ".json")).exists()


def test_static_assets_referenced_exist():
    html = (STATIC / "index.html").read_text()
    for name in ("style.css", "main.js"):
        assert f"static/{name}" in html and (STATIC / name).exists()


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_js_engine():
    tests = sorted(STATIC.glob("*.test.mjs"))
    for t in tests:
        r = subprocess.run(["node", str(t)], capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr


# --- project-specific ------------------------------------------------------------------------------------------
import json  # noqa: E402
import math  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "stories.json"


def _close(a, b, path=""):
    """Equal structures, floats within rtol 1e-9 (libm and FMA differ between platforms in the last bits)."""
    if isinstance(a, float) or isinstance(b, float):
        assert math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12), path
    elif isinstance(a, dict):
        assert a.keys() == b.keys(), path
        for k in a:
            _close(a[k], b[k], f"{path}.{k}")
    elif isinstance(a, list):
        assert len(a) == len(b), path
        for i, (x, y) in enumerate(zip(a, b)):
            _close(x, y, f"{path}[{i}]")
    else:
        assert a == b, path


def test_fixture_is_current():
    sys.path.insert(0, str(ROOT / "scripts"))
    import make_story_fixture
    want = json.loads(FIXTURE.read_text())
    got = json.loads(json.dumps(make_story_fixture.build()))
    for k in ("numpy", "python"):
        got.pop(k), want.pop(k)
    _close(got, want)


def test_spec_matches_templates_file():
    spec = client.get("/api/spec").json()
    assert spec["templates"] == json.loads((ROOT / "data" / "templates.json").read_text())
    assert len(spec["characters"]) == 5 and len(spec["themes"]) == 6


def test_story_endpoint_matches_package():
    from storygen import NarrativeGenerator
    r = client.get("/api/story/42?branches=4").json()
    g = NarrativeGenerator(seed=42)
    g.initialize_world()
    g.generate_story_structure(num_branches=4)
    told = g.tell_story()
    assert r["title"] == told["title"]
    assert [e["text"] for e in r["events"]] == [v["text"] for v in told["events"].values()]
    assert len(r["relationships"]) == 10 and len(r["events"]) == 13
    assert [e["phase"] for e in r["events"][:4]] == ["introduction", "development", "climax", "resolution"]


@pytest.mark.parametrize("url", ["/api/story/-1", "/api/story/1?branches=0", "/api/story/1?branches=99"])
def test_story_endpoint_rejects_bad_input(url):
    assert client.get(url).status_code == 422


def test_info_counts():
    info = client.get("/api/info").json()
    assert info["templates"] == 16 and info["phases"] == 4 and info["locations"] == 5
