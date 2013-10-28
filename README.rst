Copyright (c) 2010-2013, oDesk http://www.odesk.com
All rights reserved.


============================
Python bindings to oDesk API
============================

This is a Python bindings for Public oDesk API http://developers.odesk.com/
Using the API you can build apps that will help you:

* Mangage your distributed team
* Search for contractors and jobs
* Send bulk invitations to interview and make offers
* Send bulk messages to your team
* Retrieve Time & Financial information for your company, team and contractors

API is the best way to comunicate between apps.


Requirements
============
httplib2>=0.8
oauth2>=1.5.211
urllib3>=1.7


Installation
============

    pip install python-odesk

All the dependencies will be automatically installed as well.


SSL Certificates Note
=====================
Unfortunately SSL certificates for oDesk are not included in the ``httplib==0.8``.

Threrefore if you use Debian/Ubuntu/Archlinux,
we recomend to install a package ``httplib2.ca_certs_locater``::

    pip install httplib2.ca_certs_locater

It will force ``httplib2`` to use the OS's certificates file.

Another option is to create a ``ca_certs_locater.py`` in your projects directory
and following the example from https://github.com/dreamhost/httplib2-ca_certs_locater
load patched ``ca_certs.txt`` file.

You can find patched ``ca_certs.txt`` here:
https://github.com/kipanshi/odesk_meter/blob/master/lib/httplib2/cacerts.txt


Quickstart
==========
First, you need to create API key for authorization here:
https://www.odesk.com/services/api/keys

Installing **Ipython** interactive shell is very useful for playing
with the API, it has autocomplete, history, displays docstring help if you add '?'
to the end of variable/function/class/method and many other nice things.
So we greatly encourage you to install it: ``pip install ipython``

To get started, look at the docs http://odesk.github.io/python-odesk/how_to.html
and also look at the ``examples/`` folder to see examples how to
obtain oauth access tokens for web application and desktop application.

Also threre's a list of opensource projects using ``python-odesk``:

* oDesk Meter https://github.com/kipanshi/odesk_meter
* oDesk Graphs https://github.com/demalexx/odesk-graphs


Useful Links
============

* [Git repo](http://github.com/odesk/python-odesk)
* [Issues](http://github.com/odesk/python-odesk/issues)
* [Documentation](http://odesk.github.com/python-odesk/)
* [Mailing list](http://groups.google.com/group/python-odesk)
* [Facebook group](http://www.facebook.com/group.php?gid=136364403050710)
