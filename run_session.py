import argparse
from pathlib import Path

from web_interaction.browser_driver import PlaywrightBrowserDriver
from web_interaction.crawler import crawl_site


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a web interaction session and capture screenshots, DOM, and metadata.",
    )
    parser.add_argument("--url", required=True, help="Starting URL to visit.")
    parser.add_argument(
        "--depth",
        type=int,
        default=1,
        help="Interaction depth (affects number of navigation actions).",
    )
    parser.add_argument("--out", required=True, help="Output directory for captures.")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with PlaywrightBrowserDriver(headless=True) as driver:
        captures = crawl_site(url=args.url, depth=args.depth, out_dir=out_dir, driver=driver)

    print(f"Created {len(captures)} captures in {out_dir}")


if __name__ == "__main__":
    main()
