"""Built-site regression: run npm run build, then python3 -m unittest discover -s tests."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SLUGS = {"en": "rotterdam-chemo-rfs-en", "ja": "rotterdam-chemo-rfs", "zh": "rotterdam-chemo-rfs-zh"}
TAGS = ["biostatistics", "survival-analysis", "causal-inference", "overlap-weighting", "r"]


def cards(path):
    # Only HorizontalCard's outer link, not tag links or article language links.
    return re.findall(r'<a href="([^"]+)"[^>]*>\s*<div class="hero-content', path.read_text())


def pages(directory):
    return [directory / "index.html"] + sorted(directory.glob("[0-9]*/index.html"), key=lambda p: int(p.parent.name))


class LocaleListsTest(unittest.TestCase):
    def test_rotterdam_has_one_matching_translation_in_each_listing(self):
        for locale, slug in SLUGS.items():
            prefix = "" if locale == "en" else locale + "/"
            expected = f"/{prefix}blog/{slug}"
            root = DIST / prefix
            listings = {"blog (all pages)": pages(root / "blog"), "home latest notes": [root / "index.html"]}
            listings.update({"tag/" + tag: pages(root / "blog/tag" / tag) for tag in TAGS})
            for name, paths in listings.items():
                with self.subTest(locale=locale, listing=name):
                    links = [link for path in paths for link in cards(path)]
                    # Homepage also has a featured project card; inspect its final three note cards.
                    if name == "home latest notes":
                        links = links[-3:]
                    actual = [link for link in links if "rotterdam-chemo-rfs" in link]
                    self.assertEqual(actual, [expected])

    def test_legacy_posts_remain_across_pagination(self):
        legacy = {p.stem for p in (ROOT / "src/content/blog").glob("*.md") if not p.stem.startswith("rotterdam-chemo-rfs")}
        for locale, slug in SLUGS.items():
            prefix = "" if locale == "en" else locale + "/"
            with self.subTest(locale=locale):
                listing_pages = pages(DIST / prefix / "blog")
                all_cards = [cards(path) for path in listing_pages]
                links = [link for page in all_cards for link in page]
                self.assertEqual({link.rsplit("/", 1)[1] for link in links}, legacy | {slug})
                self.assertEqual(len(links), len(legacy) + 1)
                for page in all_cards[:-1]:
                    self.assertEqual(len(page), 10)
                for link in links:
                    self.assertTrue((DIST / link.lstrip("/") / "index.html").exists(), link)

    def test_existing_translation_urls_and_language_links_survive(self):
        for prefix in ["", "ja/", "zh/"]:
            for slug in SLUGS.values():
                with self.subTest(prefix=prefix, slug=slug):
                    html = (DIST / prefix / "blog" / slug / "index.html").read_text()
                    for locale, target in SLUGS.items():
                        target_prefix = "" if locale == "en" else locale + "/"
                        self.assertIn(f'href="/{target_prefix}blog/{target}"', html)


if __name__ == "__main__":
    unittest.main()
