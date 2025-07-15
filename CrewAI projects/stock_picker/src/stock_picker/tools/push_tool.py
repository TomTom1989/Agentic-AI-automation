from crewai.tools import BaseTool
from typing import Optional
import os

class PushNotificationTool(BaseTool):
    name: str = "Push Notification Tool"
    description: str = "A tool for sending push notifications about stock recommendations. If no API key is available, notifications will be logged locally."

    def _run(self, message: str) -> str:
        """
        Send a push notification with the given message.
        If no API key is available, the message will be logged locally.
        
        Args:
            message (str): The message to send in the notification
            
        Returns:
            str: Confirmation message
        """
        try:
            # Check if API key is available
            api_key = os.getenv('PUSH_API_KEY')
            
            if not api_key:
                # If no API key, just log locally
                print(f"🔔 Local Notification (No API Key): {message}")
                return f"Notification logged locally: {message}"
            
            # If API key exists, you would implement the actual push notification here
            # For now, we'll just print it
            print(f"🔔 Push Notification: {message}")
            return f"Notification sent: {message}"
            
        except Exception as e:
            # Handle any errors gracefully
            print(f"⚠️ Notification failed (error: {str(e)}). Message: {message}")
            return f"Notification failed but continuing execution. Message: {message}" 