import os
import unittest
import datetime

from dayone import journal


TEST_DIR_PATH = os.path.split(os.path.abspath(__file__))[0]
JOURNAL_DAYONE_PATH = os.path.join(TEST_DIR_PATH, 'Journal.dayone')


class TestEntryObject(unittest.TestCase):
    def setUp(self):
        self.entry = journal.Entry(JOURNAL_DAYONE_PATH,
                                   '31A6C3FEB30C4C07AA4784128EC30AAB.doentry')

    def test_text(self):
        self.assertEqual(self.entry.entry_data['Entry Text'], "Hello, World!")

    def test_tags(self):
        self.assertEqual(self.entry.entry_data['Tags'], ["Testing"])

    def test_photo(self):
        photo_path = os.path.join(JOURNAL_DAYONE_PATH,
                                  "photos", "%s.jpg" % self.entry.uuid)
        self.assertEqual(photo_path, self.entry.photo)

    def test_create_journal_entry(self):
        entry = journal.Entry(JOURNAL_DAYONE_PATH)
        today = datetime.date.today()
        text = "This is a test entry for the date of %s." % today
        entry.text = text
        entry.save_file()
        self.assertEqual(text, entry.text)


class TestJournalObject(unittest.TestCase):
    def setUp(self):
        self.journal = journal.Journal(JOURNAL_DAYONE_PATH)

    def test_get_entries(self):
        self.journal.get_entries()
        entries = self.journal.entries
        self.assertTrue(entries)

    def test_filter_by_date(self):
        entries = self.journal.filter_by_date(datetime.date.today())
        self.assertTrue(entries)

    def test_filter_between_dates(self):
        TODAY = datetime.date.today()
        SEVEN_DAYS_AGO = TODAY - datetime.timedelta(days=7)
        entries = self.journal.filter_between_dates(SEVEN_DAYS_AGO, TODAY)
        self.assertTrue(entries)


if __name__ == '__main__':
    unittest.main()
