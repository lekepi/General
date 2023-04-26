from datetime import timedelta
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


