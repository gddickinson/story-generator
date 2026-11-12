"""storygen.web - web interface for the story generator.

Contents:
    app        - FastAPI app: front end in static/, JSON API under /api, STATIC_ENDPOINTS for the Pages export
    story_api  - spec(), story(seed, branches), samples(): story data produced by the real storygen package
    static/    - ES-module front end; story_engine.js is the JS port of the generator (node-tested)
"""
