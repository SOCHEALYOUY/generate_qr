


###testing 2
from flask import Flask, jsonify, request
import socket

# Import your KHQR library
from bakong_khqr import KHQR

app = Flask(__name__)

def get_server_ip():
    """
    Get the local IP address of the server machine.
    This is used to construct the full URL for other devices to access.
    """
    try:
        # Create a socket connection to an external host (doesn't actually connect)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Google's public DNS server
            ip = s.getsockname()[0]
        return ip
    except Exception as e:
        print(f"Error retrieving server IP: {e}")
        return "127.0.0.1"  # Fallback to localhost if IP retrieval fails

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    print("✅ /generate_qr route accessed")  # Debug print

    # Get the server's IP address
    server_ip = get_server_ip()
    server_port = 5000  # Port Flask is running on
    base_url = f"http://{server_ip}:{server_port}"

    # Initialize KHQR with your token
    token = "eyJhbGciOiJIUzI1NiIsI...nMhgG87BWeDg9Lu-_CKe1SMqC0"
    khqr = KHQR(token)

    # Generate the QR code data
    qr = khqr.create_qr(
        bank_account='lyouy_sochea@aclb',
        merchant_name='lyouy_sochea',
        merchant_city='Phnom Penh',
        amount=100,
        currency='KHR',
        store_label='MShop',
        phone_number='85512345678',
        bill_number='TRX01234567',
        terminal_label='Cashier-01',
        static=False
    )

    # Generate MD5 hash of the QR code
    md5 = khqr.generate_md5(qr)

    # Construct the full URL for this endpoint
    full_url = f"{base_url}/generate_qr"

    # Return the QR code data, MD5 hash, and the full URL
    return jsonify({
        'qr': qr,
        'md5': md5,
        'url': full_url  # Include the full URL for accessibility
    })

if __name__ == '__main__':
    # Print the server's IP address and port for easy access
    server_ip = get_server_ip()
    print(f"🚀 Server starting on http://{server_ip}:5000/generate_qr")
    app.run(host='0.0.0.0', port=5000)




