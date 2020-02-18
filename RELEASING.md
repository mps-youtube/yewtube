Release process for pafy and mps-youtube
========================================

Looking at the commits and Github releases for previous versions can provide an example.

Version numbers
---------------
### pafy
Bump the `__version__` in `__init__.py`.

### mps-youtube
Bump the `version` in `VERSION`, `__version__` and `__notes__` in `__init__.py`, and `VERSION` in `setup.py`.

Changelogs
----------
Update `CHANGELOG` with a summary of changes since the last release. `git shortlog` can be helpful to see what commits have occurred.

### mps-youtube
Also update `New Features` in `helptext.py`. This help section has ended up falling out of date. If it isn't kept up to date, it should probably be removed.

Github Release
--------------
Create a release through the Github website, tagging the commit that should be released. The text from the `CHANGELOG` should be copied to the release.

py2exe
------
For mps-youtube, a `.exe` file should be built with `python setup.py py2exe` under Windows. Make sure the correct pafy and youtube-dl versions are being used, since they will be embedded in the binary. Attach this file to the Github release.

PyPI
----
Push the source, and a wheel build, to PyPI. Be careful that everything is correct at this point; PyPI does not allow replacing an uploaded file with a different one of the same name.

GPG Signatures
--------------
The `.tar.gz` signatures for `pafy` and `mps-youtube` also have GPG signatures attached to the release. Currently, they are signed with @ids1024's key, so only he can perform this step.

Possible Simplifications to this Process
----------------------------------------
The New Features help text isn't really important, but it is genuinely nice to have if kept up to date.

Perhaps the `CHANGELOG` file isn't really needed, if Github releases includes that information.
