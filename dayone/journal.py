"""
Copyright (c) 2014, Myles Braithwaite <me@mylesbraithwaite.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in
  the documentation and/or other materials provided with the
  distribution.

* Neither the name of the Monkey in your Soul nor the names of its
  contributors may be used to endorse or promote products derived
  from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import os
import uuid
import glob
import datetime
import textwrap
import plistlib
from collections import OrderedDict

import markdown
from pytz import timezone
from tzlocal import get_localzone

class Entry(object):
    """A Journal Entry."""
    
    def __init__(self, journal_dir, filename=None):
        self.entry_data = {}
        self.journal_dir = journal_dir
        self.filename = filename
        
        if self.filename:
            if not self.filename.endswith('.doentry'):
                self.filename = "%s.doentry" % filename
            
            self.load_file()
    
    def __repr__(self):
        if self.uuid:
            return "%s.%s(%s)" % (self.__module__, self.__class__.__name__, self.uuid)
        else:
            return "%s.%s" % (self.__module__, self.__class__.__name__)
    
    def __str__(self):
        if self.text:
            return textwrap.wrap(self.text)[0]
    
    def load_file(self):
        entry_path = os.path.join(self.journal_dir, 'entries', self.filename)
        self.entry_data = plistlib.readPlist(entry_path)
    
    def save_file(self):
        if not self.text:
            raise Exception
        
        if self.filename:
            entry_path = os.path.join(self.journal_dir, 'entries', self.filename)
        else:
            _uuid = str(uuid.uuid4()).replace('-', '').upper()
            self.filename = "%s.doentry" % _uuid
            self.entry_data['UUID'] = _uuid
            self.entry_data['Creation Date'] = datetime.datetime.now()
            self.entry_data['Time Zone'] = str(get_localzone())
            self.entry_data['Starred'] = False
            entry_path = os.path.join(self.journal_dir, 'entries', self.filename)
        
        plistlib.writePlist(self.entry_data, entry_path)
        
        self.load_file()
    
    @property
    def uuid(self):
        return self.entry_data['UUID']
    
    @property
    def text(self):
        return self.entry_data['Entry Text']
    
    @text.setter
    def text(self, x):
        self.entry_data['Entry Text'] = str(x)
    
    @property
    def text_html(self):
        return markdown.markdown(self.text, ['markdown.extensions.extra'])
    
    @property
    def tags(self):
        return self.entry_data.get('Tags', [])
    
    @tags.setter
    def tags(self, x):
        self.entry_data['Tags'] = x
    
    @property
    def photo(self):
        photos = glob.glob(os.path.join(self.journal_dir, "photos", "%s.*" % self.uuid))
        if photos:
            return photos[0]
        else:
            return None
    
    @property
    def creation_date(self):
        if self.time_zone:
            return self.time_zone.localize(self.entry_data['Creation Date'])
        else:
            return self.entry_data['Creation Date']
    
    @property
    def starred(self):
        return self.entry_data['Starred']
    
    @starred.setter
    def starred(self, x):
        self.entry_data['Starred'] = bool(x)
    
    @property
    def time_zone(self):
        return timezone(self.entry_data.get('Time Zone', None))

class Journal(object):
    """A Day One Journal."""
    
    def __init__(self, journal_dir):
        self.journal_dir = journal_dir
        
        self.entries_dir = os.path.join(journal_dir, "entries")
        self.photos_dir = os.path.join(journal_dir, "photos")
        
        if not os.path.exists(self.entries_dir):
            os.makedirs(self.entries_dir)
        
        if not os.path.exists(self.photos_dir):
            os.makedirs(self.photos_dir)
        
        self.entries = []
        
        self.get_entries()
    
    def get_entries(self):
        entries = glob.glob(os.path.join(self.entries_dir, "*.doentry"))
        
        for entry in entries:
            filename = os.path.basename(entry)
            self.entries += [Entry(self.journal_dir, filename),]
        
        self.entries.sort(key=lambda e: e.creation_date, reverse=True)