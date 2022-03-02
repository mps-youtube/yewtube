# Contributing for yewtube

Contributions are very much appreciated!

* Pull requests should be based on and submitted to the "develop" branch.

* Please raise an issue to discuss what you plan to implement or change before 
you start if it is going to involve a lot of work on your part.

* Please keep pull requests specific, do not make many disparate changes or
new features in one request.  A separate pull request for each feature change
is preferred.

* Please ensure your changes work in Python 3.3+ and Windows.


## Code conventions

* Maximum line length is 80 characters

* Follow the line-spacing style that is already in place.

* Ensure all functions and classes have a PEP257 compliant docstring and the
code is PEP8 compliant.

## Documentation

Install required extra docs package to setup mkdocs: `pip install -e ".[docs]"`

To run built-in dev server: `mkdocs serve`

To deploy documentation to github page: `mkdocs gh-deploy`
