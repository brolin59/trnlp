# -*- coding: utf-8 -*-
__version__ = '1.0'
__author__ = 'Esat Mahmut Bayol'

"""/*

Copyright 2018 Esat Mahmut Bayol

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA

*/"""
import sqlite3

# sozluk_tekli.txt içindeki veriler veritabanına işlenir

with open('sozluk_tekli.txt', 'r', encoding='utf-8') as fl:
    may_sozluk = [line.strip().split('\t') for line in fl]
del fl

with sqlite3.connect('tr_NLP.sqlite') as vt:
    im = vt.cursor()
    im.execute("DROP TABLE IF EXISTS tr_sozluk")
    im.execute("CREATE TABLE IF NOT EXISTS tr_sozluk (sozcuk, sozcuk_turu, ses_olayi, sozcuk_konusu, sozcuk_kokeni)")
    for veri in may_sozluk:
        im.execute("INSERT INTO tr_sozluk VALUES (?, ?, ?, ?, ?)", veri)
    vt.commit()
