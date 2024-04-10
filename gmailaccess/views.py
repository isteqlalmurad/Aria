# views.py

from django.shortcuts import redirect, HttpResponse
from google_auth_oauthlib.flow import Flow
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import logging


# # Configure a logger for your application
# logger = logging.getLogger(__name__)

# # Assuming SCOPES and REDIRECT_URI are defined elsewhere in your views.py
# SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# REDIRECT_URI = "https://0bac-2a00-23c8-6183-d400-74b9-ce8a-ae78-8ad.ngrok-free.app/authenticate/oauth2callback/"

# # Configure a logger for your application
# logger = logging.getLogger(__name__)


# def gmail_authenticate(request):
#     """Starts the OAuth flow."""
#     flow = Flow.from_client_secrets_file(
#         os.path.join(os.path.dirname(__file__), "credentials.json"),
#         scopes=SCOPES,
#         redirect_uri=REDIRECT_URI,
#     )
#     authorization_url, state = flow.authorization_url(
#         access_type="offline", include_granted_scopes="true", prompt="consent"
#     )

#     # Log the state value that is about to be stored in the session

#     logger.info(f"Storing state in session: {state}")

#     request.session["state"] = state
#     request.session.save()

#     logger.info(f"Session key after saving state: {request.session.session_key}")

#     # Optionally, log the entire session to verify
#     logger.debug(f"Session data: {request.session.items()}")

#     return redirect(authorization_url)


# def oauth2callback(request):
#     """Handles the callback from Google's OAuth 2.0 server."""
#     state = request.session.get("state")

#     # Log the retrieved state from the session
#     logger.info(f"Retrieved state from session: {state}")
#     logger.info(f"Retrieved session key in callback: {request.session.session_key}")

#     if not state:
#         # Handle missing 'state' in session
#         logger.warning("Session state not found. Attempting to authenticate again.")
#         return HttpResponse(
#             "Session state not found. Please try authenticating again.", status=400
#         )

#     flow = Flow.from_client_secrets_file(
#         os.path.join(os.path.dirname(__file__), "credentials.json"),
#         scopes=SCOPES,
#         state=state,
#         redirect_uri=REDIRECT_URI,
#     )
#     authorization_response = request.build_absolute_uri()
#     flow.fetch_token(authorization_response=authorization_response)
#     credentials = flow.credentials
#     request.session["credentials"] = credentials_to_dict(credentials)

#     # Additional functionality: Fetch and save the latest email
#     try:
#         service = build("gmail", "v1", credentials=credentials)

#         user_profile = service.users().getProfile(userId="me").execute()
#         authenticator_email = user_profile["emailAddress"]  # User's email address

#         results = (
#             service.users()
#             .messages()
#             .list(
#                 userId="me",
#                 labelIds=["INBOX"],
#                 maxResults=1,
#                 q="-category:promotions -category:social -category:updates -category:forums",
#             )
#             .execute()
#         )

#         messages = results.get("messages", [])
#         if messages:
#             message_id = messages[0]["id"]
#             message = (
#                 service.users()
#                 .messages()
#                 .get(userId="me", id=message_id, format="full")
#                 .execute()
#             )
#             subject = next(
#                 (
#                     header["value"]
#                     for header in message["payload"]["headers"]
#                     if header["name"].lower() == "subject"
#                 ),
#                 "No Subject",
#             )
#             body = get_message_body(message["payload"])
#             save_email_to_file(subject, body)
#     except Exception as e:
#         logger.error(f"An error occurred while fetching the latest email: {e}")
#         return HttpResponse(
#             f"An error occurred while fetching the latest email: {e}", status=500
#         )

#     logger.info(f"Authentication successful! Latest email saved. {authenticator_email}")
#     return HttpResponse(
#         f"Latest email saved. Subject: {subject}\nAuthenticator's Email: {authenticator_email}"
#     )


# def credentials_to_dict(credentials):
#     """Converts credentials to a dictionary."""
#     return {
#         "token": credentials.token,
#         "refresh_token": credentials.refresh_token,
#         "token_uri": credentials.token_uri,
#         "client_id": credentials.client_id,
#         "client_secret": credentials.client_secret,
#         "scopes": credentials.scopes,
#     }


# def save_email_to_file(subject, body):
#     """Saves the email subject and body to a text file."""
#     with open("latest_emails.txt", "w") as file:  # Changed to "a" for appending
#         file.write(f"Subject: {subject}\nBody:\n{body}\n\n")


