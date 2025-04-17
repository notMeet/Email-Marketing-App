import boto3

# Initialize clients
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
ses_client = boto3.client('ses')

# Reference your table
table = dynamodb.Table('Contacts')

def lambda_handler(event, context):
    bucket_name = 'my-email-marketing'

    try:
        # Get email template from S3
        email_template = s3_client.get_object(Bucket=bucket_name, Key='email_template.html')
        email_html = email_template['Body'].read().decode('utf-8')

        # Scan DynamoDB table for all contacts
        response = table.scan()
        contacts = response['Items']

        for contact in contacts:
            # Replace placeholders with contact info
            personalized_email = email_html.replace('{{FirstName}}', contact.get('FirstName', ''))

            # Send email
            email_response = ses_client.send_email(
                Source='meet.dd.patel@gmail.com',
                Destination={'ToAddresses': [contact['Email']]},
                Message={
                    'Subject': {'Data': 'Your Weekly Tiny Tales Mail!', 'Charset': 'UTF-8'},
                    'Body': {'Html': {'Data': personalized_email, 'Charset': 'UTF-8'}}
                }
            )
            print(f"Email sent to {contact['Email']}: Response {email_response}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
