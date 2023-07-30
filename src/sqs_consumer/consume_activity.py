import boto3

class sqs_consumer(object):
    def __init__(self, queue_name : str, aws_region: str):
        self.queue_name = queue_name
        self.aws_region = aws_region
        self.queue_url = get_queue(queue_name, aws_region)
    
    def consume_message(self, 
                        number_of_polls : int = 10, 
                        wait_time : int = 2, 
                        max_messages: int = 1) -> list:
        sqs = boto3.client('sqs', region_name = self.aws_region)

        messages_received = []
        for i in range(number_of_polls):
            response = sqs.receive_message(
                QueueUrl = self.queue_url,
                MaxNumberOfMessages = max_messages,  # Adjust as needed (maximum number of messages to receive at once)
                WaitTimeSeconds = wait_time,  # Adjust as needed (how long to wait for messages in seconds)
            )
            
            if 'Messages' in response:
                for message in response['Messages']:
                    # Process the message (replace this with your own message processing logic)
                    messages_received.append(message['Body'])                    
                    # Delete the message from the queue after processing
                    sqs.delete_message(
                        QueueUrl = self.queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
        return messages_received

def get_queue(queue_name : str, aws_region : str) -> str:
    sqs = boto3.client('sqs', region_name = aws_region)
    
    # Check if the queue exists
    response = sqs.list_queues(QueueNamePrefix = queue_name)
    queue_urls = response.get('QueueUrls', [])
    
    if queue_urls:
        return queue_urls[0]
    else:
        raise Exception("The SQS Queue does not exist")