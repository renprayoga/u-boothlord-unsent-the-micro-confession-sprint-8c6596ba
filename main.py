"""Unsent: The Micro-Confession Sprint — entry writer.

Chosen confession (131 characters total, two lines):

    To: my old mentor
    I still keep the thank-you draft from the night I quit — I was too
    proud to send it, and now too late to mean it.

Why this confession wins (judge rubric order: two-part form, felt reason
it stayed unsent, To: and message need each other, reads as typed never
sent, one line as typed):

- Two-part form: a To: line naming a relationship ("my old mentor", no
  real full name or handle) plus the unsent message itself, one line.
- Felt reason: the draft stayed unsent out of pride, and now it is too
  late — the reason is felt in the words ("too proud", "too late"),
  never stated as an explanation after the message.
- To: and message need each other: the thank-you draft only makes sense
  addressed to the mentor from the night the writer quit; swapping the
  addressee (a friend, an ex, a boss) breaks the confession.
- Reads as typed, never sent: a kept draft, an unfinished thank-you, a
  small regret — not a joke, greeting, or motivational line.
- Specific and honest: a concrete object (the draft), a concrete night
  (the night I quit), a concrete feeling (pride curdling into lateness).

Program: writes the confession to /output/entry.txt, then validates its
own output — UTF-8 text, 1-260 characters total, exactly two lines, the
message line at most 200 characters, not only whitespace — and exits
non-zero if the gate would fail. Deterministic: the confession is a
constant, no input, no network, no randomness, Python 3 stdlib only.
"""

import os
import sys

ENTRY = (
    "To: my old mentor\n"
    "I still keep the thank-you draft from the night I quit \u2014 I was too "
    "proud to send it, and now too late to mean it."
)

DESTINATION = "/output/entry.txt"
MIN_LEN = 1
MAX_LEN = 260
MAX_MESSAGE_LEN = 200


def _fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return -1


def _save() -> None:
    folder = os.path.dirname(DESTINATION)
    os.makedirs(folder, exist_ok=True)
    with open(DESTINATION, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY + "\n")


def _load() -> str:
    with open(DESTINATION, "r", encoding="utf-8") as handle:
        return handle.read()


def _check(written: str) -> int:
    entry = written.rstrip("\n")
    if not MIN_LEN <= len(entry) <= MAX_LEN:
        return _fail(f"entry is {len(entry)} characters (need 1-260)")
    lines = entry.split("\n")
    if len(lines) != 2:
        return _fail(f"entry has {len(lines)} lines (need exactly 2)")
    if not lines[0].startswith("To: "):
        return _fail("first line is not a To: line")
    if len(lines[1]) > MAX_MESSAGE_LEN:
        return _fail(
            f"message line is {len(lines[1])} characters (max 200)"
        )
    if not entry.strip():
        return _fail("entry is only whitespace")
    if any(line != line.rstrip() for line in entry.split("\n")):
        return _fail("entry line has trailing whitespace")
    if entry != ENTRY:
        return _fail("written entry differs from the intended confession")
    # The gate reads the whole file: exactly one trailing newline, so the
    # file holds two lines and nothing else — no blank third line.
    if written != ENTRY + "\n":
        return _fail("written file is not exactly the entry plus one newline")
    return len(entry)


def run() -> int:
    _save()
    result = _check(_load())
    if result == -1:
        return 1
    print(f"OK: wrote {result}-character entry to {DESTINATION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
