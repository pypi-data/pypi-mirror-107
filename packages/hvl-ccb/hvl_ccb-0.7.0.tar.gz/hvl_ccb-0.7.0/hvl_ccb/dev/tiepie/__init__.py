#  Copyright (c) 2019-2021 ETH Zurich, SIS ID and HVL D-ITET
#
"""
This module is a wrapper around libtiepie Oscilloscope devices; see
https://www.tiepie.com/en/libtiepie-sdk .

The device classes adds simplifications for starting of the device (using serial
number) and managing mutable configuration of both the device and oscilloscope's
channels. This includes extra validation and typing hints support.

To install libtiepie on Windows:
The installation of the Python bindings "python-libtiepie" is done automatically
with the dependencies of the hvl_ccb. The additional DLL for Windows is included in
that package.

On a Linux-system additional libraries have to be installed; see
https://www.tiepie.com/en/libtiepie-sdk/linux .

On a Windows system, if you encounter an :code:`OSError` like this::

    ...
        self._handle = _dlopen(self._name, mode)
    OSError: [WinError 126] The specified module could not be found

most likely the python-libtiepie package was installed in your :code:`site-packages/`
directory as a :code:`python-libtiepie-*.egg` file via :code:`python setup.py
install` or :code:`python setup.py develop` command. In this case uninstall the
library and re-install it using :code:`pip`::

    $ pip uninstall python-libtiepie
    $ pip install python-libtiepie

This should create :code:`libtiepie/` folder. Alternatively, manually move the folder
:code:`libtiepie/` from inside of the :code:`.egg` archive file to the containing it
:code:`site-packages/` directory (PyCharm's Project tool window supports reading and
extracting from :code:`.egg` archives).

"""
