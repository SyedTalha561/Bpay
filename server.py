#!/usr/bin/env python3
"""
BPAY Platform Server
Lightweight Python server providing local testing, static file delivery,
and simulated REST API endpoints for live expense clearing, verification, and webhooks.
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys

PORT = 8080

# In-memory database of initial verified expenses
EXPENSES = [
    {
        "id": "exp-1",
        "category": "medical",
        "categoryLabel": "Medical & Surgery",
        "title": "Elena's Pediatric Heart Surgery Arrears",
        "recipient": "Elena R. (Mother of Mia, 4)",
        "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=120&q=80",
        "amount": 2840.0,
        "dueDays": "Due in 3 days",
        "urgency": "CRITICAL",
        "billerName": "Children's Hospital of Philadelphia",
        "invoiceNo": "CHOP-2026-8819",
        "riskScore": "99.9% Clean",
        "story": "Mia had an emergency valve replacement. The insurance capped our coverage $2,840 short of the hospital bill. As a single mother working as a preschool assistant, this balance threatens wage garnishment.",
        "verified": True,
        "directPayout": True,
        "cleared": False
    },
    {
        "id": "exp-2",
        "category": "tuition",
        "categoryLabel": "Education & Tuition",
        "title": "Final Semester BSN Nursing Tuition",
        "recipient": "Marcus Vance (Senior Student)",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=120&q=80",
        "amount": 3450.0,
        "dueDays": "Due in 5 days",
        "urgency": "HIGH",
        "billerName": "Ohio State University Bursar",
        "invoiceNo": "OSU-BURSAR-9012",
        "riskScore": "99.8% Clean",
        "story": "First generation college student. I have a 3.9 GPA and already have an ICU nursing job offer lined up, but OSU holds degrees until final account arrears are cleared.",
        "verified": True,
        "directPayout": True,
        "cleared": False
    },
    {
        "id": "exp-3",
        "category": "housing",
        "categoryLabel": "Rent & Eviction Shield",
        "title": "3 Months Rent Arrears After Layoff",
        "recipient": "Sarah & David Jenkins",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80",
        "amount": 1950.0,
        "dueDays": "Due Tomorrow",
        "urgency": "CRITICAL",
        "billerName": "Oakridge Residential Property LLC",
        "invoiceNo": "OAK-LEASE-4412",
        "riskScore": "99.7% Clean",
        "story": "David lost his machining job when the plant closed. He starts his new municipal job in two weeks, but our landlord filed an immediate 7-day cure or quit notice.",
        "verified": True,
        "directPayout": True,
        "cleared": False
    }
]

GLOBAL_STATS = {
    "totalCleared": 4842910.0,
    "burdensLifted": 1248,
    "fraudScore": "99.98%"
}

class BPayHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and disable aggressive caching for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # API Routes
        if parsed.path == '/api/expenses':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(EXPENSES).encode('utf-8'))
            return
            
        elif parsed.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(GLOBAL_STATS).encode('utf-8'))
            return

        # Fallback to serving static files (index.html, etc.)
        if parsed.path == '/' or parsed.path == '':
            self.path = '/index.html'
            
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            body = json.loads(post_data.decode('utf-8')) if post_data else {}
        except Exception:
            body = {}

        # POST /api/clear: Clear an expense
        if parsed.path == '/api/clear':
            expense_id = body.get('id')
            payment_rail = body.get('rail', 'Card')
            tip_percent = body.get('tipPercent', 10)
            
            target = next((e for e in EXPENSES if e['id'] == expense_id), None)
            if target:
                target['cleared'] = True
                tip_amount = (target['amount'] * tip_percent) / 100.0
                total_cleared = target['amount'] + tip_amount
                
                GLOBAL_STATS['totalCleared'] += target['amount']
                GLOBAL_STATS['burdensLifted'] += 1
                
                response_data = {
                    "success": True,
                    "message": f"Successfully cleared expense {target['title']} via {payment_rail}",
                    "expense": target,
                    "tipAmount": tip_amount,
                    "totalPaid": total_cleared,
                    "receiptId": f"BPAY-TXN-{os.urandom(4).hex().upper()}"
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                return
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Expense not found"}).encode('utf-8'))
                return

        # POST /api/submit: Recipient submits new expense
        elif parsed.path == '/api/submit':
            new_id = f"exp-{len(EXPENSES) + 1}"
            new_expense = {
                "id": new_id,
                "category": body.get("category", "emergency"),
                "categoryLabel": body.get("categoryLabel", "Urgent Relief"),
                "title": body.get("title", "Verified Relief Request"),
                "recipient": body.get("name", "Verified Individual"),
                "avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=120&q=80",
                "amount": float(body.get("amount", 500)),
                "dueDays": "Due Soon",
                "urgency": "HIGH",
                "billerName": body.get("billerName", "Direct Verified Payee"),
                "invoiceNo": body.get("invoiceNo", "INV-NEW-001"),
                "riskScore": "99.9% Clean",
                "story": body.get("story", "Urgent essential expense requiring immediate community support."),
                "verified": True,
                "directPayout": True,
                "cleared": False
            }
            EXPENSES.insert(0, new_expense)
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "expense": new_expense}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), BPayHandler) as httpd:
        print("="*65)
        print(f"  ⚡ BPAY Sovereign Benefactor Platform is Live & Running!")
        print(f"  👉 Local URL: http://localhost:{PORT}")
        print(f"  👉 Network:   http://127.0.0.1:{PORT}")
        print("="*65)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down BPAY server.")
            httpd.server_close()

if __name__ == '__main__':
    run_server()
