import argparse, os

def folders_and_files_exist(path):

    files = [
        # [relative path, error message]
        ["", f"Folder {path} does not exist."],
        ["/base", f"Folder {path + '/base'} does not exist"],
        ["/base/LogisimClockComponent.v", f"File \"LogisimClockComponent.v\" does not exist within {path + '/base'}. Does the design use a clock?"],
        ["/base/logisimTickGenerator.v", f"File \"logisimTickGenerator.v\" does not exist within {path + '/base'}. Does the design use a clock?"],
        ["/circuit/main.v", f"File \"main.v\" does not exist within {path + '/circuit'}. Does the design exist?"],
        ["/toplevel/logisimTopLevelShell.v", f"File \"logisimTopLevelShell.v\" does not exist within {path + '/toplevel'}. Does the design exist?"]
    ]

    for rel_path, error in files:
        if not os.path.exists(path + rel_path):
            raise Exception(error)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logisim_folder", help="Path to the logisim folder containing the design")
    args = parser.parse_args()

    path = args.logisim_folder + "main/verilog"
    folders_and_files_exist(path)

    custom_clock_signal_name = "extracted_clock_o"
    shell_path = path + "/toplevel/logisimTopLevelShell.v"

    with open(shell_path) as f:
        shell_file = f.readlines()

    if f"{custom_clock_signal_name}" in shell_file[9]:
        print("signal already exists in file, will not add another")
        return -1
    
    shell_file.insert(9, f"\t\t\t     {custom_clock_signal_name},\n")

    # im sure there's a smarter way of doing this, but i'll just loop through the contents
    last_index = 0
    for i in range(0, len(shell_file)):
        if "The outputs are defined here" in shell_file[i]:
            shell_file.insert(i + 2, f"   output {custom_clock_signal_name};\n")
            last_index = i + 2
            break

    for i in range(last_index, len(shell_file)):
        if "All signal adaptations are performed here" in shell_file[i]:
            shell_file.insert(i + 2, f"   assign {custom_clock_signal_name} = s_logisimClockTree0[0];\n")
            break

    with open(shell_path, "w") as f:
        for line in shell_file:
            f.write(line)

if __name__ == "__main__":
    main()