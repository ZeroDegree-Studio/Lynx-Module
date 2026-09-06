"""Generate index.json for the Lynx-Module repository.

Scans packages/**/*.lmp, reads manifest.yaml from inside each package (zip),
and produces index.json with metadata for each module. Run by GitHub Actions
on every push to main, or locally with:

    python tools/generate_index.py

Output format consumed by the Lynx client module market (GitHubMarketAdapter):

    {
      "version": "1",
      "updated_at": "<ISO 8601 UTC>",
      "modules": [
        {
          "module_id": "...",
          "name": "...",
          "author": "...",
          "version": "...",
          "kind": "py-skill",
          "category": "...",
          "description": "...",
          "permissions": [...],
          "official": true,
          "license": "MIT",
          "size_bytes": 12345,
          "sha256": "...",
          "download_url": "packages/<id>/<id>-<version>.lmp"
        }
      ]
    }
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OFFICIAL_AUTHORS = ("lynx",)
INDEX_VERSION = "1"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_manifest_yaml(text: str) -> dict[str, Any] | None:
    """解析 manifest.yaml：优先 PyYAML，缺包时退回最小顶层键值解析（够索引用）。"""
    try:
        import yaml

        data = yaml.safe_load(text) or {}
        return data if isinstance(data, dict) else None
    except ImportError:
        pass
    except Exception as e:  # noqa: BLE001
        print(f"  ! YAML 解析失败: {e}", file=sys.stderr)
        return None
    # 最小兜底：只取顶层 `key: value`（manifest 必需字段都是平的）
    data: dict[str, Any] = {}
    for line in text.splitlines():
        if not line or line[:1] in (" ", "\t", "#") or ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        if not k:
            continue
        if v == "[]":
            data[k] = []
        elif v.startswith("[") and v.endswith("]"):
            import re as _re

            pairs = _re.findall(r'"([^"]*)"|\'([^\']*)\'', v)
            data[k] = [a or b for a, b in pairs]
        else:
            data[k] = v.strip("'\"")
    return data or None


def _read_manifest_from_lmp(lmp_path: Path) -> dict[str, Any] | None:
    """Read manifest.yaml from inside a .lmp (zip) package. None on failure."""
    try:
        with zipfile.ZipFile(lmp_path) as z:
            names = z.namelist()
            target = "manifest.yaml" if "manifest.yaml" in names else None
            if target is None:
                # 包内容可能带顶层目录：<id>/manifest.yaml
                for n in names:
                    if n.endswith("/manifest.yaml") and n.count("/") == 1:
                        target = n
                        break
            if target is None:
                print(f"  ! SKIP {lmp_path.name}: no manifest.yaml inside", file=sys.stderr)
                return None
            return _parse_manifest_yaml(z.read(target).decode("utf-8"))
    except (OSError, zipfile.BadZipFile) as e:
        print(f"  ! ERROR reading {lmp_path}: {e}", file=sys.stderr)
        return None


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_metadata(lmp_path: Path) -> dict[str, Any] | None:
    """Parse one .lmp and return its index entry, or None on failure."""
    mf = _read_manifest_from_lmp(lmp_path)
    if mf is None:
        return None

    module_id = str(mf.get("id", "")).strip()
    name = str(mf.get("name", "")).strip()
    version = str(mf.get("version", "")).strip()
    if not module_id or not name or not version:
        print(f"  ! SKIP {lmp_path.name}: missing required manifest field "
              f"(id/name/version)", file=sys.stderr)
        return None

    author = str(mf.get("author", "")).strip()
    rel = lmp_path.relative_to(lmp_path.parents[2]).as_posix()

    return {
        "module_id": module_id,
        "name": name,
        "author": author,
        "version": version,
        "kind": mf.get("kind", ""),
        "category": mf.get("category", ""),
        "description": mf.get("description", ""),
        "permissions": mf.get("permissions", []),
        "official": author.lower() in OFFICIAL_AUTHORS if author else False,
        "license": mf.get("license", "MIT"),
        "size_bytes": lmp_path.stat().st_size,
        "sha256": _sha256_file(lmp_path),
        "download_url": rel,
    }


def generate_index(repo_root: Path) -> dict[str, Any]:
    """Scan <repo_root>/packages/ and build the index structure."""
    packages_dir = repo_root / "packages"
    entries: list[dict[str, Any]] = []

    if packages_dir.exists():
        for lmp in sorted(packages_dir.rglob("*.lmp")):
            if any(part.startswith("_") for part in lmp.parts):
                continue  # 跳过草稿目录（packages/_drafts/ 等）
            print(f"  + {lmp.relative_to(repo_root).as_posix()}")
            entry = extract_metadata(lmp)
            if entry is not None:
                entries.append(entry)
    else:
        print(f"  ! packages/ directory not found at {packages_dir}", file=sys.stderr)

    return {
        "version": INDEX_VERSION,
        "updated_at": _now_iso(),
        "modules": entries,
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    print(f"Scanning {repo_root / 'packages'} ...")
    index = generate_index(repo_root)
    out_path = repo_root / "index.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {out_path}")
    print(f"  modules indexed: {len(index['modules'])}")
    print(f"  updated_at: {index['updated_at']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
