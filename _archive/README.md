# Archive

`story-generator.py` is the original single-file version of the generator, kept for reference only. It is
superseded by the `storygen/` package and `story_generator.py` (same features, split into modules, with tests).

Known problems that were fixed in the package but **not** here: the same seed can give a different story in each
run (world elements kept in sets, whose order depends on per-process string hashing), and the generator reseeds
Python's global `random` module. Use `python story_generator.py --seed N` instead.
