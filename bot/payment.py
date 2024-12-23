import requests
from requests.auth import HTTPBasicAuth

# Razorpay API credentials
key_id = "rzp_live_eiafqabWZNkjVj"
key_secret = "mjNEgUPUzFbqxfAEltyOdIOD"

# Payment ID from Razorpay response
payment_id = "pay_PaghP9DTWkiIz1"

# Razorpay API URL
url = f"https://api.razorpay.com/v1/payments/{payment_id}"

# Fetch payment details
response = requests.get(url, auth=HTTPBasicAuth(key_id, key_secret))

# Print response
if response.status_code == 200:
    print("Payment Details:", response.json())
else:
    print("Error:", response.json())
