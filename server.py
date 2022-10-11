import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pioneerRepo import all, retrieve, create, update, delete
# from views import delete_animal, delete_location, delete_employee


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
# Default response
method_mapper = {
    "animals": {
        "single": retrieve,
        "all": all,
        "update": update,
        "delete": delete
    },
    "locations": {
        "single": retrieve,
        "all": all,
        "update": update,
        "delete": delete
    },
    "employees": {
        "single": retrieve,
        "all": all,
        "update": update,
        "delete": delete
    },
    "customers": {
        "single": retrieve,
        "all": all,
        "update": update,
        "delete": delete
    }
}

class HandleRequests(BaseHTTPRequestHandler):
    
    def get_all_or_single(self, resource, id):
        if id is not None:
            response = method_mapper[resource]["single"](resource, id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = { "message": f'Sorry, there are no {resource} with an id of {id}. '}
        else:
            self._set_headers(200)
            response = method_mapper[resource]["all"](resource)

        return response
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server
        """
        # Set the response code to 'Ok'
        response = {}  

        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        #line 88 along with 35-48 and method_mapper replaces 90-122
        response = self.get_all_or_single(resource, id)

        self.wfile.write(json.dumps(response).encode())


    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.

    # def post_create(self, post_body, resource)

    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_item = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            if "name" in post_body and "species" in post_body and "locationId" in post_body and "customerId" in post_body and "status" in post_body:
                self._set_headers(201)
                new_item = create(post_body, resource)
            else:
                self._set_headers(400)
                new_item = { 
                    "message": f'{"name is required" if "name" not in post_body else ""}' f'{"species is required" if "species" not in post_body else ""}'\
                    f'{"locationId is required" if "locationId" not in post_body else ""}' f'{"customerId is required" if "customerId" not in post_body else ""}'\
                    f'{"status is required" if "status" not in post_body else ""}'
                }
        elif resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_item = create(post_body, resource)
            else:
                self._set_headers(400)
                new_item = { 
                    "message": f'{"name is required" if "name" not in post_body else ""} {"address is required" if "address" not in post_body else ""}'
                }
        elif resource == "employees":
            if "name" in post_body:
                self._set_headers(201)
                new_item = create(post_body, resource)
            else:
                self._set_headers(400)
                new_item = { 
                    "message": f'{"name is required" if "name" not in post_body else ""}'
                }
        elif resource == "customers":
            if "name" in post_body:
                self._set_headers(201)
                new_item = create(post_body, resource)
            else:
                self._set_headers(400)
                new_item = { 
                    "message": f'{"name is required" if "name" not in post_body else ""}'
                }

        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_item).encode())

    def put_update(self, resource, id, post_body):
        return method_mapper[resource]["update"](resource, id, post_body)

    # A method that handles any PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        self.put_update(resource, id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()


    def delete_module(self, id, resource):
        if resource == "customers":
            self._set_headers(405)
            response = {
                "message": f'{"Deletion of customer data is not allowed"}'
            }
        else:
            self._set_headers(204)
            response = method_mapper[resource]["delete"](id, resource)
        return response

    def do_DELETE(self):
    # Parse the URL
        (resource, id) = self.parse_url(self.path)

        response = self.delete_module(id, resource)

    # Encode the new customer and send in response
        self.wfile.write(json.dumps(response).encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
