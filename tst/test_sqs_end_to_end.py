import sys
import os

# Get the parent directory of the current directory (tests)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)

import pytest
from src.sqs_consumer.consume_activity import sqs_consumer
from src.sqs_messenger.message_activity import sqs_messenger

def test_end_to_end():
    queue_name = "test_queue"
    aws_region = "us-east-2"
    test_message = "Test Message"

    messenger = sqs_messenger(queue_name = queue_name, aws_region = aws_region)
    messenger.send_message(test_message)

    consumer = sqs_consumer(queue_name = queue_name, aws_region = aws_region)
    messages_received = consumer.consume_message()

    assert messages_received[0] == test_message



