from notes import Note, NotesBook
from constants import GREEN, RESET
from main import add_note, show_notes, add_tag, delete_note


if __name__ == "__main__":
    note_book = NotesBook()

    print(GREEN + "     створюємо нову нотатку" + RESET)
    print(add_note("zero", "If you don’t have "))
    
    print(GREEN + "     створюємо нову нотатку з #tag" + RESET)
    print(add_note("first", "If you don’t have ", "#3"))
    
    print(GREEN + "      видаляємо нотатку"  + RESET)
    print(delete_note("first"))
    
    print(GREEN + "     створюємо нову нотатку з #tag" + RESET)
    print(add_note("first", "If you don’t have ", "#3"))
    
    print(GREEN + "     створюємо нову нотатку з двома #tags" + RESET)
    print(add_note("second", "If you don’t have ", "#3", "#5"))
    
    
    
    
    print(GREEN + "     додаємо #tags" + RESET)
    print(add_tag("first", "#8"))
    
    print(GREEN + "     додаємо #tags" + RESET)
    print(add_tag("second", "#8"))
    
    

    print(show_notes())
