class Animal():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, name, breed, status, locationId, customerId):
        self.id = id
        self.name = name
        self.breed = breed
        self.status = status
        self.location_id = locationId
        self.customer_id = customerId
        self.location = None
        self.customer = None