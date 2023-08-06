in_file = "D:/GIT/uvisaurorae/uvisaurorae/resources/processing_instructions/full_set_cleaned.txt"
out_file = "D:/GIT/uvisaurorae/uvisaurorae/resources/processing_instructions/full_set_cleaned_2.txt"
with open(out_file, "w") as outfile:
    with open(in_file, "r") as infile:
        line = infile.readline()
        while line:
            if "COUVIS_0060" in line:
                filename, cmd = line.split(",")
                filename = filename.split("\\")[-1]
                f = filename[:17]
                writepath = f"/COUVIS_0060/DATA/D{f[3:11]}/{f}"
                outfile.write(f"{writepath},{cmd}")
            else:
                outfile.write(line)
            line = infile.readline()
