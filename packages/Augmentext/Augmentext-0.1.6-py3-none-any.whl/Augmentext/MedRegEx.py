# MedRegEx.py
# Collection of regular expressions for use in
# Author: Marcus D. Bloice <https://github.com/mdbloice> and contributors
# Licensed under the terms of the MIT Licence.

# See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC61354/
# for a discussion on units.

import re

# Centimetres
# Matches
cm = re.compile("[+-]?(\d*\.)?\d+\s*(cm|centimeters|centimetres)(.|\W|-)")

# Millimetres
mm = re.compile("[+-]?(\d*\.)?\d+\s*mm")

# Milligrams per decilitre
mg_dl = re.compile("[+-]?(\d*\.)?\d+\s*mg/dl")

# Grams per decilitre
mg_dl = re.compile("[+-]?(\d*\.)?\d+\s*(g|grams)/l")

# Kilograms per metre squared
kg_m2 = re.compile("[+-]?(\d*\.)?\d+\s*(kgm2|kg m2)(.|\W|-)")

# Centigrade
centigrade = re.compile("[+-]?(\d*\.)?\d+\s*C")
centigrade_variants = ["C", "°C", "centigrade"]

# Millimetres of mercury
mm_hg = re.compile("[+-]?(\d*\.)?\d+\s*(mmHg|mm Hg|mm/Hg)(.|\W|-)")
mm_hg_variants = ["mmHg", "mm Hg", "mm/Hg"]

# Inches of mercury
# FINISH

text_text = \
"""
Blood pressure of 34.2 mm Hg.
Blood pressure of 34.2 mmHg.
Blood pressure of 34.2mmHg.
Fat body was 30.1 kg/m2.
Incision was 34.4cm.
Incision was 1.1in.
Incisoin was 1.1 in.
Incision was 1.1 inches.
"""
