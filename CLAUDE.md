# Story Generator

Interactive branching narrative generator using NetworkX graphs.

## Orientation
@INTERFACE.md

## Running
```bash
python story_generator.py --seed 42 --branches 3 --output-dir output/
```

## Web interface
```bash
python run_web.py                    # http://127.0.0.1:8138
python scripts/build_static.py       # static site -> site/
python scripts/make_story_fixture.py # after any change to the generator (JS port is tested against it)
```

## Testing
```bash
python -m pytest tests/ -v
```
