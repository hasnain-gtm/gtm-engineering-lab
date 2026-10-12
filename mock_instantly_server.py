from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MockMultiChannelHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        auth_header = self.headers.get("Authorization", "")
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode("utf-8")) if body else {}

        if "Bearer FAKE_MULTI_CHANNEL_KEY_999" not in auth_header:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode("utf-8"))
            return

        path = self.path
        leads = payload.get("leads", [])
        campaign_id = payload.get("campaign_id", "UNKNOWN")

        print("\n" + "="*60)
        if "/v1/email/campaign" in path:
            print(f" [EMAIL SEQUENCER RECEIVED BATCH]")
            print(f" Campaign: {campaign_id} | Ingested: {len(leads)} leads")
            if leads:
                print(f" Sample Email Send: {leads[0]['email']}")
        elif "/v1/linkedin/campaign" in path:
            print(f" [LINKEDIN AUTOMATION ENDPOINT (HEYREACH) RECEIVED BATCH]")
            print(f" Campaign: {campaign_id} | Ingested: {len(leads)} profiles")
            if leads:
                print(f" Sample Connection Note: {leads[0]['connection_note']}")
        print("="*60)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "success",
            "message": f"Successfully queued {len(leads)} leads into {campaign_id}"
        }).encode("utf-8"))

def run_server():
    httpd = HTTPServer(("127.0.0.1", 5000), MockMultiChannelHandler)
    print("Multi-Channel Mock Endpoint running at http://127.0.0.1:5000 ...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()