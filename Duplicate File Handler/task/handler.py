# write your code here
import os
import sys

args = sys.argv
file_sizes = {}

if len(sys.argv) < 2:
    print("Directory is not specified")
    exit(0)
print("Enter file format:")
file_format = input()
for root, dirs, files in os.walk(sys.argv[1], topdown=True):
    for name in files:
        file_name = os.path.join(root, name)
        size = os.path.getsize(file_name)
        if size in file_sizes and file_name.endswith(file_format):
            names = file_sizes.get(size)
            names.append(file_name)
            file_sizes.update({size: names})
        elif file_name.endswith(file_format):
            file_sizes.update({size: [file_name]})
while True:
    print("Size sorting options:")
    print("1. Descending")
    print("2. Ascending")
    print()
    print("Enter a sorting option:")
    choice = input()
    if choice != "1" and choice != "2":
        print("Wrong option")
        continue
    if choice == "1":
        order = True
    if choice == "2":
        order = False
    for key, value in sorted(file_sizes.items(), reverse=order):
        print("{} bytes".format(key))
        for n in value:
            print(n)
    break
