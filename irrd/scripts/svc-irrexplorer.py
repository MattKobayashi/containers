#!/usr/bin/env python3
"""Script to start the IRR Explorer web application."""

import uvicorn  # type: ignore

if __name__ == "__main__":
    uvicorn.run(
        "irrexplorer.app:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="info"
        )
