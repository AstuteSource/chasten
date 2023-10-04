from typing import List


class ProperSentence:
    def __init__(self, file_name: str):
        """Initialize the ProperSentence object with a file name."""
        self.file_name = file_name

    def split_file(self) -> List[List[str]]:
        """Split the file into a list of lists containing comma-separated values."""
        check_list = []
        with open(self.file_name) as file:
            for row in file:
                row = row.strip()  # Remove leading/trailing white spaces
                if row:
                    check_list.append(row.split(","))
        return check_list

    def sentence_structure(self) -> str:
        """Generate a sentence based on the content of the file."""
        check_list = self.split_file()
        result = "Make a YAML file that checks for:"
        for checks in check_list:
            quantity = "exactly" if checks[2] == "True" else "at least"
            result += f"\n - {quantity} {checks[1]} {checks[0]}"
        return result
