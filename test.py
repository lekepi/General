from utils import get_eom, get_next_eom, find_future_date
from datetime import date

if __name__ == '__main__':
    start_date = date(2022, 12, 1)
    my_date = get_next_eom(start_date)
    print(my_date)
