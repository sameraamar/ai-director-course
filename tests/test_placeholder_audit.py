import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = REPO_ROOT / "course"
PLACEHOLDER_PATTERN = re.compile(r"YOUR TASK:|📷", re.IGNORECASE)


class PlaceholderAuditTests(unittest.TestCase):
    def test_report_remaining_screenshot_placeholders(self) -> None:
        matches: list[str] = []

        for markdown_file in sorted(COURSE_DIR.rglob("*.md")):
            lines = markdown_file.read_text(encoding="utf-8").splitlines()
            for line_number, line in enumerate(lines, start=1):
                if PLACEHOLDER_PATTERN.search(line):
                    relative_path = markdown_file.relative_to(REPO_ROOT).as_posix()
                    matches.append(f"{relative_path}:{line_number}: {line.strip()}")

        if matches:
            self.fail("Remaining screenshot/content placeholders found:\n- " + "\n- ".join(matches))


if __name__ == "__main__":
    unittest.main()