lists = list()
with open("filepaths.txt", "rt") as f:
    for i in f:
        lists.append(i.strip())

with open("filepaths-1.txt", "at") as f:
    for i in range(0, 3250):
        f.write(lists[i] + "\n")
with open("filepaths-2.txt", "at") as f:
    for i in range(3250, 6500):
        f.write(lists[i] + "\n")
with open("filepaths-3.txt", "at") as f:
    for i in range(6500, 9750):
        f.write(lists[i] + "\n")
with open("filepaths-4.txt", "at") as f:
    for i in range(9750, 13000):
        f.write(lists[i] + "\n")
with open("filepaths-5.txt", "at") as f:
    for i in range(13000, 16250):
        f.write(lists[i] + "\n")
with open("filepaths-6.txt", "at") as f:
    for i in range(16250, 19500):
        f.write(lists[i] + "\n")
with open("filepaths-7.txt", "at") as f:
    for i in range(19500, 22750):
        f.write(lists[i] + "\n")
with open("filepaths-8.txt", "at") as f:
    for i in range(22750, len(lists)):
        f.write(lists[i] + "\n")
