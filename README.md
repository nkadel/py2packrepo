py2pack4repo
==========

Wrapper for SRPM building tools for py2pack 4 on CentOS 7 and Fedora 28.

Building Py2pack
==============

These are rebuilt from Fedora rawhide releases, and need to be built
and installed in the following order.

* make cfgs # Create local .cfg configs for "mock".
* * epel-7-x86_64.cfg # Used for some Makefiles
* * fedora-28-x86_64.cfg # Used for some Makefiles
* * py2pack4repo-7-x86_64.cfg # Activates local RPM dependency repository
* * py2pack4repo-428-x86_64.cfg # Activates local RPM dependency repository

* make repos # Creates local local yum repositories in $PWD/py2pack4repo
* * py2pack4repo/el/7
* * py2pack4repo/fedora/28

* make # Make all distinct versions using "mock"

Building a compoenent, without "mock" and in the local working system,
can also be done for testing.

* make build

py2pack has strong dependencies on other python modules that may, or may not,
be available in a particular OS. These include:

* python-metaextract-srpm

Installing Py2pack
==============--

The relevant yum repository is built locally in py2pack4reepo. To enable the repository, use this:

* make repo

Then install the .repo file in /etc/yum.repos.d/ as directed. This
requires root privileges, which is why it's not automated.

Py2pack RPM Build Security
====================

There is a significant security risk with enabling yum repositories
for locally built components. Generating GPF signed packages and
ensuring that the compneents are in this build location are securely
and safely built is not addressed in this test setup.

		Nico Kadel-Garcia <nkadel@gmail.com>
