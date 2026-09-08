#!/usr/bin/env python3
"""
An unbounded split absorbs whatever sits below the last record.

A text file holds records under repeated markdown headers. Code splits the file
on the header pattern so it can check one record at a time. A record's end is
never written down anywhere, it is defined only by where the next record starts,
so the last record has no next header to stop at and runs to end of file. It
swallows any trailing section (an archive, an appendix, a footer). A per-record
check then reads record-plus-tail and reports matches that belong to neither
record.

Nothing raises. Nothing warns. The exit status is zero. Only the answer is wrong.

    python3 split_demo.py                 the defect, side by side with the fix
    python3 split_demo.py --null-control  same file with the archive removed
"""

import re
import sys
from pathlib import Path

SPECIMEN = Path(__file__).resolve().parent / "records.md"

RECORD_HEADER = re.compile(r"(?m)^## (ITEM-\d+)[ \t]*$")   # a record starts here
ANY_HEADER = re.compile(r"(?m)^## ")                       # any header at the same depth
ARCHIVE_HEADER = "## Closed"                               # the trailing section
FIELDS = ["owner", "Status:"]                              # the two fields being looked for


def split_unclipped(text):
    """The bug. A record ends at the next RECORD header, or at end of file.

    The final record has no next record header, so its end is end of file and it
    absorbs the archive section below it.
    """
    pieces = []
    starts = list(RECORD_HEADER.finditer(text))
    for i, match in enumerate(starts):
        if i + 1 < len(starts):
            end = starts[i + 1].start()
        else:
            end = len(text)                     # <- the bug lives on this line
        pieces.append((match.group(1), text[match.start():end]))
    return pieces


def split_clipped(text):
    """The fix. A record ends at the next header of the SAME DEPTH, whatever it says.

    The archive header is a header at the same depth, so it stops the final
    record exactly like another record would.
    """
    pieces = []
    boundaries = [m.start() for m in ANY_HEADER.finditer(text)]
    for match in RECORD_HEADER.finditer(text):
        start = match.start()
        later = [b for b in boundaries if b > start]
        end = later[0] if later else len(text)
        pieces.append((match.group(1), text[start:end]))
    return pieces


def scan(pieces):
    """Report every (record, field) pair where the field appears in the record."""
    hits = []
    for record_id, body in pieces:
        for field in FIELDS:
            if field in body:
                hits.append(f"{record_id} [{field}]")
    return hits


def main(argv):
    text = SPECIMEN.read_text(encoding="utf-8")

    if "--null-control" in argv:
        # Remove the trailing section. The hits should disappear, which shows they
        # came from the tail and not from either record.
        cut = text.find(ARCHIVE_HEADER)
        if cut != -1:
            text = text[:cut]

    unclipped = split_unclipped(text)
    clipped = split_clipped(text)

    for record_id, body in unclipped:
        size = len(body.encode("utf-8"))
        absorbed = ARCHIVE_HEADER in body
        line = f"{record_id}: bytes={size:4d}   contains '{ARCHIVE_HEADER}'={absorbed}"
        if absorbed:
            line += "      <- absorbed the tail"
        print(line)

    print(f"{'UNCLIPPED':9s} (the bug) : {scan(unclipped)}")
    print(f"{'CLIPPED':9s} (correct) : {scan(clipped)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
