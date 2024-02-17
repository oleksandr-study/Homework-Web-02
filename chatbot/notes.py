from collections import UserDict
from .constants import RED, GRAY, CYAN, MAGENTA, RESET, LEN_OF_NAME_FIELD
from datetime import datetime
import os.path
import pickle
from .classes import Field


class NoteError(Exception):
    ...


class Title(Field):
    ...


class Content(Field):
    def __init__(self, content):
        super().__init__(content)

    def edit_content(self, new_content):
        self.value = new_content

    def lower(self):
        return self.value.lower()


class Tags(Field):
    def __init__(self, tags=None):
        super().__init__(tags or [])

    def add_tags(self, new_tags):
        if not self.value:
            self.value = new_tags
        new_list = list(self.value)
        self.value = new_list + new_tags

    def change_tag(self, old_tag, new_tag):
        if not old_tag in self.value:
            return f"Tag {old_tag} not in Tag list"
        old_list_tag = []
        for o_t in self.value:
            old_list_tag.append(o_t)
        old_list_tag[old_list_tag.index(old_tag)] = new_tag
        self.value = old_list_tag

    def delete_tag(self, tag):
        if not tag in self.value:
            return f"Tag {tag} not in Tag list"
        self.value.remove(tag)

    # def extend(self, new_tag):
    #     # super()
    #     ...

    # def add_tags(self, new_tags):
    #     self.value.extend(new_tags)
    #     # self.value += new_tags

    def __iter__(self):
        return iter(self.value)


class Note:
    def __init__(self, title, content, tags=None):
        self.title = Title(title)
        self.content = Content(content)
        self.tags = Tags(tags) if tags else []

    # def __init__(
    #     self, title: Title, content: Content | None = None, tags: Tags | None = None
    # ) -> None:
    #     self.title = Title(title)
    #     self.content = Content(content) if content else ""
    #     self.tags = [Tags(tags)] if tags else []

    # def add_note(self, title, content):
    #     self.notes[title] = content
    #     return f"note {self.title} has been successfully added \n\t{self}"

    # def edit_note(self, title, new_content):
    #     if title in self.notes:
    #         self.notes[title] = new_content
    #         return f"Note '{title}' edited."
    #     else:
    #         return f"Note '{title}' not found."

    # def delete_note(self, title):
    #     if title in self.notes:
    #         del self.notes[title]
    #         return f"Note '{title}' deleted."
    #     else:
    #         return f"Note '{title}' not found."

    def __str__(self) -> str:
        blanks = " " * (LEN_OF_NAME_FIELD - len(str(self.title)))
        # tags_str = f"Tags {''.join(t for t in self.tags)}" if len(self.tags)>0 else ""
        tags_str = ""
        # print(f"{self.tags = }")
        if self.tags:
            tags_str = self.tags
            # print(f"{self.tags = }")
            tags_str = ", ".join(self.tags)
            # print(f"{tags_str = }")
        return f"{GRAY}•{RESET}{blanks}{CYAN}{self.title}{RESET}  {GRAY}: {RESET}{self.content} \t{MAGENTA}{tags_str}{RESET}"

    # def __str__(self) -> str:
    #     blanks = " " * (LEN_OF_NAME_FIELD - len(str(self.title)))
    #     # tags_str = f"Tags {''.join(t for t in self.tags)}" if len(self.tags)>0 else ""
    #     tags_str = ""
    #     # print(f"{self.tags = }")
    #     if self.tags:
    #         # for i in self.tags:
    #         for item in self.tags:
    #             tags_str = ", ".join(item)
    #         # print(f"{tags_str = }")
    #     return f"{GRAY}•{RESET}{blanks}{CYAN}{self.title}{RESET}  {GRAY}: {RESET}{self.content} \t{MAGENTA}{tags_str}{RESET}"


class NotesBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_note(self, title, content, tags):
        new_note = Note(title, content, tags if tags else None)
        self.data[title] = new_note
        # self.data[new_note.name.value] = new_note
        return f"Note '{title}' has been successfully added.\n\t{self.data[title]}"

    def edit_note(self, title, new_content):
        if title in self.data:
            self.data[title] = new_content
            return f"Note '{title}' edited.\n\t{self.data[title]}"
        else:
            return f"Note '{title}' not found."

    def delete_note(self, title):
        if title in self.data:
            del self.data[title]
            return f"Note '{title}' deleted."
        else:
            return f"Note '{title}' not found."

    def add_tags(self, title, tags):  # метод для додавання тегів
        if title in self.data:
            self.data[title].tags.add_tags(tags)
            return f"Tags {', '.join(tags)} added to the note with title '{title}'.\n\t{self.data[title]}"
        else:
            raise NoteError(f"Note with title '{title}' not found.")

    def change_tags(self, title, old_tag, new_tag):
        if title in self.data:
            self.data[title].tags.change_tag(old_tag, new_tag)
            return f"Tag {old_tag} has been successfully changed to {new_tag} for title '{title}'.\n\t{self.data[title]}"
        else:
            raise NoteError(f"Note with title '{title}' not found.")

    def delete_tags(self, title, tag):
        if title in self.data:
            self.data[title].tags.delete_tag(tag)
            return f"Tag {tag} has been successfully deleted for title '{title}'.\n\t{self.data[title]}"
        else:
            raise NoteError(f"Note with title '{title}' not found.")

    # def add_note(self, title, content, tags):
    #     new_note = Note(title, content, tags if tags else None)
    #     self.data[title] = new_note
    #     # self.data[new_note.name.value] = new_note

    # def add_note(self, title, content, tags):
    #     # print(f"NotesBook.add_note tags = {tags}")
    #     new_note = Note(title, content, tags if tags else None)
    #     self.data[title] = new_note
    #     # self.data[new_note.name.value] = new_note
    #     return f"Note '{title}' has been successfully added.\n\t{new_note}"

    # def edit_note(self, title, new_content):
    #     if title in self.data:
    #         self.data[title] = new_content
    #         return f"Note '{title}' edited."
    #     else:
    #         return f"Note '{title}' not found."

    # def delete_note(self, title):
    #     if title in self.data:
    #         del self.data[title]
    #         return f"Note '{title}' deleted."
    #     else:
    #         return f"Note '{title}' not found."

    # def add_tags(self, title, new_tags):  # метод для додавання тегів
    #     ...
    # print(f"1. {     new_tags = } {     title = }")
    # lst = []
    # # self.title = Title(title)
    # # self.tags = Tags(tags)
    # # print(f"2. {self.tags = } {self.title = }")
    # if title in self.data:
    #     print(f"3.{      new_tags = } {     title = }")
    #     print(f"before {self.data[title].tags = }")
    #     for i in self.data[title].tags:
    #         print(f"{i = }")
    #         # i.extend(new_tags)
    #         # i += new_tags
    #         print(f"{i = }")
    #         for k in i:
    #             print(f"{k = }")
    #             lst.append(k)

    #         print(f"{lst = }")
    #         # lst.append(new_tags[0])
    #         print(f"{lst = }")

    #         self.data[title].tags = lst
    #     print(f"after {self.data[title].tags = }")
    #     self.data[title].tags.extend(new_tags)
    #     # print(self.data[title].tags)
    #     # self.data[title].tags = Tags([tags])
    #     print(f"after after {self.data[title].tags = }")
    #     print(f"{self.data = }")
    #     return f"Tags {', '.join(new_tags)} added to the note with title '{title}'."
    # else:
    #     raise NoteError(f"Note with title '{title}' not found.")

    def search_notes_by_tag(self, tag):
        matching_notes = []
        for title, note in self.data.items():
            if tag.lower().strip() in map(str.lower, note.tags.value):
                matching_notes.append(
                    f"Note 'Title: {note.title}' Content: {note.content} Tags:{', '.join(map(str, note.tags.value))}"
                )

        if matching_notes:
            sorted_notes = sorted(matching_notes)

            return "\n".join(sorted_notes)
        else:
            return "No matching notes found."

    def search_notes(self, keyword):
        result = []
        for title, content in self.data.items():
            if keyword.lower() in title.lower() or keyword.lower() in content.lower():
                result.append(f"Title: {title}\nContent: {content}\n")
        return result if result else "No matching notes found."

    def read_notes_from_file(self, fn):
        if os.path.exists(fn):
            with open(fn, "rb") as fh:
                self = pickle.load(fh)
            self.data = dict(sorted(self.items()))
        print(f"{GRAY}the notes has been successfully restored{RESET}")
        return self

    def write_notes_to_file(self, fn):
        with open(fn, "wb") as fh:
            pickle.dump(self, fh)
        return f"{GRAY}the notes has been saved successfully{RESET}"

    def iterator(self, n=None):
        counter = 0
        while counter < len(self):
            yield list(self.values())[counter : counter + n]
            counter += n

    # def __str__(self):
    # tags_str = "".join(t.value for t in self.tags)
    # tags_str = f"Tags {tags_str}" if tags_str else ""
    # return f"Title: {self.title} Text: {self.content} {tags_str}"

    # result = []
    # for title, note in self.data.items():
    #    tags_str = ", ".join(note.tags.value) if note.tags.value else ""
    #    result.append(f"Title: {title}\nContent: {note.content}\nTags: {tags_str}\n")
    # return '\n'.join(result) if result else "No notes found."
