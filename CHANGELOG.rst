Changelog
=========
All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_.


Unreleased
----------

- Changed ``relationship`` function
    - Changed parameter name from ``related_object`` to ``related_objects``
    - Changed ``related_objects`` to expect an iterable of objects rather than one object
    - Changed the returned element to include all objects given in ``related_objects``.
