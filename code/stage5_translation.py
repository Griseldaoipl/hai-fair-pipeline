"""Stage 5 - Bilingual translation.

Loads the translation dictionaries (translation_maps.py) applied to convert the
Chinese categorical values to English, and reports the domain/entry inventory.
Verifies each domain is a non-empty mapping with string values and no blank
targets, so the applied vocabulary is auditable.

Source logic: scripts/translations.py + scripts/translation_maps.py (internal).
Portable: imports the sibling translation_maps module.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main():
    import translation_maps as tm
    domains = {name: obj for name, obj in vars(tm).items()
               if name.isupper() and isinstance(obj, dict)}
    if not domains:
        print("[stage5] ERROR: no translation domains found")
        return 1
    total = 0
    for name, mapping in sorted(domains.items()):
        if not mapping:
            print(f"[stage5] ERROR: domain {name} is empty")
            return 1
        for k, v in mapping.items():
            if not isinstance(v, str) or v.strip() == "":
                print(f"[stage5] ERROR: blank English target for {name}[{k!r}]")
                return 1
        total += len(mapping)
        print(f"[stage5] {name:20s} entries={len(mapping)}")
    print(f"[stage5] translation map OK: {len(domains)} domains, {total} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
