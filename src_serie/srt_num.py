"""Spanish number words for transcript checks ('36.000' -> 'treinta y seis mil')."""
import re

UNI = "cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro veinticinco veintiséis veintisiete veintiocho veintinueve".split()
DEC = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
CEN = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos", 6: "seiscientos", 7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def words_es(n):
    if n < 30:
        return UNI[n]
    if n < 100:
        return DEC[n // 10] + ("" if n % 10 == 0 else " y " + UNI[n % 10])
    if n < 1000:
        return "cien" if n == 100 else CEN[n // 100] + ("" if n % 100 == 0 else " " + words_es(n % 100))
    if n < 1_000_000:
        k = n // 1000
        return ("mil" if k == 1 else words_es(k) + " mil") + ("" if n % 1000 == 0 else " " + words_es(n % 1000))
    m = n // 1_000_000
    return ("un millón" if m == 1 else words_es(m) + " millones") + ("" if n % 1_000_000 == 0 else " " + words_es(n % 1_000_000))


def num_es(token):
    m = re.fullmatch(r"([^\d]*)([\d.,]*\d)([^\d]*)", token)
    if not m:
        return token
    return m.group(1) + words_es(int(re.sub(r"[.,]", "", m.group(2)))) + m.group(3)
