from datetime import date, timedelta

from .classes import (
    Name,
    Phone,
    Email,
    Address,
    Record,
    AddressBook,
    BirthDay,
    PhoneError,
    BDayError,
    EmailError,
    NoContactError,
)

from .constants import RED, RESET

def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except TypeError:
            return f"{RED}not enough params{RESET}\n\tFormat: '<command> <number of days>'\n\tUse 'help' for information"
        except AttributeError:
            return f"{RED}Address book not created. Please create Address book first{RESET}"
    return inner

def get_period(start_date: date, days: int) -> dict:
    result = {}
    for _ in range(days + 1):
        result[start_date.day, start_date.month] = start_date.year
        start_date += timedelta(1)
    return result

@user_error
def get_birthdays_on_date(users: AddressBook, days=None):
    Birthday_people = []

    if not days:
        days = 0

    start_date = date.today()
    period = get_period(start_date, days)

    for name, record in users.data.items():
        try:
            birthday: date = record.birthday.value
        except AttributeError:
            continue
        date_birthday = birthday.day, birthday.month
        if date_birthday in list(period):
            Birthday_people.append(record)

    if not Birthday_people:
        if not (days == 0 or days == 1):
            return (f"  === No any contacts with Birthdays in the next {days} days ===")
        else:
            return ("  === No any contacts with Birthdays today ===")
    else:
        if days == 0 or days == 1:
            print(f"  === Contacts with Birthdays today ===")
            for b_p in Birthday_people:
                print(b_p)
        else:
            print(f"  === Contacts with Birthdays in the next {days} days ===")
            for b_p in Birthday_people:
                print(b_p)

    return "  --- End of List ---"