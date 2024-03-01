from tkinter import Button as TkButton
from tkinter_qu.gui_components.component import Component
from tkinter_qu.base.colors import *


class Button(TkButton, Component):
    """A button for any application (adds some helper methods from Component to an existing TkButton)"""

    def __init__(self, window_type, text, font, background_color=white, text_color=black):
        """Initializes a button"""

        super().__init__(window_type, text=text, font=font, bg=background_color, fg=text_color)

    def set_command(self, command):
        """Sets the command that is called when the button is clicked (uses the one parameter tkinter config method)"""

        self.configure(command=command)
