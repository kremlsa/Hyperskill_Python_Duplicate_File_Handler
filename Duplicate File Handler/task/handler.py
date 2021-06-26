# write your code here
import os
import sys
import hashlib


def sort_files():
    while True:
        global file_sizes
        print("Size sorting options:")
        print("1. Descending")
        print("2. Ascending")
        print()
        print("Enter a sorting option:")
        choice = input()
        print()
        if choice != "1" and choice != "2":
            print("Wrong option")
            continue
        if choice == "1":
            order = True
        if choice == "2":
            order = False
        file_sizes = sorted(file_sizes.items(), reverse=order)
        for key, value in file_sizes:
            print("{} bytes".format(key))
            for n in value:
                print(n)
            print()
        break


def hash_files():
    global file_hashes, duplicates
    counter = 1
    while True:
        print("Check for duplicates?")
        answer_ = input()
        print()
        if answer_ == "no":
            break
        if answer_ != "yes":
            continue
        for key, value in file_sizes:
            for n in value:
                with open(n, "rb") as file_:
                    hash_ = hashlib.md5(file_.read()).hexdigest()
                if key in file_hashes:
                    if hash_ in file_hashes.get(key).keys():
                        temp_ = file_hashes.get(key).get(hash_)
                        temp_.append(n)
                        dup_ = file_hashes.get(key)
                        dup_.update({hash_: temp_})
                        file_hashes.update({key: dup_})
                    else:
                        dup_ = file_hashes.get(key)
                        dup_.update({hash_: [n]})
                        file_hashes.update({key: dup_})
                else:
                    file_hashes.update({key: {hash_: [n]}})

        for key, value in file_hashes.items():
            is_skip = True
            for hh, ff in value.items():
                if len(ff) > 1:
                    is_skip = False
                    break
            if is_skip:
                continue
            print("{} bytes".format(key))
            for h, f in value.items():

                if len(f) < 2:
                    continue

                print("Hash: {}".format(h))
                for f_ in f:
                    print("{}. {}".format(counter, f_))
                    duplicates.append([counter, f_, key, h])
                    counter += 1
                print()
        break


def delete_files():
    while True:
        print("Delete files?")
        answer_ = input()
        print()
        if answer_ == "no":
            break
        if answer_ != "yes":
            continue
        while True:
            print("Enter file numbers to delete:")
            answer_ = input().split(" ")
            if not set(answer_).issubset(set([str(x[0]) for x in duplicates])):
                print("Wrong format")
                print()
                continue
            size_ = 0
            for x in answer_:
                for y in duplicates:
                    if x == str(y[0]):
                        os.remove(y[1])
                        size_ += y[2]
                        break
            print("Total freed up space: {} bytes".format(size_))

            break
        break


duplicates = []
args = sys.argv
file_sizes = {}
file_hashes = {}

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

sort_files()
hash_files()
delete_files()
