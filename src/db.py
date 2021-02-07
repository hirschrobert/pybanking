#!/usr/bin/env python3
# -*- Mode:Python; encoding:utf8 -*-
#
# pybanking - a banking backend client at your service
# Copyright (C) 2021  Robert Hirsch <info@robert-hirsch.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import dataset
# connecting to a SQLite database
db = dataset.connect('sqlite:///./database/pybanking.db')

def insertTransactions(transactions):
    table = db['transactions']
    try:
        for t in transactions['transactions']:
            table.insert_ignore(dict(tid=t['id'], transaction=t), ['tid'])
    except:
      raise Exception("Could not insert transaction")
    return 0
