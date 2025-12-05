# domdiff/impact.py
import json
from typing import Dict, List
from bs4 import BeautifulSoup

from .diff import diff_dom, DomChange


def _load_html(path: str) -> BeautifulSoup:
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


def _selector_matches_change(selector: str, change: DomChange, new_html: BeautifulSoup) -> bool:
    """
    Very naive: if selector no longer finds anything in new HTML,
    but did in old HTML (we assume), we treat it as impacted when
    it is related to the changed node's attributes.
    """
    # For now, just try to use CSS selector directly
    try:
        matches = new_html.select(selector)
    except Exception:
        # Unsupported selector syntax for now
        return False

    if matches:
        return False  # still matches something → we treat as not broken

    # If no matches in new HTML, and this change modified or removed a node,
    # we treat it as potentially impacted.
    return change.change_type in ("removed", "modified")


def analyze_impact(
    old_dom_path: str,
    new_dom_path: str,
    selectors_json_path: str
) -> Dict[str, List[Dict]]:
    """
    Returns: { test_name: [ {selector, impact, reason}, ... ] }
    """
    changes = diff_dom(old_dom_path, new_dom_path)
    new_html = _load_html(new_dom_path)

    with open(selectors_json_path, "r", encoding="utf-8") as f:
        selectors_map = json.load(f)

    impacted: Dict[str, List[Dict]] = {}

    for test_name, selectors in selectors_map.items():
        for sel in selectors:
            for change in changes:
                if _selector_matches_change(sel, change, new_html):
                    impacted.setdefault(test_name, []).append({
                        "selector": sel,
                        "change_type": change.change_type,
                        "node_path": change.node_path,
                        "details": change.details
                    })

    return impacted
