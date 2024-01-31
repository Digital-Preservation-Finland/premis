Release notes
=============

Version 0.29
------------

- Code cleanups and syntax fixes

Version 0.28
------------
- Add RHEL9 RPM spec file
- Fix Python package build

Version 0.27
------------

- Changed ``relationship`` function
    - Changed parameter name from ``related_object`` to ``related_objects``
    - Changed ``related_objects`` to expect an iterable of objects rather than one object
    - Changed the returned element to include all objects given in ``related_objects``.
- Python 2.7 support officially removed
