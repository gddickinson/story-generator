"""Start the Interactive Story Generator web app on http://127.0.0.1:8138 (local only).

Run: python run_web.py [--port 8138]
Needs: pip install -r requirements-web.txt
"""
import argparse

import uvicorn

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8138)
    port = ap.parse_args().port
    print(f"Story generator web app: http://127.0.0.1:{port}")
    uvicorn.run("storygen.web.app:app", host="127.0.0.1", port=port)
