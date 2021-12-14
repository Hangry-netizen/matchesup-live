from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import app

def sendgrid(to_email, dynamic_template_data, template_id):
    message = Mail(
        from_email=('no-reply@matchesup.com', 'MatchesUp'),
        to_emails=to_email
        )
    
    message.dynamic_template_data=dynamic_template_data
    
    message.template_id=template_id
    
    try:
        sg = SendGridAPIClient(app.config.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response
        
    except Exception as e:
        return e
