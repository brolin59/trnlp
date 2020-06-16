#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
This file is part of trnlp.

trnlp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

trnlp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with trnlp.  If not, see <https://www.gnu.org/licenses/>.
Copyright (c) 2016-2020, Esat Mahmut Bayol

The full license is in the file LICENSE.txt, distributed with this software.
"""

# r"(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)"

abbr = [r"(?=\b([a-zçğıİöşü]+\.\s[a-zçğıİöşü]+\.\s[a-zçğıİöşü]+\.)(?=\s))",
        r"(?=\b([a-zçğıİöşü]+\.\s[a-zçğıİöşü]+\.)(?=\s))",
        r"(?=\b([a-zçğıİöşü]+-[a-zçğıİöşü]+)(?=\s))",
        r"(?=\b([a-zçğıİöşü]+\.)(?=\s))"]

date_rgx = [r"(?:\b(0[1-9]|1[0-9]|2[0-9]|3[0-1])\s"
            r"([eoşmnhtak][kcuaiİeğyr][abrsyzmuliİ][a-zıü]{1,4})"
            r"(\s\d{2,4})?)",
            r"(?:\b(0[1-9]|1[0-9]|2[0-9]|3[01])[/.-](0[1-9]|1[0-2])[/.-]\d{2,4})",
            r"(\d{1,4})(?= yılı)"]

fin_rgx = [r"(?:[\$€₺]\d+(\.\d\d\d)*(,\d\d)?)",
           r"(?:\d+(\.\d\d\d)*\s?(try|türk l[iİ]rası|tl|₺|l[iİ]ra|avro|euro|dolar))",
           r"(?:(%|‰|yüzde|b[iİ]nde)\s?\d+(,\d+)?)",
           r"(?:\d+(,\d+)?(%|‰))"]

time_rgx = [r"(?:(0?[0-9]|1[0-9]|[0-2][0-4])[.:][0-5][0-9])",
            r"(?:(0?[0-9]|1[0-2])([.:][0-5][0-9])?\s?(am|pm|a\.m\.|p\.m\.))"]

phone_rgx = [r"(?:(\+9|009)?0?\s?(5[0-5][0-9])\s?\d{3}\s?\d{2}\s?\d{2})",
             r"(?:(\+9|009)?0?\s?([234][0-9][0-9])\s?\d{3}\s?\d{2}\s?\d{2})"]

web_rgx = [r"(?:[a-z0-9_\-\.]+)@([a-z0-9_\-\.]+)\.([a-z]{2,5})",
           r"(?:(https?://)?(www\.)?[a-z0-9]+\.[a-z]{3,6}[.a-z0-9\?=\-\+%&\_/]*)"]

th_rgx = [r"(?<=\s)(\d+\.)(?=\s)",
          r"(?<=\s)([xvı]+\.)(?=\s)", ]

nbr_rgx = [r"(?:(\d+)([,.]\d+)?)",
           r"(?:(\d{1,3})([,.]\d{3})*([,.]\d+)?)"]

enter_regex = [r"\n"]

space_regex = [r"\s"]

proper_noun_abbr = [r"((?<=\s)([a-zçğıİöşü]\.))"]

words = [r"([0-9a-zÀ-ž]+([’'][a-zçğıöşü]+)?)"]

suff = [r"(?<=')([a-zÀ-ž]+)"]

end_of_seq = [r"(\?\.\.)|(!\.\.)|(\.\.\.)|(\?)|(!)|(:)|(\.)"]

punch = [r"[^\w\s]"]

all_regex = [(fin_rgx, 'financial'),
             (date_rgx, 'date'),
             (time_rgx, 'time'),
             (phone_rgx, 'phone'),
             (web_rgx, 'web'),
             (th_rgx, 'th'),
             (nbr_rgx, 'number'),
             (proper_noun_abbr, 'proabbr'),
             (end_of_seq, 'eos'),
             (words, 'word'),
             (suff, 'suffix'),
             (enter_regex, 'enter'),
             (space_regex, 'space'),
             (punch, 'punch')]
