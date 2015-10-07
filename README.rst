======================
Day One Python Library
======================

.. image:: https://travis-ci.org/myles/dayone.svg?branch=master
    :target: https://travis-ci.org/myles/dayone

A Python library and command line application for `Day One`_.

.. _Day One: http://dayoneapp.com/

Libray Usage
------------

.. code-block:: pycon

	>>> from dayone.journal import Journal, Entry
	>>> journal = Journal(path_to_dayone_journal)
	>>>

List entries
~~~~~~~~~~~~

.. code-block:: pycon

	>>> journal.entries
	[dayone.journal.Entry(...)]
	>>>

Create an entry
~~~~~~~~~~~~~~~

.. code-block:: pycon

	>>> entry = Entry(path_to_dayone_journal)
	>>> entry.text = "Hello, World!"
	>>> entry.save_file()
	>>>

Command Line Usage
------------------

First setup your py-dayone envourment.

.. code-block:: shell-session

	$ py-dayone setup
	Path to your DayOne journal. /Users/mb/Dropbox/Apps/Day One/Journal.dayone
	Setup py-dayone.
	$ 
