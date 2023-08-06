from os import path, listdir


def search(tpath):
    if path.isdir(tpath):
        try:
            for dirs in listdir(tpath):
                if path.isdir(path.join(tpath, dirs)):
                    search(path.join(tpath, dirs))
                else:
                    print("\n", path.basename(path.join(tpath, dirs)))
        except PermissionError:
            print("\n""Отказано в доступе - " + tpath)
    else:
        if path.isfile(tpath):
            print(path.basename(tpath))
        else:
            print("Неверно указан путь!")
