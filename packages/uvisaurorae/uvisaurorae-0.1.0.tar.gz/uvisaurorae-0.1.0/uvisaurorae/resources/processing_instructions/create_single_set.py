from pathlib import Path

file_path = "D:/GIT/uvisaurorae/uvisaurorae/resources/processing_instructions"
all_files = list(Path(file_path).glob("COUVIS*"))

out_file = (
    "D:/GIT/uvisaurorae/uvisaurorae/resources/processing_instructions/full_set.txt"
)
with open(out_file, "w") as outfile:
    for in_file in all_files:
        with open(in_file, "r") as infile:
            line = infile.readline()
            while line:
                if not "SKIP" in line:
                    outfile.write(line)
                line = infile.readline()
