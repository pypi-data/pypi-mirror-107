import sys
import os
import os.path
# Messy code, oh well you'll never notice 😏

def main(path):
    i = 0
    local = path

    os.chdir(local)
    content = os.listdir()

    items = []

    for things in content:
        items.append(things)

    d = []
    f = []

    for item in items:
        if os.path.isdir(items[i]) == True:
            d.append(items[i])

        if os.path.isfile(items[i]) == True:
            f.append(items[i])
        i += 1

    print(d, f)

    if d:
        thing = path + '\\' + d[0]
        main(thing)

if __name__ == '__main__':
    main(sys.argv[1])