#!/usr/bin/env python3
"""
BPAY Master Blueprint Email Dispatcher
Sends the BPAY Master Blueprint PDF and strategic summary to the founder's primary email.
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

RECIPIENT_EMAIL = "syedalirezatalha561@gmail.com"
SUBJECT = "BPAY Master Blueprint & Strategic Execution Roadmap (Confidential)"
PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BPAY_MASTER_BLUEPRINT.pdf")

EMAIL_BODY_HTML = """
<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #0f172a; max-width: 650px; margin: 0 auto; padding: 20px;">
  
  <div style="background: #0f172a; padding: 24px; border-radius: 16px; color: #ffffff; text-align: center; margin-bottom: 24px;">
    <h1 style="margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.5px;">BPAY</h1>
    <p style="margin: 6px 0 0 0; color: #f59e0b; font-size: 13px; font-family: monospace; text-transform: uppercase; font-weight: bold;">
      The Sovereign Benefactor Network • Master Strategic Blueprint
    </p>
  </div>

  <p>Hello,</p>
  
  <p>Per your instruction, here is the complete <strong>Master Blueprint and Execution Roadmap</strong> for <strong>BPAY</strong>. The platform codebase has also been updated with all requested enhancements:</p>

  <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin: 20px 0;">
    <h3 style="margin-top: 0; font-size: 15px; color: #0f172a;">Summary of Key Platform Updates Implemented:</h3>
    <ul style="padding-left: 20px; font-size: 13px; color: #334155; margin-bottom: 0;">
      <li><strong>Navbar Layout Fix</strong>: Completely resolved the squished layout and vertical text wrapping visible in your screenshot. Header is now pristine, responsive, and horizontally aligned.</li>
      <li><strong>Realistic Loyalty Multiplier</strong>: Calibrated the calculator for genuine high-net-worth tiers ($15k/mo to $150k/mo) yielding 1x up to 2x Emirates Skywards / KrisFlyer miles.</li>
      <li><strong>0% Recipient Fees</strong>: Withdrawal and processing fees are automatically computed and covered by the patron at checkout.</li>
      <li><strong>Founding Guild Launch Offer</strong>: Configured the $299/month promotional tier (saving $2,400/yr on $499/mo).</li>
      <li><strong>Global Institutions & Rent Deeds</strong>: Integrated worldwide universities, hospitals, and tenancy lease deed verification.</li>
      <li><strong>Private Video Vault</strong>: Encrypted recipient video appeals visible exclusively to verified Patrons.</li>
      <li><strong>100% Traditional & Digital Rails</strong>: Purged all crypto; now operating strictly via Apple Pay, Google Pay, Cards (Amex/Visa), and Bank Wire.</li>
    </ul>
  </div>

  <h3 style="font-size: 16px; color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">Next Strategic Steps Included in the Blueprint:</h3>
  <ol style="padding-left: 20px; font-size: 13px; color: #334155;">
    <li><strong>Go-To-Market 5-Phase Playbook</strong>: From legal fiscal sponsorship to global scale.</li>
    <li><strong>Brand & Airline Affiliation</strong>: How to formalize co-branded points with Emirates Skywards, Singapore KrisFlyer, and American Express.</li>
    <li><strong>Financial Institution Onboarding</strong>: Stripe Connect, Plaid open banking, and Persona KYC.</li>
    <li><strong>The Creator Blitz (MrBeast & Creators)</strong>: Turnkey pitch for philanthropic creators to clear live boards for viral transparency content.</li>
    <li><strong>Corporate ESG Matching Engine</strong>: Capturing corporate 1:1 match budgets with an 8% enterprise management fee.</li>
    <li><strong>IRS §2503(e) Legal Gift Tax Shield</strong>: How billionaires legally gift unlimited tuition and healthcare with zero gift tax penalty.</li>
  </ol>

  <p style="font-size: 13px; color: #64748b; margin-top: 24px;">
    The complete publication-ready document <strong>BPAY_MASTER_BLUEPRINT.pdf</strong> is attached to this email and saved directly in your project folder.
  </p>

  <div style="border-top: 1px solid #e2e8f0; padding-top: 16px; margin-top: 32px; font-size: 11px; color: #94a3b8; font-family: monospace;">
    BPAY Inc. • Confidential Strategic Architecture Document
  </div>

</body>
</html>
"""

def prepare_message():
    msg = MIMEMultipart()
    msg['From'] = "bpay-system@bpay.network"
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = SUBJECT

    msg.attach(MIMEText(EMAIL_BODY_HTML, 'html'))

    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, 'rb') as f:
            pdf_data = f.read()
        part = MIMEApplication(pdf_data, Name="BPAY_MASTER_BLUEPRINT.pdf")
        part['Content-Disposition'] = f'attachment; filename="BPAY_MASTER_BLUEPRINT.pdf"'
        msg.attach(part)
        print(f"Attached {PDF_PATH} ({len(pdf_data)} bytes)")
    else:
        print(f"Warning: PDF file not found at {PDF_PATH}")

    return msg

def send_via_local_sendmail(msg):
    try:
        from subprocess import Popen, PIPE
        p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
        p.communicate(msg.as_bytes())
        if p.returncode == 0:
            print(f"Successfully dispatched email via sendmail to {RECIPIENT_EMAIL}")
            return True
        else:
            print(f"sendmail exited with return code {p.returncode}")
            return False
    except Exception as e:
        print(f"sendmail error: {e}")
        return False

if __name__ == '__main__':
    msg = prepare_message()
    success = send_via_local_sendmail(msg)
    if not success:
        print("Note: Outbound sendmail requires live mail transport configuration.")
        print(f"Email drafted and prepared for {RECIPIENT_EMAIL}.")
