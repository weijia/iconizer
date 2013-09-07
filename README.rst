===============================
iconizer
===============================

.. image:: https://badge.fury.io/py/iconizer.png
    :target: http://badge.fury.io/py/iconizer
    
.. image:: https://travis-ci.org/weijia/iconizer.png?branch=master
        :target: https://travis-ci.org/weijia/iconizer

.. image:: https://pypip.in/d/iconizer/badge.png
        :target: https://crate.io/packages/iconizer?version=latest


"Iconize console application to task bar icon."

* Free software: BSD license
* Documentation: http://iconizer.rtfd.org.

Features
--------

Transform python console script, java console app and other windows console app to an task bar icon.
* No black console window with task bar item will be dislayed anymore.
* The console log can be showed through task bar icon menu.

Additional features:
-------------------------------------------------------------------------------------------------------
* Send msg to console manager to launch python script app, java console app, and other console app.
* Send msg to console manager to open a web page.

Interface:
-------------------------------------------------------------------------------------------------------
* Msg service should be passed in as parameters to this app.
* An initial app list may be passed to this app, so all apps in the list will be launched by console manager in managed windows instead of in black console windows.

Implementation Progress:
-------------------------------------------------------------------------------------------------------
* Used in approot: https://github.com/weijia/approot
* TODO