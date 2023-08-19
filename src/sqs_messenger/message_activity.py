import boto3

class sqs_messenger(object):
    def __init__(self, queue_name : str, aws_region: str):
        self.name = queue_name
        self.aws_region = aws_region
        self.queue_url = get_queue(queue_name = queue_name, aws_region = aws_region)
    
    def send_message(self, message: str):
        sqs = boto3.client('sqs', region_name = self.aws_region)

        response = sqs.send_message(
            QueueUrl = self.queue_url,
            MessageBody=message
        )

        return response['MessageId']

def get_queue(queue_name : str, aws_region : str) -> str:
    sqs = boto3.client('sqs', region_name=aws_region)
    
    # Check if the queue exists
    response = sqs.list_queues(QueueNamePrefix=queue_name)
    queue_urls = response.get('QueueUrls', [])
    
    if queue_urls:
        return queue_urls[0]
    else:
        raise Exception('The queue that you are trying to get does not exist')
    assert queue_urls