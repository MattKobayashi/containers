#!/usr/bin/env python3
"""Script to start the IRR Explorer web application."""

import sys
import uvicorn
import yaml

if __name__ == "__main__":
    try:
        with open("/opt/irrexplorer/irrexplorer.yaml", "r", encoding="utf-8") as yaml_conf:
            irrexplorer_conf = yaml.safe_load(yaml_conf)
    except FileNotFoundError:
        print("Error: Could not find the configuration file at /opt/irrexplorer/irrexplorer.yaml.")
        sys.exit(1)
    uvicorn.run(
        "irrexplorer.app:app",
        host="0.0.0.0",
        port=irrexplorer_conf["irrexplorer"].get("http_port", 8000),
        workers=irrexplorer_conf["irrexplorer"].get("http_workers", 4),
        log_level="info",
    )
