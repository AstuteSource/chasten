# Import necessary modules and components from the Textual library,
# as well as other Python modules like os and validation tools.
from pathlib import Path
from typing import List

from textual.app import App, ComposeResult
from textual.validation import Number
from textual.widgets import Button, Input, Pretty, Static

from chasten import constants

CHECK_STORAGE = constants.chasten.App_Storage
# Define default values for checking and exact status
Check = [
    "",
    "1",
    False,
]  # Check[0] stores "Check For:", Check[1] stores "Matches", Check[2] stores if you want exact checks
Valid = False
# Constants to map input field names to their positions in the Check list
CHECK_VALUE = {
    "Check": 0,
    "Matches": 1,
}

def split_file(file_name: Path) -> List[List[str]]:
    """Split a csv file into a list of lists."""
    check_list = []
    with open(file_name) as file:
        for row in file:
            strip_row = row.strip()  # Remove leading/trailing white spaces
            if strip_row:
                check_list.append(strip_row.split(","))
    return check_list


def write_checks(check_list: List[List[str]]) -> str:
    """Generate structured output based on the contents of the file."""
    if len(check_list) != 0:
        result = "Make a YAML file that checks for:"
        for checks in check_list:
            quantity = "exactly" if checks[2] == "True" else "at minimum"
            result += f"\n - {quantity} {checks[1]} {checks[0]}"
        return result
    return "[red][ERROR][/red] No checks were supplied"


def store_in_file(File: Path, Pattern: str, Matches: int, Exact: bool):
    """Store inputed values into a text file"""
    File.touch()
    with open(File, "a") as file:
        file.write(
            f"\n{Pattern},{Matches},{Exact}"
        )  # Append input data to the file

# Define input fields and buttons for the user interface
Check_Input = Input(placeholder="Check For:", id="Check", name="Check")
Match_Input = Input(
    placeholder="How many matches do you expect",
    id="Matches",
    name="Matches",
    validators=Number(1, 500),  # Validate that Matches is a number between 1 and 500
)
Exact_button = Button("Exact", id="Exact")  # Button to trigger an action


# Static widget to display user input and validation results
class answers(Static):
    def on_input_changed(self, event: Input.Changed) -> bool:
        """When inputs change this updates the values of Check"""
        global Check, Valid  # noqa: PLW0602, PLW0603
        Valid = False
        if event.input.id == "Check":
            Check[CHECK_VALUE[event.input.name]] = event.input.value
        elif event.validation_result.is_valid:
            Check[CHECK_VALUE[event.input.name]] = event.input.value
            Valid = True
        return Valid

    def compose(self) -> ComposeResult:
        """For displaying the user interface"""
        yield Check_Input
        yield Match_Input


# Static widget to display buttons for user interactions
class button_prompts(Static):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """When a button is pressed this function determines what to do"""
        global Check, Valid  # noqa: PLW0602, PLW0603
        if event.button.id == "Exact":
            Check[2] = True  # Mark the "Exact" button as clicked
            event.button.disabled = True  # Disable the "Exact" button after clicking
        elif event.button.id == "done":
            config_App.exit(
                self
            )  # Exit the application if the "Done" button is clicked
        elif event.button.id == "clear":
            with open(CHECK_STORAGE, "w") as file:
                file.write(
                    ""
                )  # Clears Checks.txt file when "Clear Check" button is clicked
        elif Valid:
            if event.button.id == "next":
                # If "Next Check!" is clicked and input is valid, record the input data to a file
                store_in_file(CHECK_STORAGE,Check[0],Check[1],Check[2])
                Check = ["", "1", False]
                # Reset input fields, clear validation messages, and enable the "Exact" button
                self.query_one(Pretty).update([])  # Clear any validation messages
                Exact_button.disabled = False  # Re-enable the "Exact" button
                Check_Input.value = ""
                Match_Input.value = ""  # Refresh the application UI
        else:
            self.query_one(Pretty).update(["Invalid Input Please enter a Integer"])
            Match_Input.value = ""  # Clear the "Matches" input field

    def compose(self) -> ComposeResult:
        """For displaying the user interface"""
        yield Pretty([])  # Widget to display validation messages
        yield Exact_button  # Display the "Exact" button
        yield Button("Submit Check!", id="next")  # Display the "Next Check!" button
        yield Button("Done!", id="done")  # Display the "Done!" button
        yield Button("Clear Checks", id="clear", variant="error")


# Custom App class for the Textual application
class config_App(App):
    CSS = """
    Screen {
        layout: horizontal;
    }
    answers {
        width: 100%;
        align: center top;
        dock: top;
        background: $boost;
        min-width: 50;
        padding: 1;
        border: wide black;
    }
    button_prompts {
        background: $boost;
        layout: vertical;
        margin: 1;
        align: left top;
        border: wide black;
        width: 100%;
    }
    Button {
        background: rgb(245, 184, 50);
        content-align: center top;
        height: 3;
        width: 100%;
    }
    Button:hover {
        background: white;
        color: black;
    }
    """

    def compose(self) -> ComposeResult:
        """For displaying the user interface"""
        yield answers()  # Display the input fields for user input
        yield button_prompts()  # Display the buttons for user interaction
