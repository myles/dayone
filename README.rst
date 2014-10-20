Day One Python Library
======================

A Python library for `Day One`_

.. _Day One: http://dayoneapp.com/

Usage
-----

.. code-block:: python

	>>> from dayone.journal import Journal, Entry
	>>> journal = Journal(path_to_dayone_journal)
	>>>

List entries:

.. code-block:: python

	>>> journal.entries
	[dayone.journal.Entry(...)]
	>>>

Create an entry:

.. code-block:: python

	>>> entry = Entry(path_to_dayone_journal)
	>>> entry.text = "Hello, World!"
	>>> entry.save_file()
	>>>
