from importlib import import_module
import json
import sqlite3
from models import Employee, Location, AnimalInEmployee

EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    }
]

# def get_all_employees():
#     return EMPLOYEES

def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.id location_id,
            l.name location_name,
            l.address location_address
        FROM Employee e
        JOIN Location l
            ON l.id = e.location_id
        """)

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Employee class above.
            employee = Employee(row['id'], row['name'], row['address'],
                                row['location_id'])

            location = Location(row['location_id'], row['location_name'], row['address'])

            employee.location = location.__dict__

            employees.append(employee.__dict__)

    return employees

# def get_single_employee(id):
#     requested_employee = None
#     for employee in EMPLOYEES:
#         if employee["id"] == id:
#             requested_employee = employee
#     return requested_employee

def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
       SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            an.id animal_id,
            an.name animal_name,
            d.name duty_name
        FROM Employee e
        JOIN Assignments a
            ON a.employee_id = e.id
        JOIN Duties d
            ON d.id = a.duties_id
        JOIN Animal an
            ON an.id = a.animal_id
        WHERE e.id = ?
        GROUP BY an.name
        """, ( id, ))

        # Load the single result into memory
        dataset = db_cursor.fetchall()

        assigned_animals = []
        employee = None

        for row in dataset:
            
            animal = AnimalInEmployee(row['animal_id'], row['animal_name'])

            assigned_animals.append(animal.__dict__)

        for row in dataset:

            if employee is None:
        # Create an employee instance from the current row
                employee = Employee(row['id'], row['name'], row['address'],
                                row['location_id'])


                employee.animal = assigned_animals
                

        return employee.__dict__

# def create_employee(employee):
#     # Get the id value of the last employee in the list
#     max_id = EMPLOYEES[-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an `id` property to the employee dictionary
#     employee["id"] = new_id

#     # Add the employee dictionary to the list
#     EMPLOYEES.append(employee)

#     # Return the dictionary with `id` property added
#     return employee

def create_employee(new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            ( name, address, location_id )
        VALUES
            ( ?, ?, ?);
        """, (new_employee['name'], new_employee['address'], 
                new_employee['location_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_employee['id'] = id


    return new_employee

def delete_employee(id):
    # Initial -1 value for employee index, in case one isn't found
    employee_index = -1

    # Iterate the EMPLOYEES list, but use enumerate() so that you
    # can access the index value of each item
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Store the current index.
            employee_index = index

    # If the employee was found, use pop(int) to remove it from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)

# def update_employee(id, new_employee):
#     # Iterate the EMPLOYEES list, but use enumerate() so that
#     # you can access the index value of each item.
#     for index, employee in enumerate(EMPLOYEES):
#         if employee["id"] == id:
#             # Found the employee. Update the value.
#             EMPLOYEES[index] = new_employee
#             break

def update_employee(id, new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Employee
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_employee['name'], new_employee['breed'],
              new_employee['status'], new_employee['locationId'],
              new_employee['customerId'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def get_employees_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            e.id,
            e.name,
            e.address,
            e.location_id
        from Employee e
        WHERE e.location_id = ?
        """, ( location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
            employees.append(employee.__dict__)

    return employees
