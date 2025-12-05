# cli.py
import argparse
from domdiff.impact import analyze_impact
from domdiff.diff import diff_dom


def main():
    parser = argparse.ArgumentParser(description="DOM diff and test impact analyzer")
    parser.add_argument("--old", required=True, help="Path to old DOM snapshot (HTML)")
    parser.add_argument("--new", required=True, help="Path to new DOM snapshot (HTML)")
    parser.add_argument("--selectors", required=True, help="Path to selectors.json")
    args = parser.parse_args()

    print("=== DOM CHANGES ===")
    changes = diff_dom(args.old, args.new)
    for ch in changes:
        print(f"[{ch.change_type.upper()}] {ch.node_path} -> {ch.details}")

    print("\n=== IMPACTED TESTS ===")
    impacted = analyze_impact(args.old, args.new, args.selectors)
    if not impacted:
        print("No impacted tests detected (with current naive logic).")
    else:
        for test_name, issues in impacted.items():
            print(f"\nTest: {test_name}")
            for issue in issues:
                print(f"  - Selector: {issue['selector']}")
                print(f"    Change: {issue['change_type']} at {issue['node_path']}")
                print(f"    Details: {issue['details']}")

if __name__ == "__main__":
    main()
