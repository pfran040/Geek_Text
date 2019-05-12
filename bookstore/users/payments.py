import datetime

YEARS = []
THIS_YEAR = datetime.datetime.today().year
LAST_YEAR = datetime.datetime.today().year + 10

for y in range(THIS_YEAR, LAST_YEAR):
    YEARS.append((y,y))

JAN = 1
FEB = 2
MAR = 3
APR = 4
MAY = 5
JUN = 6
JUL = 7
AUG = 8
SEP = 9
OCT = 10
NOV = 11
DEC = 12

MONTHS = (
    (JAN, 'January'),
    (FEB, 'February'),
    (MAR, 'March'),
    (APR, 'April'),
    (MAY, 'May'),
    (JUN, 'June'),
    (JUL, 'July'),
    (AUG, 'August'),
    (SEP, 'September'),
    (OCT, 'October'),
    (NOV, 'November'),
    (DEC, 'December'), )
