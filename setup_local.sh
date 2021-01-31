#!/bin/bash
pip install git+https://${GITHUB_TOKEN}:x-oauth-basic@github.com/VaLena10012020/Finanzen_python_base.git@minor_updates#egg=finanzen_base
pip install -e .[dev]
pre-commit install
pre-commit autoupdate
