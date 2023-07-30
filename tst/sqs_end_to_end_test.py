import pytest
from src.sqs_consumer.consume_activity import sqs_consumer
from src.sqs_messenger.message_activity import sqs_messenger

def end_to_end_sqs_test():
    queue_name = "test_queue"
    aws_region = "us-east-2"
    test_message = "Test Message"

    messenger = sqs_messenger(queue_name = queue_name, aws_region = aws_region)
    messenger.send_message(test_message)

    consumer = sqs_consumer(queue_name = queue_name, aws_region = aws_region)
    messages_received = consumer.consume_message()

    assert messages_received[0] == test_message