# def get_message_body(payload):
#     """Fetches the body of an email from the payload, converting HTML to plain text if necessary."""
#     body = ""
#     if "parts" in payload:
#         for part in payload["parts"]:
#             part_body = get_message_body(part)
#             if part_body:
#                 # Optionally check part['mimeType'] to decide how to concatenate
#                 body += part_body + "\n"  # Simple concatenation, might need adjustment
#     elif "body" in payload and "data" in payload["body"]:
#         try:
#             body_data = base64.urlsafe_b64decode(
#                 payload["body"]["data"] + "=="
#             )  # Ensure padding
#             body_content = body_data.decode("utf-8")
#             if payload.get("mimeType") == "text/html":
#                 soup = BeautifulSoup(body_content, "html.parser")
#                 body = soup.get_text()  # Convert HTML to plain text
#             else:
#                 body = body_content
#         except UnicodeDecodeError:
#             logger.error("Failed to decode email body.")
#     return body


from django.shortcuts import redirect, HttpResponse
from google_auth_oauthlib.flow import Flow
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import logging
from html.parser import HTMLParser

# Configure a logger for your application
logger = logging.getLogger(__name__)

# Assuming SCOPES and REDIRECT_URI are defined elsewhere in your views.py
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
REDIRECT_URI = "https://0bac-2a00-23c8-6183-d400-74b9-ce8a-ae78-8ad.ngrok-free.app/authenticate/oauth2callback/"


def gmail_authenticate(request):
    """Starts the OAuth flow."""
    flow = Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), "credentials.json"),
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent"
    )

    logger.info(f"Storing state in session: {state}")
    request.session["state"] = state
    request.session.save()

    return redirect(authorization_url)


def oauth2callback(request):
    """Handles the callback from Google's OAuth 2.0 server."""
    state = request.session.get("state")
    if not state:
        logger.warning("Session state not found. Attempting to authenticate again.")
        return HttpResponse(
            "Session state not found. Please try authenticating again.", status=400
        )

    flow = Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), "credentials.json"),
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI,
    )
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    request.session["credentials"] = credentials_to_dict(credentials)

    try:

        subject = "No Subject"
        service = build("gmail", "v1", credentials=credentials)
        user_profile = service.users().getProfile(userId="me").execute()
        authenticator_email = user_profile["emailAddress"]
        print(f"login by:  {authenticator_email}")

        query = (
            "-category:promotions -category:social -category:updates -category:forums"
        )
        results = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX"], q=query, maxResults=1)
            .execute()
        )

        messages = results.get("messages", [])
        if messages:
            message_id = messages[0]["id"]
            message = (
                service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )
            subject = next(
                (
                    header["value"]
                    for header in message["payload"]["headers"]
                    if header["name"].lower() == "subject"
                ),
                "No Subject",
            )
            body = get_message_body(message["payload"])
            save_email_to_file(subject, body, authenticator_email)

        return HttpResponse(
            f"Latest email saved. Subject: {subject}\nAuthenticator's Email: {authenticator_email}"
        )
    except Exception as e:
        logger.error(f"An error occurred while fetching the latest email: {e}")
        return HttpResponse(
            f"An error occurred while fetching the latest email: {e}", status=500
        )


def credentials_to_dict(credentials):
    """Converts credentials to a dictionary."""
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def save_email_to_file(subject, body, authenticator_email):
    """Saves the email subject, body, and the authenticator's email to a text file."""
    with open("latest_emails.txt", "a") as file:
        file.write(f"Authenticator's Email: {authenticator_email}\n")
        file.write(f"Subject: {subject}\n")
        file.write("Body:\n")
        file.write(
            body
            + "\n\n"
            + "---------------------------------------------------------------------------------------------------"
            + "\n\n"
        )


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
        self.ignore_data = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ["style", "script"]:
            self.ignore_data = True

    def handle_endtag(self, tag):
        if tag.lower() in ["style", "script"]:
            self.ignore_data = False

    def handle_data(self, d):
        if not self.ignore_data:
            self.text.append(d)

    def get_data(self):
        return "".join(self.text)


# The strip_tags function remains the same
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# Adjusted get_message_body function to use strip_tags for HTML content
def get_message_body(payload, prefer_plain_text=True):
    """Fetches the body of an email from the payload, preferring plain text or HTML based on the flag."""
    body = ""
    if "parts" in payload:  # Multipart message, iterate through parts
        text_part = None
        html_part = None
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain" and not text_part:
                text_part = part
            elif part["mimeType"] == "text/html" and not html_part:
                html_part = part
            if text_part and html_part:
                break  # Stop looking through parts if both are found

        # Decide which part to use based on preference and availability
        if prefer_plain_text and text_part:
            part_to_use = text_part
        elif html_part:
            part_to_use = html_part
        else:
            part_to_use = text_part if text_part else None

        # Recursive call for selected part
        if part_to_use:
            body += get_message_body(part_to_use, prefer_plain_text)
    elif "body" in payload and "data" in payload["body"]:  # Single part message
        body_data = base64.urlsafe_b64decode(payload["body"]["data"] + "==").decode(
            "utf-8"
        )
        if payload.get("mimeType") == "text/html":
            body = strip_tags(body_data)  # Use the strip_tags function for HTML content
        else:
            body = body_data
    return body
