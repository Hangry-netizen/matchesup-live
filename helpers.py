import boto3, botocore
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import app

# ec2 = boto3.client(
#     "ec2",
#     "ap-southeast-1",
#     aws_access_key_id=app.config.get("EC2_KEY"),
#     aws_secret_access_key=app.config.get("EC2_SECRET")
# )

# response = ec2.describe_instances()
# #print(response)


# conn = ec2.run_instances(InstanceType="t2.micro",
#                          MaxCount=1,
#                          MinCount=1,
#                          ImageId="ami-0df7a207adb9748c7")
# print(conn)

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
