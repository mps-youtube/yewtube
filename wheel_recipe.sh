# a script to build and upload wheel files on pypi.org
rm -rf dist/
semantic-release version
python -m build --sdist
python -m build --wheel
twine upload --verbose dist/*
semantic-release publish
