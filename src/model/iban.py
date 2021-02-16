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

from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from controller.base import Base  # @UnresolvedImport
from model.bank import Bank
from model.account import Account


class Iban(Base):
    __tablename__ = 'ibans'

    id = Column(Integer, primary_key=True)
    iban = Column(String, unique=True)
    bank_id = Column(Integer, ForeignKey('banks.id'))
    bank = relationship("Bank", back_populates="ibans")
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account", back_populates="ibans")

    def __init__(self, iban):
        self.iban = iban
    
    def setBank(self, bank):
        self.bank = bank
