#!/usr/bin/env python3
"""Validate vendored browser assets and source snapshots without build tooling."""

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "flask-bootstrap/app/static/css/flag-icon-css"
TOOLTIP_BUNDLE = ROOT / "flask-bootstrap/app/static/js/@coreui/plugin-chartjs-custom-tooltips"
COREUI_BUNDLES = (
    ROOT / "flask-bootstrap/app/static/js/@coreui/coreui",
    ROOT / "flask-bootstrap/app/static/js/coreui",
)
PACE_BUNDLE = ROOT / "flask-bootstrap/app/static/js/pace-progress"
PERFECT_SCROLLBAR_BUNDLE = ROOT / "flask-bootstrap/app/static/js/perfect-scrollbar"
POPPER_BUNDLE = ROOT / "flask-bootstrap/app/static/js/popper.js"
COREUI_REQUIRED_FILES = tuple(
    bundle / relative
    for bundle in COREUI_BUNDLES
    for relative in ("LICENSE", "README.md", "js/src/index.js", "scss/coreui.scss")
)
REQUIRED_FILES = (
    BUNDLE / "LICENSE",
    BUNDLE / "README.md",
    BUNDLE / "css/flag-icon.css",
    BUNDLE / "css/flag-icon.min.css",
    TOOLTIP_BUNDLE / "README.md",
    TOOLTIP_BUNDLE / "js/custom-tooltips.js",
    PACE_BUNDLE / "LICENSE",
    PACE_BUNDLE / "README.md",
    PACE_BUNDLE / "pace.js",
    PACE_BUNDLE / "pace.min.js",
    PERFECT_SCROLLBAR_BUNDLE / "LICENSE",
    PERFECT_SCROLLBAR_BUNDLE / "README.md",
    PERFECT_SCROLLBAR_BUNDLE / "dist/perfect-scrollbar.min.js",
    COREUI_BUNDLES[0] / "dist/js/coreui.min.js",
) + COREUI_REQUIRED_FILES
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
COREUI_FORBIDDEN_FILES = (
    "package.json",
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pnpm-lock.yaml",
    "yarn.lock",
)
LEGACY_BUILD_FILES = (
    ".hsdoc",
    ".npmignore",
    "Gruntfile.coffee",
    "bower.json",
    "package.json",
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pnpm-lock.yaml",
    "yarn.lock",
)
EXPECTED_RUNTIME_HASHES = {
    PERFECT_SCROLLBAR_BUNDLE / "dist/perfect-scrollbar.min.js": (
        "9b237657ba86b4f520dcbe7af367b6b566b07e66385258442fd219a80d58629e"
    ),
    COREUI_BUNDLES[0] / "dist/js/coreui.min.js": (
        "14c42dffdf34c2d8dcaf36b9f5d97680d25cf859eba2da7b45e0e9c6f02d322d"
    ),
}


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

    for bundle in COREUI_BUNDLES:
        forbidden = [name for name in COREUI_FORBIDDEN_FILES if (bundle / name).exists()]
        if forbidden:
            relative = bundle.relative_to(ROOT)
            raise SystemExit(f"unused CoreUI build graph in {relative}: {', '.join(forbidden)}")

    for bundle in (PACE_BUNDLE, PERFECT_SCROLLBAR_BUNDLE):
        forbidden = [name for name in LEGACY_BUILD_FILES if (bundle / name).exists()]
        if forbidden:
            relative = bundle.relative_to(ROOT)
            raise SystemExit(f"legacy browser build graph in {relative}: {', '.join(forbidden)}")

    if POPPER_BUNDLE.exists():
        raise SystemExit("unused Popper metadata bundle must stay removed")

    for path, expected in EXPECTED_RUNTIME_HASHES.items():
        data = path.read_bytes()
        if not data.endswith(b"\n") or data.endswith(b"\n\n"):
            relative = path.relative_to(ROOT)
            raise SystemExit(f"vendored runtime must have one normalized trailing newline: {relative}")
        actual = hashlib.sha256(data.removesuffix(b"\n")).hexdigest()
        if actual != expected:
            relative = path.relative_to(ROOT)
            raise SystemExit(f"unexpected vendored runtime bytes in {relative}: {actual}")

    for ratio in ("1x1", "4x3"):
        flags = tuple((BUNDLE / "flags" / ratio).glob("*.svg"))
        if len(flags) != 256:
            raise SystemExit(f"expected 256 {ratio} flag assets; found {len(flags)}")

    print("Vendored browser bundles retain runtime assets and attribution without build graphs.")


if __name__ == "__main__":
    main()
