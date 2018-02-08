PREMIS Library
==============

This repository contains general Python functions for PREMIS 2.x XML handling.

Installation
------------

This software is tested with Python 2.7 with Centos 7.x / RHEL 7.x releases.

Install the required software with command::

    pip install -r requirements_github.txt

Usage
-----

Import the library with::

    import premis

All the functions can now be used with calling premis.<function>.

For example, the fixity() function in object_base.py can be used with::
    
    fix_elem = premis.fixity('MD5', '...')

This creates a PREMIS <fixity> element with <messageDigestAlgorithm> and
<messgeDigest> to fix_elem as lxml.etree.

Please, see the PREMIS documentation for more information:
https://www.loc.gov/standards/premis/

Copyright
---------
All rights reserved to CSC - IT Center for Science Ltd.

