#!/usr/bin/env python3
"""
BPAY Platform Server
Lightweight Python server providing local testing, static file delivery,
and REST API endpoints for live needs clearing, dual-sided authentication,
automatic withdrawal fee coverage, and global institution verification.
(No crypto rails - 100% Apple Pay, Google Pay, Cards, and Direct Bank Wire).
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys

PORT = 8080

NEEDS = [
    {
        "id": "need-1",
        "category": "medical",
        "categoryLabel": "Medical & Surgery",
        "title": "Elena's Pediatric Heart Surgery Arrears",
        "recipient": "Elena R. (Mother of Mia, 4)",
        "location": "Philadelphia, USA",
        "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=120&q=80",
        "amount": 2840.0,
        "dueDays": "Due in 3 days",
        "urgency": "CRITICAL",
        "payee": "Children's Hospital of Philadelphia",
        "invoiceNo": "CHOP-2026-8819",
        "riskScore": "100% Clean",
        "hasVideo": True,
        "videoDuration": "0:42",
        "story": "Mia had an emergency valve repair. Insurance capped out $2,840 short. As an assistant teacher, this balance threatens wage garnishment.",
        "cleared": False
    },
    {
        "id": "need-2",
        "category": "tuition",
        "categoryLabel": "University & School",
        "title": "Final Semester BSN Nursing Tuition",
        "recipient": "Marcus Vance (Senior Student)",
        "location": "Columbus, USA",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=120&q=80",
        "amount": 3450.0,
        "dueDays": "Due in 5 days",
        "urgency": "HIGH",
        "payee": "Ohio State University Bursar",
        "invoiceNo": "OSU-BURSAR-9012",
        "riskScore": "100% Clean",
        "hasVideo": True,
        "videoDuration": "0:35",
        "story": "First generation college student with a 3.9 GPA. I have an ICU hospital contract ready upon graduation, but OSU holds degrees until arrears are cleared.",
        "cleared": False
    },
    {
        "id": "need-3",
        "category": "rent",
        "categoryLabel": "Rent & Tenancy Deeds",
        "title": "3 Months Rent Arrears After Layoff",
        "recipient": "David & Sarah Jenkins",
        "location": "Manchester, UK",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80",
        "amount": 1950.0,
        "dueDays": "Due Tomorrow",
        "urgency": "CRITICAL",
        "payee": "Oakridge Residential Property LLC (Verified Lease)",
        "invoiceNo": "LEASE-UK-4412",
        "riskScore": "99.9% Clean",
        "hasVideo": True,
        "videoDuration": "0:50",
        "story": "David's factory closed unexpectedly. He starts his municipal job next week, but our tenancy contract stipulates immediate eviction notice.",
        "cleared": False
    },
    {
        "id": "need-4",
        "category": "groceries",
        "categoryLabel": "Groceries & Food Security",
        "title": "Monthly Family Groceries & Formula",
        "recipient": "Fatima & 3 Children",
        "location": "Sydney, Australia",
        "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=120&q=80",
        "amount": 380.0,
        "dueDays": "Due Today",
        "urgency": "URGENT",
        "payee": "Direct Supermarket Voucher (Woolworths)",
        "invoiceNo": "GROC-SYD-009",
        "riskScore": "100% Clean",
        "hasVideo": False,
        "story": "Single mother working night cleaning shifts. Need urgent grocery voucher for baby formula, fresh vegetables, and pantry staples for the children.",
        "cleared": False
    }
]

GLOBAL_STATS = {
    "totalCleared": 5412890.0,
    "burdensLifted": 1489,
    "recipientFees": "0.00%",
    "milesMultiplier": "3x - 5x"
}

class BPayHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
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
        
        if parsed.path == '/api/needs':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(NEEDS).encode('utf-8'))
            return
            
        elif parsed.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(GLOBAL_STATS).encode('utf-8'))
            return

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

        # POST /api/create-payment-intent: Stripe PaymentIntent creation
        if parsed.path == '/api/create-payment-intent':
            need_id = body.get('needId', 'need-demo')
            recipient_name = body.get('recipientName', 'Verified Recipient')
            payee = body.get('payee', 'Verified Direct Institution')
            base_amount = float(body.get('amount', 100.0))
            tip_pct = float(body.get('tipPercent', 5.0))

            fee = round((base_amount * 0.039) + 0.30, 2)
            tip = round((base_amount * tip_pct) / 100.0, 2)
            total = round(base_amount + fee + tip, 2)

            res = {
                "clientSecret": f"pi_test_bpay_{os.urandom(8).hex()}_secret_{os.urandom(12).hex()}",
                "paymentIntentId": f"pi_test_{os.urandom(10).hex()}",
                "baseAmount": base_amount,
                "withdrawalFee": fee,
                "tipAmount": tip,
                "totalAmount": total
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        # POST /api/create-guild-subscription: Stripe Checkout Session for $299/mo Guild
        elif parsed.path == '/api/create-guild-subscription':
            res = {
                "url": f"https://checkout.stripe.com/c/pay/cs_test_{os.urandom(12).hex()}",
                "sessionId": f"cs_test_{os.urandom(12).hex()}"
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        # POST /api/create-connect-account: Stripe Connect Express Onboarding
        elif parsed.path == '/api/create-connect-account':
            res = {
                "accountId": f"acct_{os.urandom(8).hex()}",
                "url": f"https://connect.stripe.com/setup/c/acct_{os.urandom(8).hex()}"
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        # POST /api/clear: Clear a verified need
        elif parsed.path == '/api/clear':
            need_id = body.get('id')
            rail = body.get('rail', 'Apple Pay')
            tip_pct = body.get('tipPercent', 5)
            
            target = next((n for n in NEEDS if n['id'] == need_id), None)
            if target:
                target['cleared'] = True
                
                # Automatic withdrawal fee calculation added to patron total
                fee = round((target['amount'] * 0.039) + 0.30, 2)
                tip = round((target['amount'] * tip_pct) / 100.0, 2)
                total_paid = round(target['amount'] + fee + tip, 2)
                miles_earned = round(total_paid * 1.25)

                GLOBAL_STATS['totalCleared'] += target['amount']
                GLOBAL_STATS['burdensLifted'] += 1
                
                res = {
                    "success": True,
                    "need": target,
                    "recipientReceivedExact": target['amount'],
                    "recipientFeesDeducted": 0.0,
                    "feeCoveredByPatron": fee,
                    "patronTip": tip,
                    "totalPaidByPatron": total_paid,
                    "airlineMilesCredited": miles_earned,
                    "paymentRail": rail,
                    "receiptNumber": f"BPAY-CLEAR-{os.urandom(4).hex().upper()}"
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(res).encode('utf-8'))
                return
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Need not found"}).encode('utf-8'))
                return

        # POST /api/needs/submit: Recipient submits new need
        elif parsed.path == '/api/needs/submit':
            new_id = f"need-{len(NEEDS) + 1}"
            new_need = {
                "id": new_id,
                "category": body.get("category", "groceries"),
                "categoryLabel": body.get("categoryLabel", "Essential Relief"),
                "title": body.get("title", "Verified Essential Need"),
                "recipient": body.get("name", "Verified Individual"),
                "location": body.get("location", "Global Resident"),
                "avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=120&q=80",
                "amount": float(body.get("amount", 400)),
                "dueDays": "Due in 3 days",
                "urgency": "HIGH",
                "payee": body.get("payee", "Direct Payee"),
                "invoiceNo": f"VERIF-{os.urandom(2).hex().upper()}",
                "riskScore": "100% Audited",
                "hasVideo": bool(body.get("hasVideo", True)),
                "videoDuration": "0:30",
                "story": body.get("story", "Urgent essential support request."),
                "cleared": False
            }
            NEEDS.insert(0, new_need)
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "need": new_need}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), BPayHandler) as httpd:
        print("="*65)
        print(f"  ⚡ BPAY Sovereign Benefactor Platform (Light Luxury Mode)")
        print(f"  👉 Local URL: http://localhost:{PORT}")
        print(f"  👉 Network:   http://127.0.0.1:{PORT}")
        print("="*65)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()

if __name__ == '__main__':
    run_server()
