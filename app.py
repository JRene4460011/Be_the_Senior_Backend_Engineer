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
        driver_id = int(self.path.split("/")[-1])

        # Find the driver
        for driver in drivers:

            if driver["driverId"] == driver_id:

                # Read request body
                content_length = int(self.headers["Content-Length"])
                body = self.rfile.read(content_length)

                data = json.loads(body)

                # Update driver
                driver["driverName"] = data["driverName"]
                driver["driverAvailability"] = data["driverAvailability"]
                driver["driverVehiclePlateNumber"] = data["driverVehiclePlateNumber"]

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
        driver_id = int(self.path.split("/")[-1])

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