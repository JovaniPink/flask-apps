#!/usr/bin/env python3
"""Reject mutable container and browser dependency references."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DIGEST = re.compile(r"@sha256:[0-9a-f]{64}(?:\s|\"|$)")
SCRIPT = re.compile(r"<script\b[^>]*\bsrc=\"(https://[^\"]+)\"[^>]*></script>")
TEMPLATES = (
    ROOT / "flask-bootstrap/app/templates/global.html",
    ROOT / "flask-bootstrap/app/templates/layout.html",
    ROOT / "flask-bootstrap/app/templates/user.html",
)
EXPECTED_SCRIPTS = {
    "https://code.jquery.com/jquery-3.7.1.min.js",
    "https://cdn.jsdelivr.net/npm/highcharts@12.4.0/highcharts.js",
    "https://cdn.jsdelivr.net/npm/highcharts@12.4.0/modules/exporting.js",
    "https://cdn.jsdelivr.net/npm/highcharts@12.4.0/modules/export-data.js",
}


def main() -> None:
    mutable_images = []
    for dockerfile in ROOT.rglob("Dockerfile"):
        for line_number, line in enumerate(dockerfile.read_text().splitlines(), 1):
            if line.startswith("FROM ") and not DIGEST.search(line):
                mutable_images.append(f"{dockerfile.relative_to(ROOT)}:{line_number}")
    for compose in ROOT.rglob("docker-compose*.yml"):
        for line_number, line in enumerate(compose.read_text().splitlines(), 1):
            if re.match(r"\s*image:", line) and not DIGEST.search(line):
                mutable_images.append(f"{compose.relative_to(ROOT)}:{line_number}")
    if mutable_images:
        raise SystemExit("mutable container references: " + ", ".join(mutable_images))

    observed = set()
    for template in TEMPLATES:
        source = template.read_text()
        tags = SCRIPT.findall(source)
        if set(tags) != EXPECTED_SCRIPTS:
            raise SystemExit(f"unexpected external scripts in {template.relative_to(ROOT)}")
        for tag in re.findall(r"<script\b[^>]*\bsrc=\"https://[^>]+></script>", source):
            if not re.search(r'\bintegrity="sha384-[A-Za-z0-9+/=]+"', tag):
                raise SystemExit(f"missing SHA-384 integrity in {template.relative_to(ROOT)}")
            if 'crossorigin="anonymous"' not in tag:
                raise SystemExit(f"missing anonymous CORS in {template.relative_to(ROOT)}")
        observed.update(tags)

    if observed != EXPECTED_SCRIPTS:
        raise SystemExit("browser dependency allowlist is incomplete")

    print("Container digests and external browser script integrity contracts passed.")


if __name__ == "__main__":
    main()
