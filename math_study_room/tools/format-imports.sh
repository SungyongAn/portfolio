#!/bin/bash
cd ${BASH_SOURCE%/*}
cd ..
ruff check --fix --select I
