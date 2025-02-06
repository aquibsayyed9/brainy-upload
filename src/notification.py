import os
import requests

SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

def send_slack_alert(message, is_error=False):
    """Send a message to Slack"""
    try:
        if not SLACK_WEBHOOK_URL:
            print("Slack webhook URL not configured")
            return False

        emoji = "🚨" if is_error else "ℹ️"
        payload = {
            "text": f"{emoji} {message}"
        }

        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending Slack notification: {e}")
        return False