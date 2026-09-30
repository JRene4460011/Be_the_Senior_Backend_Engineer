from http.server import BaseHTTPRequestHandler, HTTPServer
import json


drivers = [
    {
        "driverId": 1,
        "driverName": "Jean Paul",
        "driverAvailability": True,
        "driverVehiclePlateNumber": "RAB123A"
    },
    {
        "driverId": 2,
        "driverName": "Eric",
        "driverAvailability": False,
        "driverVehiclePlateNumber": "RAD456B"
    }
]


class DriverHandler(BaseHTTPRequestHandler):

    # PUT /api/v1/drivers/:driverId
    def do_PUT(self):

        # Get driver ID from URL
        try:
            driver_id = int(self.path.split("/")[-1])
        except ValueError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "Invalid driver ID"}).encode()
            )
            return

        # Find the driver
        for driver in drivers:

            if driver["driverId"] == driver_id:

                # Read request body
                content_length = int(self.headers["Content-Length"])
                body = self.rfile.read(content_length)

                # Parse and validate the body
                try:
                    data = json.loads(body)
                    driver["driverName"] = data["driverName"]
                    driver["driverAvailability"] = data["driverAvailability"]
                    driver["driverVehiclePlateNumber"] = data["driverVehiclePlateNumber"]
                except (json.JSONDecodeError, KeyError):
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(
                        json.dumps({"error": "Missing or invalid fields"}).encode()
                    )
                    return

                # Send response
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(driver).encode())

                return

        # Driver not found
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            json.dumps({
                "error": "Driver not found"
            }).encode()
        )


    # DELETE /api/v1/drivers/:driverId
    def do_DELETE(self):

        # Get driver ID from URL
        try:
            driver_id = int(self.path.split("/")[-1])
        except ValueError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "Invalid driver ID"}).encode()
            )
            return

        # Find the driver
        for driver in drivers:

            if driver["driverId"] == driver_id:

                # Deactivate the driver
                driver["driverAvailability"] = False

                # Send response
                self.send_response(204)
                self.end_headers()

                return

        # Driver not found
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            json.dumps({
                "error": "Driver not found"
            }).encode()
        )


server = HTTPServer(("localhost", 8000), DriverHandler)

print("Server running at http://localhost:8000")

server.serve_forever()