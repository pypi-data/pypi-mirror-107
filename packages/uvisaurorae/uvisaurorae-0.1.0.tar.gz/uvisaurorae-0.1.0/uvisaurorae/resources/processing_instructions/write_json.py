import json
from pathlib import Path

all_cmds = []

with open(Path.cwd() / "uvisaurorae/resources/processing_instructions_raw.txt", "r") as f:
    current_cmd = dict(
        uvis_file_names=[],
    )
    line = f.readline()
    while line:
        full_file, cmd = line.strip("\n").split(",")
        current_cmd["release_number"] = int(full_file[10:12])
        current_cmd["uvis_file_names"].append(full_file.split("/")[-1])
        current_cmd["projection_mode"] = "split" if "SPLIT" in cmd else "combine"
        if current_cmd["projection_mode"] == "combine":
            current_cmd["clean"] = False if "NOCLEAN" in cmd else True
        if "SENS" in cmd:
            current_cmd["sensitivity"] = float(cmd.split("SENS")[-1])
        if not "COMBINE_START" in cmd and not "CONT" in cmd:
            all_cmds.append(current_cmd)
            current_cmd = dict(
                uvis_file_names=[],
            )
        line = f.readline()


with open(Path.cwd() / "uvisaurorae/resources/full_command_list.json", "w") as f:
    f.write(json.dumps(all_cmds, indent=4))
