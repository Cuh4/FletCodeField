# ----------------------------------------
# Code Field
# ----------------------------------------

# A Flet control that allows you to type code with syntax highlighting.
# Repo: https://github.com/Cuh4/FletCodeField

"""
Copyright (C) 2024 Cuh4

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# ---- // Imports
import flet

# ---- // Main
class CodeField(flet.Container):
    """
    A custom TextField with proper syntax highlighting. Uses flet.Markdown() under the hood.
    This only works with Windows (tested), MacOS (untested, but should work), and Linux (untested, but should work).
    
    Params:
        text: str -> The default text to display in the code field.
        code_theme: str -> The color theme to be used. Accepted values: https://flet.dev/docs/controls/markdown/#code_theme
        show_language_text: bool -> Whether to show the language text.
        language_text_color: str -> The color of the language text.
        show_line_numbers: bool -> Whether to show line numbers.
        line_number_text_color: str -> The color of the line number text.
        allow_pasting: bool -> Whether to allow pasting (CTRL + V).
        show_focus_border: bool -> Whether to show the focus border upon the code field being focused.
        focus_border_color: str -> The color of the focus border.
        tab_spacing: int -> The amount of spaces to add when the user presses tab.
        font_size: int -> The size of the font.
        font: str -> The name of the font.
        letter_spacing: int|float -> The spacing between letters.
        language: str -> The language to be used for syntax highlighting.
        custom_shift_mapping: dict[str, str] -> A dictionary containing keys as the index, and values as the version of the key when shift is held. Example: {"1" : "!", ...}. Omitting this argument will use the UK layout mapping.
        
    Events:
        on_focus: function(focused: bool) -> Fired when the code field is clicked.
        on_change: function(text: str) -> Fired when the user types.
    """
    def __init__(self, text: str = "print('hello world')", code_theme: str = "obsidian", show_language_text: bool = True, language_text_color: str = flet.colors.GREY, show_line_numbers: bool = True, line_number_text_color: str = flet.colors.WHITE, allow_pasting: bool = True, show_focus_border: bool = True, focus_border_color: str = flet.colors.BLUE_400, tab_spacing: int = 4, font_size: int = 10, font: str = "Roboto Mono", letter_spacing: int|float = 0, language: str = "python", custom_shift_mapping: dict[str, str] = None):
        # // attributes
        self.text = text
        self.code_theme = code_theme
        self.show_language_text = show_language_text
        self.language_text_color = language_text_color
        self.show_line_numbers = show_line_numbers
        self.line_number_text_color = line_number_text_color
        self.allow_pasting = allow_pasting
        self.show_focus_border = show_focus_border
        self.focus_border_color = focus_border_color
        self.tab_spacing = tab_spacing
        self.font_size = font_size
        self.font = font
        self.letter_spacing = letter_spacing
        self.language = language
        self.custom_shift_mapping = custom_shift_mapping

        if self.custom_shift_mapping is None:
            self.custom_shift_mapping = {
                "1": "!",
                "2": "\"",
                "3": "£",
                "4": "$",
                "5": "%",
                "6": "^",
                "7": "&",
                "8": "*",
                "9": "(",
                "0": ")",
                "-" : "_",
                "=" : "+",
                
                "[" : "{",
                "]" : "}",
                ";" : ":",
                "'" : "@",
                "#" : "~",
                "," : "<",
                "." : ">",
                "/" : "?",
                "`" : "¬",
                "\\" : "|",
            }
        
        self.is_caps = False
        self.focused = False
        self.type_point = len(self.text)
        
        # // controls
        # create root control
        self.root = flet.Column(
            controls = [],
            expand = True,
            spacing = 0.4
        )
        
        # create language text
        self.language_text = flet.Text() # other params are added in _update_controls
        
        if self.show_language_text:
            self.root.controls.append(self.language_text)
        
        # create row containing line numbers and markdown
        self.code = flet.Row(
            controls = [],
            spacing = 0
        )
        
        self.root.controls.append(self.code)
        
        # line numbers
        self.line_numbers = flet.Column(
            controls = [],
            spacing = 0,
            width = 25
        )
        
        if self.show_line_numbers:
            self.code.controls.append(self.line_numbers)
        
        # code
        self.code_markdown = flet.Markdown(
            extension_set = flet.MarkdownExtensionSet.GITHUB_FLAVORED,
            expand = True
        )
        
        self.code_markdown_container = flet.Container(
            content = self.code_markdown,
            on_click = self.on_container_click
        )
        
        self.code.controls.append(self.code_markdown_container)

        # init
        super().__init__(content = self.root)
        
    """
    Construct a TextStyle object for the markdown.
    
    Returns:
        flet.TextStyle -> The constructed TextStyle object.
    """
    def _construct_markdown_text_style(self) -> flet.TextStyle:
        return flet.TextStyle(font_family = self.font, size = self.font_size, letter_spacing = self.letter_spacing)
        
    """
    Surrounds text in a code block.
    
    Params:
        text: str -> The text to surround.
        
    Returns:
        str -> The text surrounded in a code block.
    """
    def _code(self, text: str):
        filtered = text.replace("`", "\\`")
        return f"```{self.language}\n{filtered}\n```"
    
    """
    Set the markdown control value to self.text and update the control.
    """
    def _update_controls(self):
        # update code markdown
        self.code_markdown.value = self._code(self.text if self.text != "" else " ") # prevent 0 width
        self.code_markdown.code_theme = self.code_theme
        self.code_markdown.code_style = self._construct_markdown_text_style()

        self.code_markdown.update()
        
        # update language text
        if self.show_language_text:
            self.language_text.value = self.language.upper()
            self.language_text.font_family = self.font
            self.language_text.size = self.font_size
            self.language_text.color = self.language_text_color
            
            self.language_text.update()
        
        # update line numbers
        if self.show_line_numbers:
            lineCount = len(self.text.split("\n")) + 1
            
            self.line_numbers.controls = [flet.Text(
                value = line,
                size = self.font_size,
                font_family = self.font,
                color = self.line_number_text_color,
                bgcolor = flet.colors.TRANSPARENT,
                style = flet.TextStyle(height = 0) # important! prevents inaccuracy
            ) for line in range(1, lineCount)]
            
            self.line_numbers.update()
        
    """
    Parse a key to a proper letter.

    Params:
        letter: str -> The key that was pressed.
        isShift: bool -> Whether the shift key was pressed along with the provided key.
    """
    def _parse_letter(self, letter: str, isShift: bool):
        # handle enter
        if letter == "Enter":
            letter = "\n"
    
        # handle secondary keys
        if isShift:
            if letter in self.custom_shift_mapping:
                letter = self.custom_shift_mapping[letter]
                
        # handle keypad
        if letter.startswith("Numpad" ):
            letter = letter.replace("Numpad ", "")
            
        if letter == "Decimal":
            return "."
        
        if letter == "Add":
            return "+"
        
        if letter == "Subtract":
            return "-"
        
        if letter == "Divide":
            return "/"
        
        if letter == "Multiply":
            return "*"
        
        if letter == "Num Lock":
            return ""
        
        if len(letter) > 1:
            return ""
            
        # return
        return letter.upper() if self.is_caps or isShift else letter.lower()
    
    """
    Set the focus of this code field.
    
    Params:
        focus: bool -> Whether to focus or not.
    """
    def set_focus(self, focus: bool):
        # set focus
        self.focused = focus
        
        # fire event
        self.on_focus(focus)

        # visual representation of focus
        self.code_markdown_container.border = flet.border.all(1, self.focus_border_color) if focus and self.show_focus_border else None
        self.code_markdown_container.update()
        
    """
    Set self.type_point.
    
    Params:
        to: int -> The point to set self.type_point to.
    """
    def set_type_point(self, to: int):
        self.type_point = max(0, min(len(self.text), to))
        
    """
    Insert a letter into the text.
    
    Params:
        letter: str -> The letter to insert.
    """
    def insert_letter(self, letter: str):
        if letter == "":
            return
        
        if len(letter) > 1:
            return
        
        self.text = self.text[:self.type_point] + letter + self.text[self.type_point:]
        self.set_type_point(self.type_point + 1)
        self._update_controls()
        
        self.on_change()
        
    """
    Insert a word into the text.
    
    Params:
        word: str -> The word to insert.
    """
    def insert_word(self, word: str):
        for letter in word:
            self.insert_letter(letter)
        
    """
    Remove the letter before the type_point from the text.
    """
    def remove_letter(self):
        self.text = self.text[:self.type_point - 1] + self.text[self.type_point:]
        self.set_type_point(self.type_point - 1)
        self._update_controls()
        
        self.on_change()
        
    """
    Returns the text up to the type_point.
    
    Returns:
        str -> The text up to the type_point.
    """
    def get_text_up_to_point(self):
        return self.text[:self.type_point]
    
    """
    Returns the text after the type_point.
    
    Returns:
        str -> The text after the type_point.
    """
    def get_text_after_point(self):
        return self.text[self.type_point:]

    # ---- // Control Events
    """
    Fired when the code field is focused or unfocused.
    
    Params:
        focus: bool -> Whether the code field has been focused or not.
    """
    def on_focus(self, focus: bool):
        pass
    
    """
    Fired when the user types in the code field.
    """
    def on_change(self):
        pass

    # ---- // Flet Events
    def will_unmount(self):
        self.focused = False
        self.on_keyboard_input = None
    
    def did_mount(self):
        self._update_controls()
        
        self.page.on_keyboard_event = self.on_keyboard_input
        self.page.update()
        
    def on_container_click(self, event: flet.ControlEvent):
        self.set_focus(not self.focused)
        
    def on_keyboard_input(self, event: flet.KeyboardEvent):
        # if not listening for keyboard input, do nothing
        if not self.focused:
            return
        
        # get key
        letter = event.key

        # handle backspace
        if letter == "Backspace":
            if not event.ctrl:
                # regular backspace
                self.remove_letter()
            else:
                # remove word
                locationOfSpace = self.get_text_up_to_point().rfind(" ")

                for _ in range(self.type_point, locationOfSpace if locationOfSpace != -1 else 0, -1):
                    self.remove_letter()

            return

        # lose focus if escape is pressed
        if letter == "Escape":
            self.set_focus(False)
            return
        
        # set caps lock
        if letter == "Caps Lock":
            self.is_caps = not self.is_caps
            return
        
        # move type_point left
        if letter == "Arrow Left":
            if event.ctrl:
                textBeforePoint = self.get_text_up_to_point()
                spaceLocation = textBeforePoint.rfind(" ")
                
                self.set_type_point(spaceLocation if spaceLocation != -1 else 0)
            else:
                self.set_type_point(self.type_point - 1)
            
            return
        
        if letter == "Tab":
            self.insert_word(" " * self.tab_spacing)
            
        # move type_point right
        if letter == "Arrow Right":
            if event.ctrl:
                charactersBeforePoint = len(self.get_text_up_to_point())
                textAfterPoint = self.get_text_after_point()
                spaceLocation = textAfterPoint.find(" ")

                self.set_type_point(charactersBeforePoint + (self.type_point + spaceLocation if spaceLocation != -1 else len(textAfterPoint)))
            else:
                self.set_type_point(self.type_point + 1)
                
            return
            
        # move type_point up
        if letter == "Arrow Up":
            locationOfNewline = self.get_text_up_to_point().rfind("\n")
            self.set_type_point(locationOfNewline if locationOfNewline != -1 else self.type_point)

            return
        
        # move type_point down
        if letter == "Arrow Down":
            charactersBeforePoint = len(self.get_text_up_to_point())
            locationOfNewline = self.get_text_after_point().find("\n")
            self.set_type_point(charactersBeforePoint + (self.type_point + locationOfNewline if locationOfNewline != -1 else len(self.get_text_after_point())))

            return
        
        # handle pasting
        if event.ctrl and letter == "V":
            self.insert_word(self.page.get_clipboard(2))
            return
        
        # parse letter
        letter = self._parse_letter(letter, event.shift)
        
        if letter == "":
            return
        
        # update text input, considering self.type_point
        self.insert_letter(letter)
        
# ---- // Preview
if __name__ == "__main__":
    def main(page: flet.Page):
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"
        
        code_field = CodeField()

        page.add(
            code_field
        )
    
    flet.app(target = main)