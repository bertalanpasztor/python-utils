""" A modul egyedi azonosítókat generál."""

import random

def generateid() -> str:
    """ Véletlenszerű 20 jegyű azonosítót generál nagyobb egyediséget biztosítva """
    rndint = random.randint(10**19, 10**20 - 1)
    szam = rndint
    szam_konv = ''
    while szam > 0:
        szamjegy = szam % 35
        if 0 <= szamjegy <= 9:
            szam_konv = chr(48 + szamjegy) + szam_konv
        elif 10 <= szamjegy <= 34:
            szam_konv = chr(65 + szamjegy - 10) + szam_konv
        szam = szam // 35
    return szam_konv

