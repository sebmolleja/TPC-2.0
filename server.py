import json
import cgi
import os
import mimetypes

import backend
import batch
import sfc_calc

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from pathlib import Path

hostName = "localhost"
serverPort = 5000

connect = ['/index.html', '/bootstrap.css', '/script.js']


class TPC_Server(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path.startswith("/images/"):
            # Handle image requests
            file_path = Path.cwd() / self.path[1:]

            if file_path.exists() and file_path.is_file():
                with file_path.open("rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "image/x-icon")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"404 Not Found")

        elif self.path.startswith("/docs/"):
            # Handle PDF file download requests
            file_path = Path.cwd() / "docs" / "Figure2Params.pdf"

            if file_path.exists() and file_path.is_file():
                with file_path.open("rb") as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition",
                                'attachment; filename="Figure2Params.pdf"')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"404 Not Found")

        elif self.path.startswith("/batch/"):

            file_path = Path.cwd() / "batch" / "default_batch.csv"

            if file_path.exists() and file_path.is_file():
                with file_path.open("rb") as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/csv")
                self.send_header("Content-Disposition",
                                'attachment; filename="default_batch.csv"')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"404 Not Found")

        elif self.path.startswith("/sfc_data/"):

            file_path = Path.cwd() / "sfc_data" / "default_sfc.csv"

            if file_path.exists and file_path.is_file():
                with file_path.open("rb") as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/csv")
                self.send_header("Content-Disposition",
                                'attachment; filename="default_sfc.csv"')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"404 Not Found")

        elif self.path.startswith("/download/"):
            # Extract the filename from the URL
            filename = self.path.split("/")[-1]

            # Check if the file exists in the server
            if os.path.exists(filename):
                # Set the appropriate Content-Type based on the file extension
                content_type, _ = mimetypes.guess_type(filename)
                if content_type is None:
                    content_type = "application/octet-stream"

                # Send the file to the client
                with open(filename, "rb") as f:
                    file_content = f.read()

                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Disposition",
                                f'attachment; filename="{filename}"')
                self.end_headers()
                self.wfile.write(file_content)
            else:
                # If the file does not exist, return a 404 Not Found response
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response_data = json.dumps({"message": "File not found."})
                self.wfile.write(response_data.encode("utf-8"))

        elif self.path.startswith("/download_sfc/"):
            # Extract the filename from the URL
            filename = self.path.split("/")[-1]

            # Check if the file exists in the server
            if os.path.exists(filename):
                # Set the appropriate Content-Type based on the file extension
                content_type, _ = mimetypes.guess_type(filename)
                if content_type is None:
                    content_type = "application/octet-stream"

                # Send the file to the client
                with open(filename, "rb") as f:
                    file_content = f.read()

                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Disposition",
                                f'attachment; filename="{filename}"')
                self.end_headers()
                self.wfile.write(file_content)
            else:
                # If the file does not exist, return a 404 Not Found response
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response_data = json.dumps({"message": "File not found."})
                self.wfile.write(response_data.encode("utf-8"))

        elif self.path in connect:
            # Handle requests for other resources (e.g., CSS, JavaScript, HTML)
            file_path = Path.cwd() / self.path[1:]

            if file_path.exists() and file_path.is_file():
                with file_path.open("r", encoding="utf-8") as file:
                    page = file.read()
                self.send_response(200)
                if file_path.suffix == ".css":
                    self.send_header("Content-type", "text/css")
                elif file_path.suffix == ".js":
                    self.send_header("Content-type", "text/javascript")
                else:
                    self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(page))
                self.end_headers()
                self.wfile.write(bytes(page, "utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"404 Not Found")

        else:
            # Handle other requests (e.g., 404 not found)
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Parse the POST data
        data = parse_qs(post_data.decode('utf-8'))

        if all(key in data for key in ['sn1', 'sn2', 'sn3', 'polymorph']):
            sn1 = data['sn1'][0]
            sn2 = data['sn2'][0]
            sn3 = data['sn3'][0]
            polymorph = data['polymorph'][0]

            polym, tag, chemical_formula, mol_weight_sample, exp_enthalpy, exp_temp, sat_enthalpy_sample, temp_sample_a, temp_sample_b, hfGCM, tfGCM = backend.compute(
                sn1, sn2, sn3, polymorph, "reference")

            polym, tag, chemical_formula, mol_weight_sample, exp_enthalpy, exp_temp, sat_enthalpy_sample_P1L, temp_sample_a_P1L, temp_sample_b_P1L, hfGCM, tfGCM = backend.compute(
                sn1, sn2, sn3, polymorph, "P1L")

            mol_weight_sample = mol_weight_sample.tolist()
            sat_enthalpy_sample = sat_enthalpy_sample.tolist()
            temp_sample_a = temp_sample_a.tolist()
            temp_sample_b = temp_sample_b.tolist()

            refID = polym + " " + tag

            results = {
                'refID': refID,
                'chemical_formula': chemical_formula,
                'mol_weight_sample': mol_weight_sample,
                'exp_enthalpy': exp_enthalpy,
                'exp_temp': exp_temp,
                'sat_enthalpy_sample': sat_enthalpy_sample,
                'temp_sample_a': temp_sample_a,
                'temp_sample_b': temp_sample_b,
                'hfGCM': hfGCM,
                'tfGCM': tfGCM,
                'sat_enthalpy_sample_P1L': sat_enthalpy_sample_P1L,
                'temp_sample_a_P1L': temp_sample_a_P1L,
                'temp_sample_b_P1L': temp_sample_b_P1L
            }

            response_data = json.dumps(results)

            # Send a response back to the client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_data.encode('utf-8'))

        else:
            self.send_response(200)
            self.end_headers()

    def do_POST(self):

        if self.path == "/compute":

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Parse the POST data
            data = parse_qs(post_data.decode('utf-8'))

            if all(key in data for key in ['sn1', 'sn2', 'sn3', 'polymorph']):
                sn1 = data['sn1'][0]
                sn2 = data['sn2'][0]
                sn3 = data['sn3'][0]
                polymorph = data['polymorph'][0]

                polym, tag, chemical_formula, mol_weight_sample, exp_enthalpy, exp_temp, sat_enthalpy_sample, temp_sample_a, temp_sample_b, hfGCM, tfGCM = backend.compute(
                    sn1, sn2, sn3, polymorph, "reference")

                polym, tag, chemical_formula, mol_weight_sample, exp_enthalpy, exp_temp, sat_enthalpy_sample_P1L, temp_sample_a_P1L, temp_sample_b_P1L, hfGCM, tfGCM = backend.compute(
                    sn1, sn2, sn3, polymorph, "P1L")

                mol_weight_sample = mol_weight_sample.tolist()
                sat_enthalpy_sample = sat_enthalpy_sample.tolist()
                temp_sample_a = temp_sample_a.tolist()
                temp_sample_b = temp_sample_b.tolist()

                refID = polym + " " + tag

                results = {
                    'refID': refID,
                    'chemical_formula': chemical_formula,
                    'mol_weight_sample': mol_weight_sample,
                    'exp_enthalpy': exp_enthalpy,
                    'exp_temp': exp_temp,
                    'sat_enthalpy_sample': sat_enthalpy_sample,
                    'temp_sample_a': temp_sample_a,
                    'temp_sample_b': temp_sample_b,
                    'hfGCM': hfGCM,
                    'tfGCM': tfGCM,
                    'sat_enthalpy_sample_P1L': sat_enthalpy_sample_P1L,
                    'temp_sample_a_P1L': temp_sample_a_P1L,
                    'temp_sample_b_P1L': temp_sample_b_P1L
                }

                response_data = json.dumps(results)

                # Send a response back to the client
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response_data.encode('utf-8'))

            else:
                self.send_response(200)
                self.end_headers()

        elif self.path == "/upload_batch":

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            file_item = form["file"]

            if file_item.filename and file_item.file:
                if file_item.filename.endswith(".csv"):
                    # Save the uploaded file with the given filename
                    filename = os.path.basename(file_item.filename)
                    with open(filename, 'wb') as f:
                        f.write(file_item.file.read())

                    # Process the uploaded file and get the result file path
                    result_file = batch.handle_batch_file(filename)
                    os.remove(filename)

                    # Send the result_file to the client for download
                    with open(result_file, 'rb') as f:
                        result_file_content = f.read()

                    # Send the JSON response with the filename
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response_data = json.dumps({
                        "message": "File uploaded. Please wait while we process the data...",
                        "filename": os.path.basename(result_file),
                        "original_filename": os.path.splitext(file_item.filename)[0],
                    })
                    # print(response_data)
                    self.wfile.write(response_data.encode('utf-8'))
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response_data = json.dumps(
                        {"message": "Invalid file format. Only CSV files are allowed."})
                    self.wfile.write(response_data.encode('utf-8'))
            else:
                # No file was uploaded
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = json.dumps(
                    {"message": "No file uploaded."})
                self.wfile.write(response_data.encode('utf-8'))

        elif self.path == "/upload_sfc":

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            file_item = form["file"]

            if file_item.filename and file_item.file:
                if file_item.filename.endswith(".csv"):
                    # Save the uploaded file with the given filename
                    filename = os.path.basename(file_item.filename)
                    with open(filename, 'wb') as f:
                        f.write(file_item.file.read())

                    # Process the uploaded file and get the result file path
                    result_file = sfc_calc.handle_sfc_file(filename)
                    os.remove(filename)

                    # Send the result_file to the client for download
                    with open(result_file, 'rb') as f:
                        result_file_content = f.read()

                    # Send the JSON response with the filename
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response_data = json.dumps({
                        "message": "File uploaded. Please wait while we process the data...",
                        "filename": os.path.basename(result_file),
                        "original_filename": os.path.splitext(file_item.filename)[0],
                    })
                    # print(response_data)
                    self.wfile.write(response_data.encode('utf-8'))
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response_data = json.dumps(
                        {"message": "Invalid file format. Only CSV files are allowed."})
                    self.wfile.write(response_data.encode('utf-8'))
            else:
                # No file was uploaded
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = json.dumps(
                    {"message": "No file uploaded."})
                self.wfile.write(response_data.encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()


server = HTTPServer((hostName, serverPort), TPC_Server)
print("Server now running...")

server.serve_forever()
server.server_close()

print("Server stopped")
