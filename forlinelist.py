import csv
a = []
input_file = open("maps.csv", 'r')
rf = csv.reader(input_file, dialect="excel")
for line in rf:
    s = line[0].split(";")
    if s[0] != "":
        a.append(s[0])
karts = set(a)
karts = list(karts)
karts.sort()

