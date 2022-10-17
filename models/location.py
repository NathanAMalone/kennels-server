class Location():

    # Class initializer. It has 2 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, name, animals, address):
        self.id = id
        self.name = name
        self.animals = animals
        self.address = address
        