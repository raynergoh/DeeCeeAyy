import datetime

def get_last_year(datetime):
    date = list(datetime)
    year = int(date[3])
    if (date[:4] == ['2','0','0','0']):
        date[0] = '1'
        date[1] = '9'
        date[2] = '9'
        date[3] = '9'
    elif (year == 0):
        sub = int(date[2]) - 1
        date[2] = str(sub)
        date[3] = '9'
    else:     
        date[3] = str(year - 1)
    lastYear = "".join(date)
    return lastYear

# today = str(datetime.date.today())
today = "1908-08-09"

lastyear = get_last_year(today)

print(lastyear)