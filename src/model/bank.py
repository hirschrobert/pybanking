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


class Bank(Base):
    __tablename__ = 'banks'
    __table_args__ = (UniqueConstraint('name', 'authorize_endpoint', 'tokenurl', 'apiurl', name='bank_uc'),)
    id = Column(Integer, primary_key=True)
    bic = Column(String, unique=True)
    name = Column(String)
    authorize_endpoint = Column(String)
    tokenurl = Column(String)
    apiurl = Column(String)
    accountInput = Column(JSON)
    requests = Column(JSON)
    ibans = relationship("Iban", back_populates="bank")
    accounts = relationship("Account", back_populates="bank")

    def __init__(self, bic, name, authorize_endpoint, tokenurl, apiurl, accountInput, requests):
        self.bic = bic
        self.name = name
        self.authorize_endpoint = authorize_endpoint
        self.tokenurl = tokenurl
        self.apiurl = apiurl
        self.accountInput = accountInput
        self.requests = requests
    
    def getAccountInput(self):
        return self.accountInput
