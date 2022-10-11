DATABASE = {
    "animals": [
        {
            "id": 1,
            "name": "Snickers",
            "species": "Dog",
            "locationId": 1,
            "customerId": 4,
            "status": "Admitted"
        },
        {
            "id": 2,
            "name": "Roman",
            "species": "Dog",
            "locationId": 1,
            "customerId": 2,
            "status": "Admitted"
        },
        {
            "id": 3,
            "name": "Blue",
            "species": "Cat",
            "locationId": 2,
            "customerId": 1,
            "status": "Admitted"
        }
    ],
    "customers": [
        {
            "id": 1,
            "name": "Ryan Tanay"
        }
    ],
    "employees": [
        {
            "id": 1,
            "name": "Jenna Solis"
        }
    ],
    "locations": [
        {
            "id": 1,
            "name": "Nashville North",
            "address": "8422 Johnson Pike"
        },
        {
            "id": 2,
            "name": "Nashville South",
            "address": "209 Emory Drive"
        }
    ]
}

def all(resource):
    """For GET requests to collection"""
    return DATABASE[resource]

def retrieve(resource, id):
    requested_item = None

    for dictionary in DATABASE[resource]:
        if dictionary["id"] == id:
            requested_item = dictionary
            
            if "locationId" in requested_item:
                for location in DATABASE["locations"]:
                    if location["id"] == requested_item["locationId"]:
                        requested_item["location"] = location
                requested_item.pop("locationId")
            else:
                ""
            
            if "customerId" in requested_item:
                for customer in DATABASE["customers"]:
                    if customer["id"] == requested_item["customerId"]:
                        requested_item["customer"] = customer
                requested_item.pop("customerId")
            else:
                ""
    return requested_item

def create(post_body, resource):
    max_id = DATABASE[resource][-1]["id"]
    new_id = max_id + 1
    post_body["id"] = new_id
    DATABASE[resource].append(post_body)
    return post_body

def  update(resource, id, post_body):
    for index, item in enumerate(DATABASE[resource]):
        if item["id"] == id:
            DATABASE[resource][index] = post_body
            break

def delete(id, resource):
    item_index = -1
    for index, item in enumerate(DATABASE[resource]):
        if item["id"] == id:
            item_index = index
    if item_index >= 0:
        DATABASE[resource].pop(item_index)