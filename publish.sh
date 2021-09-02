#!/usr/bin/env bash

rm -rvf build || exit 1

rm -rvf dist || exit 1

rm -rvf puts.egg-info || exit 1

# check-manifest || exit 1

python setup.py sdist bdist_wheel || exit 1

# python -m twine upload dist/* || exit 1