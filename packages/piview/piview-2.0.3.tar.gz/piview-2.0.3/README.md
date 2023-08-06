======
PiView
======


.. image:: https://img.shields.io/pypi/v/piview.svg
        :target: https://pypi.python.org/pypi/piview

.. image:: https://img.shields.io/travis/AdyGCode/piview.svg
        :target: https://travis-ci.com/AdyGCode/piview

.. image:: https://readthedocs.org/projects/piview/badge/?version=latest
        :target: https://piview.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



**A Raspberry Pi System Information Package**

.. image:: ./docs/PiView.svg
        :target: https://pypi.python.org/pypi/piview
        :alt: PiView Icon

PiView provides the details of the Raspberry Pi currently being interrogated. System information includes, but is not limited to:

- **CPU**: max load across cores, temperature, clock speed
- **GPU**: temperature
- **HARDWARE**: bluetooth, i2c, spi, camera statuses
- **HOST**: boot time, model, name, revision, serial number, uptime
- **NETWORK**: host name, interface names, ip addresses, mac addresses
- **STORAGE**: total disk capacity, free disk capacity, total RAM and free RAM

Also includes a small utility library with:

- conversion of bytes into Kilobytes, Megabytes, Gigabytes and up
- create list with a quartet of integer numbers representing the IPv4 Address

General Information
-------------------
* Free software: Open Software License ("OSL") v. 3.0
* Documentation: https://piview.readthedocs.io.


Features
--------

* TODO


Requirements
------------

This project requires the following package(s):

* `psutils`

Remaining packages are Python 'built-ins'.


Credits
-------

A very large thank you to Matt Hawkins upon whose code this package is based: https://www.raspberrypi-spy.co.uk/

The original code may be found at https://github.com/tdamdouni/Raspberry-Pi-DIY-Projects/blob/master/MattHawkinsUK-rpispy-misc/python/mypi.py

Thank you to Sander Huijsen for his contributions and guidance in all things Python.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


Copyright
---------

Copyright Adrian Gould, 2021-. Licensed under
the Open Software License version 3.0
