import sys

# List of supported mnemonics
mnemonics = {
    "add": "00000", "sub": "00001", "mov_imm": "00010", "mov_reg": "00011",
    "ld": "00100", "st": "00101", "mul": "00110", "div": "00111",
    "rs": "01000", "ls": "01001", "xor": "01010", "or": "01011",
    "and": "01100", "not": "01101", "cmp": "01110",
    "jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111", "hlt": "11010"
}

# Dictionary to store variable names and their memory addresses
variables = {}

# Dictionary to store label names and their memory addresses
labels = {}

# Initialize the program counter
program_counter = 0

# Function to convert a decimal number to a binary string of specified length
def dec2bin(num, length):
    binary = bin(num)[2:]
    return binary.zfill(length)

# Function to convert a 16-bit binary string to a decimal number
def bin2dec(binary):
    return int(binary, 2)

# Function to parse the instruction and generate the corresponding binary code
def parse_instruction(instruction):
    global program_counter

    parts = instruction.strip().split()

    # Ignore empty lines and variable definitions
    if len(parts) == 0 or parts[0] == "var":
        return None

    # Check for label definition
    if parts[0].endswith(":"):
        label = parts[0][:-1]
        if label in labels:
            print(f"Error: Duplicate label '{label}'")
            sys.exit(1)
        labels[label] = program_counter
        parts = parts[1:]

    # Check for instruction
    if len(parts) > 0:
        mnemonic = parts[0]
        opcode = mnemonics.get(mnemonic)
        if opcode is None:
            print(f"Error: Unknown mnemonic '{mnemonic}'")
            sys.exit(1)

        if opcode == "11010" and program_counter != 0:
            print(f"Error: 'hlt' instruction must be the last instruction")
            sys.exit(1)

        # Check if the instruction has the correct number of arguments
        if len(parts) != 4:
            print(f"Error: Invalid number of arguments for '{mnemonic}'")
            sys.exit(1)

        # Parse the instruction fields
        reg1 = parts[1]
        reg2 = parts[2]
        reg3 = parts[3]

        # Validate register names
        if not (reg1.startswith("R") and reg2.startswith("R") and reg3.startswith("R")):
            print(f"Error: Invalid register name in '{mnemonic}'")
            sys.exit(1)

        reg1 = int(reg1[1:])
        reg2 = int(reg2[1:])
        reg3 = int(reg3[1:])

        # Generate the binary code for the instruction
        binary_code = opcode + dec2bin(reg1, 3) + dec2bin(reg2, 3) + dec2bin(reg3, 3)
        program_counter += 1
        return binary_code

    return None

# Main program
if _name_ == "_main_":
    # Read the assembly program from stdin
    assembly_program = sys.stdin.readlines()

    # Remove comments and empty lines from the program
    assembly_program = [line.split("#")[0].strip() for line in assembly_program if line.strip() and not line.strip().startswith("#")]

    # Pass 1: Process label definitions and variable declarations
    for line in assembly_program:
        parts = line.strip().split()

        if len(parts) > 0:
            if parts[0] == "var":
                # Variable declaration
                if len(parts) != 3:
                    print("Error: Invalid variable declaration")
                    sys.exit(1)
                variable_name = parts[1]
                variable_address = int(parts[2])
                if variable_name in variables or variable_name in labels:
                    print(f"Error: Duplicate variable or label '{variable_name}'")
                    sys.exit(1)
                variables[variable_name] = variable_address
            elif parts[0].endswith(":"):
                # Label definition
                label = parts[0][:-1]
                if label in labels or label in variables:
                    print(f"Error: Duplicate variable or label '{label}'")
                    sys.exit(1)
                labels[label] = program_counter
                program_counter += 1

    # Pass 2: Generate binary code for instructions
    binary_code = []
    for line in assembly_program:
        instruction = parse_instruction(line)
        if instruction is not None:
            binary_code.append(instruction)

    # Output the generated binary code
    for instruction in binary_code:
        print(instruction)