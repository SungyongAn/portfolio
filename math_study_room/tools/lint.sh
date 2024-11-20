#!/bin/bash
cd ${BASH_SOURCE%/*}
cd ..
flake8 --max-line-length 120 .
ruff check .
ruff format . --check
