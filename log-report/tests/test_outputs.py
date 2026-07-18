import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected():
    """Independently recompute the expected report from the fixed input log."""
    paths, ips, total = Counter(), set(), 0
    for line in LOG_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
        if m:
            paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def test_report_exists_and_valid_json():
    """Success criterion 1: /app/report.json exists and contains valid JSON."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    json.loads(REPORT_PATH.read_text())  # raises if not valid JSON


def test_total_requests():
    """Success criterion 2: total_requests equals the number of non-empty log lines."""
    report = json.loads(REPORT_PATH.read_text())
    assert report.get("total_requests") == _expected()["total_requests"]


def test_unique_ips():
    """Success criterion 3: unique_ips equals the number of distinct client IPs."""
    report = json.loads(REPORT_PATH.read_text())
    assert report.get("unique_ips") == _expected()["unique_ips"]


def test_top_path():
    """Success criterion 4: top_path equals the most frequently requested path (tie-break: first occurrence)."""
    report = json.loads(REPORT_PATH.read_text())
    assert report.get("top_path") == _expected()["top_path"]
