import os
from Assembler import Assembler


if __name__ == "__main__":
    assembler = Assembler()

    read_file_path = input(f"Directory of .asm files (will also scan sub-dirs):\n")
    write_file_path = input(f"Directory to write all translated .hack files:\n")

    for root, dirs, files in os.walk(read_file_path):
        for file in files:
            if file.endswith(".asm"):
                full_file_path = os.path.join(root, file)
                machine_file = assembler.assemble(full_file_path)

                new_file_name = os.path.splitext(file)[0] + ".hack"
                new_file_path = os.path.join(write_file_path, new_file_name)

                with open(new_file_path, "w") as f:
                    f.write(machine_file)
