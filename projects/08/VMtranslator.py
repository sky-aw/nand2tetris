import os                   # check if input is directory or file
import sys                  # command-line arguments, 
import parser               # parse .vm commands into nice arrays, ignores comments and blank lines
import codeWriter           # return .asm code

pathname = sys.argv[1]      # pathname can be directory or file

asm_lines = []              # array; used to print lines to .asm file at the end
asm_filename = ""           # will be set depending on whether pathname is directory or file

def main():                 # called at bottom of file; allows functions to be defined before they are called
    global asm_lines, asm_filename                      # variables that will be updated in runtime

    add_bootstrap()                                     # add preamble startup code

    if os.path.isfile(pathname):                        # if pathname is a file
        asm_filename = pathname.split(".")[0] + ".asm"  # "SimpleAdd/SimpleAdd.vm" => "SimpleAdd/SimpleAdd.asm"
        translate_file(pathname)

    elif os.path.isdir(pathname):                               # if pathname is a directory
        folder_name = pathname.strip("/").split("/")[-1]        # strip("/") to remove trailing "/" if provided
        asm_filename = pathname + "/" + folder_name + ".asm"    # "StackArithmetic/SimpleAdd/" => "StackArithmetic/SimpleAdd/SimpleAdd.asm"

        for filename in os.listdir(pathname):                   # translate all .vm files in specified directory
            if filename.endswith(".vm"):
                translate_file(pathname + "/" + filename)

    for i, line in enumerate(asm_lines):                # add newline character after each asm instruction
        asm_lines[i] = line + "\n"

    asm_file = open(asm_filename, "w")                  # open and write to .asm file
    asm_file.writelines(asm_lines)                      # after done translating all .vm files

def translate_file(filename):                           # called for each .vm file that needs to be translated
    global asm_lines                                    # use global asm_lines to consolidate asm lines from multiple .vm files

    vm_file = open(filename, "r")
    file_prefix = filename.split("/")[-1].split(".")[0] # "MemoryAccess/StaticTest/StaticTest.vm" => "StaticTest"

    for line in vm_file:
        parsed_fields = parser.parse(line)              # returns array - ["push", "local", "3"]

        if parsed_fields is None:                       # returns None if comment line or empty line
            continue
        
        asm_lines += ["// " + line.split("/")[0].strip()]     # adds vm comment (e.g. // push local 3) before asm instructions

        asm_codes = codeWriter.translate(parsed_fields, file_prefix) # pass current file prefix (for static vars, functions)

        asm_lines += asm_codes                          # asm_codes is an array of codes to be printed to .asm file

def add_bootstrap():                    # starting code in .asm file
    global asm_lines

    asm_lines += [
        "@261", "D=A", "@SP", "M=D",    # set SP = 261
        "@Sys.init", "0;JMP"            # jump to Sys.init function
    ]


main()


