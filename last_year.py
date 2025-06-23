from datetime import datetime, timedelta

def get_last_year(date_str):
    """
    Returns the same date one year ago.
    Args:
        date_str (str): Date in 'YYYY-MM-DD' format.
    Returns:
        str: Date string for the same day last year.
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        last_year_date = date.replace(year=date.year - 1)
        return last_year_date.strftime("%Y-%m-%d")
    except ValueError:
        # Handles leap years and other edge cases by subtracting 365 days
        date = datetime.strptime(date_str, "%Y-%m-%d")
        last_year_date = date - timedelta(days=365)
        return last_year_date.strftime("%Y-%m-%d")
    
# today = str(datetime.date.today())
# today = "2008-02-29"

# lastyear = get_last_year(today)

# print(lastyear)