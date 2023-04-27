from datetime import timedelta, date
from models import session, TaskChecker


def task_checker_db(status, task_details, comment='', task_name='Get EMSX Trade', task_type='Task Scheduler ', only_new=False):
    if comment != '':
        comment_db = comment
    else:
        comment_db = 'Success'
    add_db = True
    if only_new:
        my_task = session.query(TaskChecker).filter(TaskChecker.task_details == task_details)\
                                            .filter(TaskChecker.status == status)\
                                            .filter(TaskChecker.active == 1).first()
        if my_task:
            add_db = False
    if add_db:
        new_task_checker = TaskChecker(
            task_name=task_name,
            task_details=task_details,
            task_type=task_type,
            status=status,
            comment=comment_db
        )
        session.add(new_task_checker)
        session.commit()

    if status == 'Success':
        session.query(TaskChecker).filter(TaskChecker.task_details == task_details) \
            .filter(TaskChecker.status == 'Fail').filter(TaskChecker.active == 1).delete()
        session.commit()



def find_future_date(my_date, days):
    cur_date = my_date
    nb_days = days
    while nb_days > 0:
        cur_date += timedelta(days=1)
        if cur_date.weekday() < 5:
            nb_days -= 1
    return cur_date


def find_past_date(my_date, days):
    cur_date = my_date
    nb_days = days
    while nb_days > 0:
        cur_date -= timedelta(days=1)
        if cur_date.weekday() < 5:
            nb_days -= 1
    return cur_date


def get_eom(my_date):
    if my_date.month == 12:
        last_date = date(my_date.year + 1, 1, 1) - timedelta(days=1)
    else:
        last_date = date(my_date.year, my_date.month + 1, 1) - timedelta(days=1)
    # if sunday go back
    if last_date.weekday() == 6:
        last_date = last_date - timedelta(days=1)
    return last_date


def get_next_eom(my_date):
    # get a date for next month
    next_month = my_date.month + 1
    if next_month == 13:
        next_month = 1
        next_year = my_date.year + 1
    else:
        next_year = my_date.year
    next_month_date = date(next_year, next_month, 1)
    last_date = get_eom(next_month_date)
    if last_date.weekday() == 6:
        last_date = last_date - timedelta(days=1)
    #   last_date -= timedelta(days=last_date.weekday() - 4)
    return last_date
