# The World in One Picture — Saturday 21 November 2026

A make.fun `news-image-20261121` entry: one 1024×1024 image summing up
Saturday 21 November 2026's world news — 3 heroes, 12 cards, 18 briefs,
27 stories across 6 regions, every story dated to the day, with a date
check naming what was excluded and a "not yet known" line.

## Build

`draw.py` renders `entry.png` with Pillow from a single story data table
(the tally strap, region bar and field bar are computed from that same
table). `main.py` is the competition entry point: it copies `entry.png`
to the output directory, standard library only, deterministic bytes.

## License

MIT — see `LICENSE`. Fonts are Playfair Display and Archivo, both under
the SIL Open Font License 1.1 (see `fonts/OFL-*.txt`).
SPDX-License-Identifier: MIT
