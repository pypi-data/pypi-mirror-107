[![Python application](https://github.com/jininvt/adolet-db/actions/workflows/python-app.yml/badge.svg)](https://github.com/jininvt/adolet-db/actions/workflows/python-app.yml)

# Adolet API

Python ORM that will enable users to make API calls. The Python library will allow users to interface with api.postgres.com.

This library will be hosted on PyPi as a Python package.

## Deploy changes to PyPi
```
python3 setup.py sdist

twine upload --skip-existing dist/*
```