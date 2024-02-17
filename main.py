from abc import ABC, abstractmethod

from classes import (
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
from constants import (
    TITLE,
    FILENAME,
    NOTE_FILENAME,
    HELP_LIST,
    HELP_LIST_ADD,
    HELP_LIST_EDIT,
    HELP_LIST_DEL,
    HELP_LIST_CONTACT,
    HELP_LIST_PHONE,
    HELP_LIST_NOTE,
    HELP_LIST_FIND,
    RED,
    BLUE,
    YELLOW,
    CYAN,
    GRAY,
    WHITE,
    RESET,
    MAGENTA,
)

from notes import NotesBook, NoteError, Title, Content, Tags, Note


from prompt_toolkit.completion import NestedCompleter

from prompt_toolkit import prompt

from sort_path import sorting

book = AddressBook()
notes = NotesBook()


class NewPrint(ABC):
    @abstractmethod
    def printer(our_data):
        print(our_data)


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return f"{RED}not enough params{RESET}\n\tFormat: '<command> <name> <args>'\n\tUse 'help' for information"
        except KeyError:
            return f"{RED}Unknown name {args[0]}. Try another or use help{RESET}"
        except ValueError:
            return f"{RED}time data does not match format 'dd-mm-YYYY' (dd<=31, mm<=12){RESET}"
        except BDayError:
            return f"{RED}time data does not match format 'dd-mm-YYYY' (dd<=31, mm<=12) {RESET}"
        except PhoneError:
            return f"{RED}the phone number must contains only digits, format: '0671234567' or '+380671234567'{RESET}"
        except EmailError as ee:
            return f"{RED} {ee}{RESET}"
        # except AttributeError:
        #    return f"{RED}phone number {args[1]} is not among the contact numbers of {args[0]} {RESET}"
        except AttributeError as ae:
            return f"{RED} {ae}{RESET}"
        except TypeError as ve:
            return f"{RED} {ve}{RESET}"
        except NoteError as ne:
            return f"{RED} {ne}{RESET}"

    return inner


def get_record_or_error(name, book, return_error=False):
    name_rec = Name(name)
    rec = book.get(str(name_rec))
    if not rec:
        error_message = (
            f"{RED}contact {WHITE}{name}{RED} not found in address book{RESET}"
        )
        if return_error:
            return error_message
        else:
            return rec
    return rec


@user_error
def add_birthday(*args):
    if get_record_or_error(args[0], book):
        return get_record_or_error(args[0], book).add_birthday((args[1]))
    else:
        return f"{RED}contact {WHITE}{args[0]}{RED} not found in address book{RESET}"


@user_error
def add_address(*args):
    if get_record_or_error(args[0], book):
        addr_str = ""
        # join args with " " starting from 1
        addr_str = " ".join(args[1:])
        print(addr_str)
        return get_record_or_error(args[0], book).add_address((addr_str))
    else:
        return f"{RED}contact {WHITE}{args[0]}{RED} not found in address book{RESET}"


@user_error
def add_email(*args):
    if get_record_or_error(args[0], book):
        return get_record_or_error(args[0], book).add_email(args[1])
    else:
        return f"{RED}contact {WHITE}{args[0]}{RED} not found in address book{RESET}"


@user_error
def add_contact(*args):
    if get_record_or_error(args[0], book):
        return f"{RED}contact {Name(args[0])} already exist{RESET}\n\t{get_record_or_error(args[0], book)}\n\tUse 'add_phone' or 'change' command to add or change the phone"
    book.add_record(Record(args[0]))

    if len(args) > 1:
        if all([args[-1][2] == args[-1][5] == "-", len(args[-1]) == 10]):
            add_birthday(args[0], args[-1])
            args = args[:-1]
        add_phones(args[0], *args[1:])

    return f"contact {Name(args[0])} has been successfully added \n\t{get_record_or_error(args[0],book)}"


@user_error
def add_few_phones(rec, *args):
    result = ""
    for phone in args:
        rec.add_phone(phone)
        result += (
            f"phone number {Phone(phone)} has been added to {rec.name}'s contact list\n"
        )
    return result


@user_error
def add_phones(*args):
    rec = get_record_or_error(args[0], book)
    if rec:
        return add_few_phones(rec, *args[1:]) + f"\t{rec}"
    else:
        return f"{RED}contact {WHITE}{args[0]}{RED} not found in address book{RESET}"


@user_error
def change_name(*args):
    return book.change_name((args[0]), args[1])


@user_error
def change_phone(*args):
    if get_record_or_error(args[0], book):
        return get_record_or_error(args[0], book).edit_phone(
            Phone(args[1]), Phone(args[2])
        )
    else:
        return f"{RED}contact {WHITE}{args[0]}{RED} not found in address book{RESET}"


@user_error
def change_email(*args):
    if get_record_or_error(args[0], book):
        return get_record_or_error(args[0], book).edit_email(
            Email(args[1]), Email(args[2])
        )
    else:
        return f"{RED}contact {WHITE}{args[0]}{RED} not found in address book{RESET}"


@user_error
def del_phone(*args):
    if get_record_or_error(args[0], book):
        return get_record_or_error(args[0], book).remove_phone(Phone(args[1]))
    else:
        return f"{RED}contact {WHITE}{args[0]}{RED} not found in address book{RESET}"


@user_error
def del_email(*args):
    if get_record_or_error(args[0], book):
        return get_record_or_error(args[0], book).remove_email(Email(args[1]))
    else:
        return f"{RED}contact {WHITE}{args[0]}{RED} not found in address book{RESET}"


@user_error
def change_address(*args):
    if get_record_or_error(args[0], book):
        return get_record_or_error(args[0], book).edit_address(args[1])
    else:
        return f"{RED}contact {WHITE}{args[0]}{RED} not found in address book{RESET}"


@user_error
def del_address(*args):
    if get_record_or_error(args[0], book):
        return get_record_or_error(args[0], book).remove_address()
    else:
        return f"{RED}contact {WHITE}{args[0]}{RED} not found in address book{RESET}"


@user_error
def delete_record(*args):
    return book.delete_record(args[0])


@user_error
def name_find(*args):
    return book.find_name(args[0])


# --- Notes
@user_error
def add_tag(*args):
    title = args[0]
    tags = list(args[1:])
    return notes.add_tags(title, tags)


def search_notes_by_tag(notes, tag):
    return notes.search_notes_by_tag(tag)


# @user_error
# def search_notes_by_tag(*args):
#     tag = args[0]
#     sort_by_keywords = args[1:].lower() == "true" if len(args) > 1 else False
#     return notes.search_notes_by_tag(tag, sort_by_keywords)


@user_error
def add_note(*args):
    title = args[0]
    content_start_index = 1
    tags = []

    # теги в аргументах
    content_words = []
    for arg in args[content_start_index:]:
        if arg.startswith("#"):
            tags.append(arg)
        else:
            content_words.append(arg)

    content = " ".join(content_words)

    return notes.add_note(title, content, tags)


@user_error
def edit_note(title, *args):
    # Перевірка наявності тайтлу в 
    new_content = ' '.join(args) 
    print(f"{new_content = }")
    if title in notes.data:
        # Змінюємо тільки content
        notes.data[title].content.edit_content(new_content)
        return f"Note '{title}' changed. New content: '{new_content}'\n\t{notes.data[title]}"
    else:
        return f"note '{title}' not found."


@user_error
def search_notes(keyword, notes):
    matching_notes = [
        f"Note 'Title: {title}' Content: {note.content} Tags:{', '.join(note.tags)}"
        for title, note in notes.items()
        if keyword.lower() in title.lower() or keyword.lower() in note.content.lower()
    ]
    if matching_notes:
        return "\n".join(matching_notes)
    else:
        return "No matching notes found."


@user_error
def delete_note(*args):
    title = args[0]
    return notes.delete_note(title)


def add_content(*args):  # воно ж change_content
    ...

def del_content(*args):  # а воно треба??? - а нащо лишати заголовок, тег без опису?
    ...


@user_error
def change_tag(*args):
    search_title = args[0]
    search_tag = args[1]
    new_tag = args[2]
    return notes.change_tags(search_title, search_tag, new_tag)


@user_error
def delete_tag(*args):
    search_title = args[0]
    search_tag = args[1]
    return notes.delete_tags(search_title, search_tag)


# --- Notes end


@user_error
def search(*args):
    result = ""
    if not args:
        return f"{RED}searching string is required{RESET}"
    seek = args[0].lower()
    for record in book.data.values():
        if seek.isdigit():
            if record.seek_phone(seek):
                result += f"\t{BLUE}[   Phone match] {RESET}{record}\n"
            if record.birthday:
                date_str = record.birthday.value.strftime("%d-%m-%Y")
                if date_str.find(seek) != -1:
                    result += f"\t{MAGENTA}[Birthday match] {RESET}{record}\n"

        if seek in record.name.value.lower():
            result += f"\t{CYAN}[ Name match] {RESET}{record}\n"
        if record.seek_email(seek):
            result += f"\t{BLUE}[Email match] {RESET}{record}\n"
        if record.address:
            addr_str = record.address.value.lower()
            if addr_str.find(seek) != -1:
                result += f"\t{GRAY}[ Address match] {RESET}{record}\n"

    if result:
        return f"data found for your request '{seek}': \n{result[:-1]}"
    else:
        return f"{RED}nothing was found for your request '{seek}'{RESET}"


@user_error
def show_all(*args):
    pages = int(args[0]) if args else len(book.data)
    print(f"  === Address book ===")
    count = 0
    for _ in book.iterator(pages):
        for item in _:
            print(item)
            count += 1
        if count < len(book):
            input(f"  Press Enter for next page: ")
    return "  --- End of List ---"


@user_error
def show_notes(*args):
    pages = int(args[0]) if args else len(notes.data)
    print(f"  === Notes ===")
    count = 0
    for _ in notes.iterator(pages):
        for item in _:
            print(item)
            count += 1
        if count < len(notes):
            input(f"  Press Enter for next page: ")
    return "  --- End of List ---"


def help_part(*args):
    help_list = []
    for i in args[0]:
        help_list.append(HELP_LIST[i])
    return "\n".join(help_list)


# ===== helps =====
def help_page(*_):
    return help_part(range(len(HELP_LIST)))


def add(*_):
    return help_part(HELP_LIST_ADD)


def change(*_):
    return help_part(HELP_LIST_EDIT)


def delete(*_):
    return help_part(HELP_LIST_DEL)


def contact(*_):
    return help_part(HELP_LIST_CONTACT)


def phone(*_):
    return help_part(HELP_LIST_PHONE)


def note(*_):
    return help_part(HELP_LIST_NOTE)


def find(*_):
    return help_part(HELP_LIST_FIND)


# ===== helps =====


def say_hello(*_):
    return (
        BLUE + TITLE + RESET + "\t\tType 'help' for information\n   How can I help you?"
    )


def say_good_bay(*_):
    print(book.write_contacts_to_file(FILENAME))
    exit("Good bye!")


def unknown(*_):
    return f"{RED}Unknown command. Try again{RESET}"



def birthday(days=0):
    list_birthday = []
    result = f'  === Contacts whose birthday is {"in the next "+str(days)+" days" if days else "today"} ===\n'
    for item in book:
        rec = get_record_or_error(item, book)
        if rec.birthday:
            if int(rec.days_to_birthday(rec.birthday)[0]) <= int(days):
                list_birthday.append(rec)
    if len(list_birthday) == 0:
        return f'{RED}there are no contacts whose birthday is {"in the next "+str(days)+" days" if days else "today"}{RESET}'

    for rec in list_birthday:
        result += str(rec) + "\n"
    result += "  --- End of List --- "
    return result


# =============================================
#                main
# =============================================


COMMANDS = {
    add: ("add","help_add"),
    add_contact: ("add_record", "add_contact"),
    add_phones: ("add_phone", "add_phones"),
    add_birthday: ("add_birthday", "add_bd", "change_birthday", "change_bd"),
    add_address: ("add_address", "add_adr", "change_address", "change_adr"),
    add_email: ("add_email", "email_add"),
    add_note: ("add_note", "note_add"),
    add_tag: ("add_tag", "tag_add"),
    change_tag: ("change_tag", "edit_tag"),
    change: ("change", "edit"),
    change_name: ("change_name", "name_change", "edit_name"),
    change_phone: ("change_phone", "phone_change", "edit_phone"),
    change_address: ("change_address", "change_adr", "edit_address", "edit_adr"),
    change_email: ("change_email", "email_change", "edit_email"),
    edit_note: ("change_note", "note_change", "edit_note"),
    delete: ("delete", "del"),
    del_phone: ("del_phone", "delete_phone"),
    delete_record: ("delete_contact", "del_contact", "delete_record", "del_record"),
    del_address: ("delete_address", "delete_adr", "del_adr"),
    delete_tag: ("delete_tag", "del_tag"),
    del_email: ("delete_email", "del_email"),
    delete_note: ("delete_note", "del_note"),
    name_find: ("name", "find_name"),
    birthday: ("birthdays", "birthday", "find_birthdays", "bd"),
    search: ("search", "seek", "find_any"),
    help_page: ("help",),
    say_hello: ("hello", "hi"),
    show_all: ("show_all", "show", "list"),
    show_notes: ("show_notes", "show_note", "list_notes"),
    say_good_bay: ("exit", "good_bay", "by", "close", "end"),
    contact: ("contact", "help_contact", "help_record"),
    phone: ("phone", "help_phone"),
    note: ("note", "help_note"),
    find: ("find",),
    sorting: ("sorting", "sort_path"),
}


def parser(text: str):
    for func, cmd_tpl in COMMANDS.items():
        for command in cmd_tpl:
            data = text.strip().lower().split()
            if len(data) < 1:
                break
            if data[0] == command:
                return func, data[1:]
    return unknown, []


def func_completer(CMD):
    comp_dict = {}
    # sorted_command = []
    # for i in CMD.values():
    #     for k in i:
    #         sorted_command.append(k)
    sorted_command = [
        # 'add_record',
        "add_contact",
        "add_phone",
        # "add_phones",
        "add_birthday",
        "add_address",
        "add_email",
        "add_note",
        "add_tag",
        "change_birthday",
        "change_address",
        "change_name",
        # "change_address",
        "change_phone",
        "change_email",
        "change_note",
        "change_tag",
        "edit_birthday",
        "edit_address",
        "edit_name",
        "edit_phone",
        "edit_email",
        "edit_note",
        "edit_tag",
        "delete_contact",
        "delete_phone",
        # "delete_record",
        "delete_address",
        "delete_email",
        "delete_note",
        "delete_tag",
        "find_name",
        "birthdays",
        "search",
        "find_any",
        "help",
        "show",
        "list",
        "show_notes",
        "list_notes",
        "exit",
        "close",
        "sort_path",
    ]
    for i in sorted_command:
        # print(f"'{i}',")
        comp_dict.update({i: None})
    return comp_dict


completer = NestedCompleter.from_nested_dict(func_completer(COMMANDS))


def main():
    global book
    global notes
    book = book.read_contacts_from_file(FILENAME)
    notes = notes.read_notes_from_file(NOTE_FILENAME)
    NewPrint.printer(say_hello())
    while True:
        user_input = prompt(">>>", completer=completer)
        # user_input = input(f"{BLUE}>>{YELLOW}>>{RESET}")
        func, data = parser(user_input.strip().lower())
        NewPrint.printer(func(*data))
        if func not in [
            say_good_bay,
            show_all,
            show_notes,
            say_hello,
            help_page,
            search,
            name_find,
            birthday,
        ]:
            book.write_contacts_to_file(FILENAME)
            notes.write_notes_to_file(NOTE_FILENAME)


if __name__ == "__main__":
    main()
