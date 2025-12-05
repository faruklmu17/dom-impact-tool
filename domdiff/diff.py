# domdiff/diff.py
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple


@dataclass
class DomChange:
    change_type: str          # "added", "removed", "modified"
    node_path: str            # like "html > body > form > button[0]"
    details: Dict[str, Any]   # attributes/text diffs


def _build_tree(soup: BeautifulSoup):
    """
    Build a flat list of (path, node) tuples for comparison.
    Path is a simple "tag[index]" style chain.
    """
    result = []

    def walk(node, path):
        # Only keep real element nodes (tag, not strings)
        if not hasattr(node, "name") or node.name is None:
            return

        # Count sibling index for same tag type
        parent = node.parent
        if parent:
            same_tag_siblings = [c for c in parent.children if getattr(c, "name", None) == node.name]
            idx = same_tag_siblings.index(node)
        else:
            idx = 0

        current_path = f"{path} > {node.name}[{idx}]" if path else f"{node.name}[{idx}]"
        result.append((current_path, node))

        for child in node.children:
            walk(child, current_path)

    walk(soup.body or soup, "")  # start at body if possible
    return result


def load_dom(path: str) -> List[Tuple[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return _build_tree(soup)


def diff_dom(old_path: str, new_path: str) -> List[DomChange]:
    old_nodes = load_dom(old_path)
    new_nodes = load_dom(new_path)

    old_map = {p: n for p, n in old_nodes}
    new_map = {p: n for p, n in new_nodes}

    changes: List[DomChange] = []

    # Detect removed and modified
    for path, old_node in old_map.items():
        if path not in new_map:
            changes.append(DomChange(
                change_type="removed",
                node_path=path,
                details={"tag": old_node.name, "attrs": dict(old_node.attrs)}
            ))
        else:
            new_node = new_map[path]
            old_attrs = dict(old_node.attrs)
            new_attrs = dict(new_node.attrs)
            if old_attrs != new_attrs:
                changes.append(DomChange(
                    change_type="modified",
                    node_path=path,
                    details={"old_attrs": old_attrs, "new_attrs": new_attrs}
                ))

    # Detect added
    for path, new_node in new_map.items():
        if path not in old_map:
            changes.append(DomChange(
                change_type="added",
                node_path=path,
                details={"tag": new_node.name, "attrs": dict(new_node.attrs)}
            ))

    return changes
