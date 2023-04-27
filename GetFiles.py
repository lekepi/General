import re
from datetime import date, timedelta
import os
import shutil
from utils import get_eom, get_next_eom, find_future_date


def get_reports(re_list, frequency, start_date, end_date, input_path, output_path, rename_rule):
    if frequency == 'EOM':
        current_date = get_eom(start_date)
    else:
        current_date = start_date

    while current_date <= end_date:

        year = current_date.strftime("%Y")
        month = current_date.strftime("%B")
        day = current_date.strftime("%d")

        full_input_path = os.path.join(input_path, f'{year}\\{month}\\{day}')
        os.chdir(full_input_path)
        files = filter(os.path.isfile, os.listdir(full_input_path))
        for filename in files:
            for re_item in re_list:
                if re_item.search(filename) is not None:
                    full_input_path_file = os.path.join(full_input_path, filename)
                    if rename_rule == 'Date in front':
                        new_filename = f'{current_date.strftime("%Y%m%d")}_{filename}'
                    else:
                        new_filename = filename
                    destination = os.path.join(output_path, new_filename)
                    shutil.copy(full_input_path_file, destination)

        if frequency == 'EOM':
            current_date = get_next_eom(current_date)
        else:
            current_date += timedelta(days=1)


def run_income_expense_reports():

    # 1) define the file name pattern and put them in a list:
    re_dat = re.compile(r'^SRTCS_219502_1200583322_incexpclt*_06023181_950.dat$')
    re_pdf = re.compile(r'^SRTCS_219502_1200583322_INCOMEEXPENSECLT*_06023181_942.pdf$')
    re_list = [re_dat, re_pdf]

    # 2) define the frequency and date range
    # For a specific day, put start_date=end_date and frequency = 'Day'
    # frequency = 'EOM'
    frequency = 'Day'
    start_date = date(2022, 10, 29)
    end_date = date(2022, 10, 29)
    # end_date = date.today()


    # 3) define the input and output path and renaming rule
    input_path = r'A:\Reporting Files\GS\Download'
    output_path = r'H:\Python Output\Income Expense'
    rename_rule = 'Date in front'

    # 4) run the function
    get_reports(re_list, frequency, start_date, end_date, input_path, output_path, rename_rule)


if __name__ == '__main__':
    run_income_expense_reports()
