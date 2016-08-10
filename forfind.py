import csv
from forlinelist import karts


def findrastres(name, coord_x, coord_y, file="maps.csv"):
    input_file = open(file, 'r')
    rf = csv.reader(input_file, dialect="excel")
    for line in rf:
        s = line[0].strip().split(";")
        if s[0] == name:
            if float(s[2]) <= coord_x <= float(s[3]) and float(s[4]) <= coord_y <= float(s[5]):
                return s[1]


if __name__ == "__main__":
    check = True
    district = input("Введите район - ")
    while check:
        if district not in karts:
            print("Введенного района нет в базе.\n")
            district = input("Введите район - ")
        else:
            break
    x = float(input("Введите координату X - "))
    y = float(input("Введите координату Y - "))
    print(findrastres(district, x, y))

