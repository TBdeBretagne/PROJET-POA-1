def enfiler(file, objet):
    file.append(objet)

def defiler(file):
    aux = file[0]
    file.pop(0)
    return aux
