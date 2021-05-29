from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import app


def send_gsc_consent_email(to_email, dynamic_template_data):
    message = Mail(
        from_email=('noreply@matchesup.com', 'MatchesUp'),
        to_emails=to_email
        )
    
    message.dynamic_template_data=dynamic_template_data
    
    message.template_id="d-fcb0e7483d4448319fa772341765a581"
    
    try:
        sg = SendGridAPIClient(app.config.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response

    except Exception as e:
        return e.message

def send_reference_email(to_email, dynamic_template_data):
    message = Mail(
        from_email=('noreply@matchesup.com', 'MatchesUp'),
        to_emails=to_email
        )
    
    message.dynamic_template_data=dynamic_template_data

    message.template_id="d-6af1d902e5544dc68eeab4fe99809219"
    
    try:
        sg = SendGridAPIClient(app.config.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response
        
    except Exception as e:
        return e

def send_approve_reference_email(to_email, dynamic_template_data):
    message = Mail(
        from_email=('noreply@matchesup.com', 'MatchesUp'),
        to_emails=to_email
        )
    
    message.dynamic_template_data=dynamic_template_data
    
    message.template_id="d-b0df696531cb4b8fb4234b6ff1a05aa0"
    
    try:
        sg = SendGridAPIClient(app.config.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response
        
    except Exception as e:
        return e

def send_approved_email(to_email, dynamic_template_data):
    message = Mail(
        from_email=('noreply@matchesup.com', 'MatchesUp'),
        to_emails=to_email
        )
    
    message.dynamic_template_data=dynamic_template_data
    
    message.template_id="d-e0573f50445145e9ba6542744ff4053a"
    
    try:
        sg = SendGridAPIClient(app.config.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response
        
    except Exception as e:
        return e