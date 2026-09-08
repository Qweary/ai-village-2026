# Unbounded split

A three file, zero dependency demonstration of a parsing bug that returns a wrong
answer while raising nothing, warning nothing, and exiting zero.

Takes about a minute. Python 3 standard library only. No network.

## The defect

`records.md` holds records under repeated markdown headers:

```
## ITEM-0001
...
## ITEM-0002
...
## Closed          <- an archive section, not a record
ITEM-0000 [owner: sam]
Status: closed
```

Code that wants to check one record at a time splits the file on the record
header pattern. The catch is that a record's *end* is never written down
anywhere. It exists only as "wherever the next record starts". So the last
record has no next record header to stop at, its end becomes end of file, and it
absorbs everything below it, in this case the whole archive section.

A per record check then reads record-plus-tail. It finds the `owner` and
`Status:` fields sitting in the archive, and attributes both of them to
`ITEM-0002`, which contains neither.

## Run it

```
python3 split_demo.py
```

Expected output, all four lines:

```
ITEM-0001: bytes=  51   contains '## Closed'=False
ITEM-0002: bytes= 124   contains '## Closed'=True      <- absorbed the tail
UNCLIPPED (the bug) : ['ITEM-0002 [owner]', 'ITEM-0002 [Status:]']
CLIPPED   (correct) : []
```

## What to look for

Both records are the same shape and roughly the same size. `ITEM-0001` comes out
at 51 bytes. `ITEM-0002` comes out at 124, because it is carrying 76 bytes that
belong to the archive section rather than to the record.

The correct answer is the empty list. Neither record contains an `owner` field
or a `Status:` field. The buggy splitter reports two matches anyway, and it
blames both on `ITEM-0002`.

Notice what does *not* happen. No exception. No warning. Exit status zero. The
two code paths are indistinguishable from anything except the value they return.
If you were watching a log, or a CI status, or an exit code, you would see a
clean run.

The fix is one line, and it is in `split_demo.py` next to the bug. A record ends
at the next header *of the same depth*, whatever that header happens to say. The
archive header is one of those, so it stops the last record exactly the way
another record would.

## Break it yourself

This is the half that proves the point, so do not skip it. If the two matches
really come from the tail, then removing the tail should make them disappear:

```
python3 split_demo.py --null-control
```

That reads the same file with the archive section cut off, and prints:

```
ITEM-0001: bytes=  51   contains '## Closed'=False
ITEM-0002: bytes=  48   contains '## Closed'=False
UNCLIPPED (the bug) : []
CLIPPED   (correct) : []
```

Both lists go empty, and `ITEM-0002` drops from 124 bytes to 48, which is what
the clipped splitter was reporting all along. The matches were never in the
records. They were in the tail.

You can do the same thing by hand: open `records.md`, delete from `## Closed`
down, and run the script again with no flag.

Other things worth trying:

* Add a second entry under `## Closed`. The absorbed size grows, but the match
  count stays at two, because it is set by the number of fields being looked for
  and not by how much text got swallowed.
* Add a third record at the bottom, *below* the archive. `ITEM-0002` still
  absorbs the archive, at 125 bytes, even though it is no longer the last
  record, and the new `ITEM-0003` comes out clean at 44. "Only the last record
  is affected" is the wrong mental model. Any record followed by a same depth
  header the splitter does not recognise will absorb it, and running off the end
  of the file is just the most common way that happens.
* Give `ITEM-0001` a genuine `owner:` line. The buggy run now reports three
  matches, one real and two invented, with nothing in the output to tell them
  apart. The clipped run reports exactly the one that is real.

## Files

* `records.md` - the specimen, 186 bytes
* `split_demo.py` - both splitters, the check, and the null control
* `README.md` - this file
