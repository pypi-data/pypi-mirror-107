def modify(file, old=None, new=None, combination=None, whole=None, delete=False):
    if delete is True:
        import os
        os.remove(file)
    else:
        if whole != None:
            with open(file, "w") as f:
                if type(whole) == list:
                    for i in whole:
                        f.write(i + "\n")
                elif type(whole) == str:
                    f.write(whole)
        else:
            fileContent = ""
            if combination != None:
                old = list(combination.keys())
                new = list(combination.values())
            elif old is None or new is None:
                raise Exception("没有old或new")
            with open(file, "r") as f:
                c = 0
                for line in f:
                    if type(new) == list:
                        for i in old:
                            if i in line:
                                line = line.replace(i, new[c])
                                old.pop(c)
                                new.pop(c)
                            c += 1
                    elif type(old) == str:
                        if old in line:
                            line = line.replace(old, new)
                    c = 0
                    fileContent += line
            with open(file, "w") as f:
                f.write(fileContent)
