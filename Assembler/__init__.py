"""
Assembler translates HACK assembly language into machine language.
1. get .hack doc path from user
2. read contents of doc
3. first run: for each line in doc, add labels to symbol dict
"""

from . import pre_defined


class Assembler:
    def __init__(self):
        self._symbols_table = pre_defined.symbols

    def assemble(self, file_path):
        self._n = 16
        # store contents of file
        with open(file_path, "r") as f:
            self._assembly_file = f.read()
        print("Initial assembly file: \n" + self._assembly_file + "\n")

        # remove whitespaces, empty lines and comments from file
        self.__clean_file()
        print("Cleaned assembly file: \n" + self._assembly_file + "\n")

        # add all labels and variables occuring in the file to the symbols table
        self.__fill_symbols_table()

        self.__create_machine_file()
        print("Machine language file: \n" + self._machine_file)

        return self._machine_file

    def __clean_file(self):
        """
        Remove all comments, white spaces, and empty lines from the file.
        """
        clean_lines = []
        for line in self._assembly_file.split("\n"):
            # Remove comments (anything after a '//')
            line = line.split("//")[0]

            # Remove leading and trailing white spaces
            line = line.strip()

            # Skip empty lines
            if line:
                clean_lines.append(line)

        # Join lines back into a single string
        self._assembly_file = "\n".join(clean_lines)

    def __fill_symbols_table(self):
        self.__add_labels_to_symbols_table()
        print("Symbols table with labels: ", self._symbols_table)
        self.__add_variables_to_symbols_table()
        print("Symbols table with variables: ", self._symbols_table)

    def __add_labels_to_symbols_table(self):
        line_number = 0
        for line in self._assembly_file.split("\n"):
            if line[0] == "(":
                # line is a label, so add label to table
                label = line.split("(")[1].split(")")[0]
                self._symbols_table[label] = line_number
            else:
                line_number += 1

    def __add_variables_to_symbols_table(self):
        for line in self._assembly_file.split("\n"):
            if line[0] == "@":
                # line is a variable, so add variable to table
                variable_name = line.split("@")[1]
                is_integer = variable_name.isdigit()
                if not is_integer and not variable_name in self._symbols_table.keys():
                    self._symbols_table[variable_name] = self._n
                    self._n += 1

    def __create_machine_file(self):
        binary_lines = []
        for line in self._assembly_file.split("\n"):
            if line[0] != "(":
                if line[0] == "@":
                    binary_line = self.__translate_A_instruction(line)
                else:
                    binary_line = self.__translate_C_instruction(line)
                binary_lines.append(binary_line)

        self._machine_file = "\n".join(binary_lines)

    def __translate_A_instruction(self, line):
        variable = line.split("@")[1]
        address = (
            self._symbols_table[variable] if not variable.isdigit() else int(variable)
        )

        binary_instruction = bin(address)[2:].zfill(16)
        if variable == "ponggame.0":
            print("lululu", address, binary_instruction)

        return binary_instruction

    def __translate_C_instruction(self, line):
        dest, jump, comp = None, None, None

        if "=" in line:
            dest, line = line.split("=")

        if ";" in line:
            line, jump = line.split(";")

        comp = line

        if comp is None:
            raise ValueError("Invalid C-instruction format: missing comp!")

        try:
            comp_code = pre_defined.comp_mnemonics[comp]
            dest_code = pre_defined.dest_mnemonics[dest]
            jump_code = pre_defined.jump_mnemonics[jump]
        except KeyError as e:
            raise ValueError(f"Invalid mnemonics: {e}")

        binary_instruction = "111" + comp_code + dest_code + jump_code

        return binary_instruction
