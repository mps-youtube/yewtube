rm -rf dist/
python -m build --sdist
python -m build --wheel
twine upload --verbose dist/*