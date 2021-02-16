#!/usr/bin/env python3
# -*- Mode:Python; encoding:utf8 -*-
#
# pybanking - a banking backend client at your service
# Copyright (C) 2021  Robert Hirsch <dev@robert-hirsch.de>
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

from sqlalchemy import Table, Column, Integer, String, JSON, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from controller.base import Base  # @UnresolvedImport
from model.bank import Bank


class Account(Base):
    __tablename__ = 'accounts'
    __table_args__ = (UniqueConstraint('username', 'bank_id', name='account_uc'),)

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    access_token = Column(JSON)
    scope = Column(JSON)
    ibans = relationship("Iban", back_populates="account")
    bank_id = Column(Integer, ForeignKey('banks.id'))
    bank = relationship("Bank", back_populates="accounts")

    def __init__(self, username, password, access_token):
        self.username = username
        self.password = password
        self.access_token = access_token

    def setBank(self, bank):
        self.bank = bank
        
    def getAccessToken(self):
        return self.access_token

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password
