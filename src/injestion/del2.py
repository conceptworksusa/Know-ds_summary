import logging
import jwt
import requests
from azure.identity import DefaultAzureCredential

class GetUserInfo:
    def get_azure_username(self):
        """
        Retrieves the current Azure username using DefaultAzureCredential.
        Handles both local and Azure container environments.
        """
        try:
            logger = logging.getLogger(__name__)
            logger.info("Getting Azure username using DefaultAzureCredential...")

            # Initialize credential
            credential = DefaultAzureCredential()
            logger.info("Azure credential retrieved")

            # Get token for Microsoft Graph API
            token = credential.get_token("https://graph.microsoft.com/.default")
            access_token = token.token
            logger.info("Access token retrieved")

            # Try to decode token for 'upn'
            try:
                decoded_token = jwt.decode(
                    access_token,
                    options={"verify_signature": False, "verify_aud": False}
                )
                logger.info("Decoded token: " + str(decoded_token))

                username = decoded_token.get('upn') or decoded_token.get('preferred_username')
                if username:
                    return username
                else:
                    logger.info("UPN not in token, trying Graph API...")
            except Exception as decode_error:
                logger.warning(f"JWT decode failed, trying Graph API: {decode_error}")

            # Fallback: Call Microsoft Graph API /me endpoint
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

            if response.ok:
                user_info = response.json()
                username = user_info.get('userPrincipalName') or user_info.get('mail')
                if username:
                    return username
                else:
                    return "Username not found in Graph response."
            else:
                return f"Graph API error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Error getting Azure username: {e}"
