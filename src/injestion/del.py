import base64
import json

def get_user_info(headers: dict):
    """
    Extract user email from the 'X-MS-CLIENT-PRINCIPAL' header.
    Returns a dict with status and message/email.
    """
    principal = headers.get('X-MS-CLIENT-PRINCIPAL')

    if principal:
        try:
            # Decode the base64-encoded principal
            principal_decoded = base64.b64decode(principal).decode('utf-8')
            # Parse it as JSON
            claims = json.loads(principal_decoded)
            # Extract email
            user_email = claims.get('email')

            if user_email:
                return {"status": 200, "user_email": user_email}
            else:
                return {"status": 404, "error": "Email not found in claims."}
        except Exception as e:
            return {"status": 400, "error": f"Decoding error: {str(e)}"}
    else:
        return {"status": 401, "error": "Authentication header not found."}


claims = {
    "email": "testuser@example.com",
    "name": "Test User",
    "roles": ["User"]
}

# Convert to JSON and base64 encode
claims_json = json.dumps(claims)
encoded_claims = base64.b64encode(claims_json.encode('utf-8')).decode('utf-8')

# Simulate HTTP headers
headers = {
    "X-MS-CLIENT-PRINCIPAL": encoded_claims
}

# Call the function
result = get_user_info(headers)

# Print result
print("Result:", result)
