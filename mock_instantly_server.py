from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MockInstantlyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read request headers and payload length
        auth_header = self.headers.get("Authorization", "")
        content_length = int(self.headers.get("Content-Length", 0))
        
        # Parse incoming JSON body
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode("utf-8")) if body else {}

        # Validate mock API authentication header
        if "Bearer FAKE_INSTANTLY_API_KEY_123" not in auth_header:
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unauthorized: Invalid API Key"}).encode("utf-8"))
            return

        # Extract leads and campaign metadata
        leads = payload.get("leads", [])
        campaign_id = payload.get("campaign_id", "UNKNOWN")

        # Print formatted log output in Terminal 1
        print("\n" + "="*60)
        print(" [LOCAL MOCK SEQUENCER ENDPOINT RECEIVED PAYLOAD]")
        print("="*60)
        print(f"Target Campaign ID : {campaign_id}")
        print(f"Total Leads Loaded : {len(leads)}")
        if leads:
            sample = leads[0]
            print(f"Sample Lead 1      : {sample.get('first_name')} {sample.get('last_name')} <{sample.get('email')}>")
            print(f"Clean Company Name : {sample.get('custom_variables', {}).get('clean_company_name')}")
            print(f"Target Persona Job : {sample.get('custom_variables', {}).get('title')}")
        print("="*60 + "\n")

        # Return success HTTP 200 JSON response to client
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response_data = {
            "status": "success",
            "message": f"Successfully ingested {len(leads)} leads into campaign '{campaign_id}'",
            "upload_count": len(leads)
        }
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

def run_mock_server():
    server_address = ("127.0.0.1", 5000)
    httpd = HTTPServer(server_address, MockInstantlyHandler)
    print("\nMock Instantly/Smartlead REST Endpoint running at http://127.0.0.1:5000 ...")
    print("Listening for incoming pipeline payloads. Press Ctrl+C to stop.\n")
    httpd.serve_forever()

if __name__ == "__main__":
    run_mock_server()