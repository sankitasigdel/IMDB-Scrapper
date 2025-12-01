from abc import ABC, abstractmethod
import os
from appscript import app, k
from mactypes import Alias

class IEmailHandler(ABC):
    """Interface for email operations"""
    
    @abstractmethod
    def send_email(self, to_email: str, subject: str, body: str, attachment_path: str = None):
        """Send email with optional attachment"""
        pass

class OutlookEmailHandler(IEmailHandler):
    """Handles email sending operations using Microsoft Outlook"""
    
    def __init__(self):
        self.outlook = app('Microsoft Outlook')
    
    def send_email(self, to_email: str, subject: str, body: str, attachment_path: str = None):
        """Send email via Outlook with Excel attachment"""
        try:
            # Create a new outgoing message
            msg = self.outlook.make(
                new=k.outgoing_message,
                with_properties={
                    k.subject: subject,
                    k.plain_text_content: body
                }
            )
            
            # Add recipient
            msg.make(
                new=k.recipient,
                with_properties={
                    k.email_address: {
                        k.name: to_email,
                        k.address: to_email
                    }
                }
            )
            
            # Add attachment if provided
            if attachment_path:
                # Expand full path (no ~)
                full_path = os.path.expanduser(attachment_path)
                
                if os.path.exists(full_path):
                    try:
                        # Use Alias to fix the -2700 error!
                        msg.make(
                            new=k.attachment,
                            with_properties={k.file: Alias(full_path)}
                        )
                        print(f"✓ Attached: {full_path}")
                    except Exception as e:
                        print(f"Error attaching file: {e}")
                        return False
                else:
                    print(f"⚠ Attachment not found: {full_path}")
                    return False
            
            # Display the email
            msg.open()
            msg.activate()
            
            # Send the email
            msg.send()
            
            print(f"✓ Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email via Outlook: {e}")
            return False