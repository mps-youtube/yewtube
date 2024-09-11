# a script to build and upload wheel files on pypi.org
rm -rf dist/
python -m build --sdist
python -m build --wheel
twine upload --verbose dist/*
