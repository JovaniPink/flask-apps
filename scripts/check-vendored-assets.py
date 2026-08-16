#!/usr/bin/env python3
"""Validate that the flag bundle contains runtime assets, not build tooling."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "flask-bootstrap/app/static/css/flag-icon-css"
TOOLTIP_BUNDLE = ROOT / "flask-bootstrap/app/static/js/@coreui/plugin-chartjs-custom-tooltips"
REQUIRED_FILES = (
    BUNDLE / "LICENSE",
    BUNDLE / "README.md",
    BUNDLE / "css/flag-icon.css",
    BUNDLE / "css/flag-icon.min.css",
    TOOLTIP_BUNDLE / "README.md",
    TOOLTIP_BUNDLE / "js/custom-tooltips.js",
)
FORBIDDEN_PATHS = (
    ".editorconfig",
    "Gruntfile.coffee",
    "assets",
    "bower.json",
    "composer.json",
    "index.html",
    "less",
    "package.json",
    "sass",
    "svgo.yaml",
    "yarn.lock",
)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        raise SystemExit("missing vendored runtime assets: " + ", ".join(missing))

    forbidden = []
    for name in FORBIDDEN_PATHS:
        path = BUNDLE / name
        if path.is_file() or path.is_symlink() or (path.is_dir() and any(path.rglob("*"))):
            forbidden.append(name)
    if forbidden:
        raise SystemExit("vendored build tooling must stay removed: " + ", ".join(forbidden))

    if (TOOLTIP_BUNDLE / "package.json").exists():
        raise SystemExit("the unused CoreUI tooltip package build graph must stay removed")

    for ratio in ("1x1", "4x3"):
        flags = tuple((BUNDLE / "flags" / ratio).glob("*.svg"))
        if len(flags) != 256:
            raise SystemExit(f"expected 256 {ratio} flag assets; found {len(flags)}")

    print("Vendored browser bundles retain runtime assets and attribution without build graphs.")


if __name__ == "__main__":
    main()
