#!/bin/bash
cd ${BASH_SOURCE%/*}
cd ..
pytest -s test
