"""sampler for using share_name on request reply message publishing and receiving"""
import time
from concurrent.futures.thread import ThreadPoolExecutor

from solace.messaging.config.solace_properties.message_properties import SEQUENCE_NUMBER
from solace.messaging.messaging_service import MessagingService
from solace.messaging.publisher.outbound_message import OutboundMessage
from solace.messaging.publisher.request_reply_message_publisher import RequestReplyMessagePublisher
from solace.messaging.receiver.request_reply_message_receiver import RequestMessageHandler, Replier
from solace.messaging.resources.share_name import ShareName
from solace.messaging.resources.topic import Topic
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace_sampler.sampler_boot import SolaceConstants, SamplerBoot

constants = SolaceConstants
boot = SamplerBoot()
MAX_SLEEP = 10


class RequestMessageHandlerImpl(RequestMessageHandler):
    """this is a callback for request message"""

    def __init__(self, messaging_service=None):
        super().__init__()
        self._messaging_service = messaging_service

    def on_message(self, message: 'InboundMessage', replier: 'Replier'):
        topic = message.get_destination_name()
        payload_as_bytes = message.get_payload_as_bytes()
        payload_as_string = message.get_payload_as_string()
        print("\n" + f"Receiver A \n"
                     f"CALLBACK: Message Received on Topic: {topic}.\n"
                     f"Message Bytes: {payload_as_bytes} \n"
                     f"Message String: {payload_as_string}")

        response_message: OutboundMessage = self._messaging_service.message_builder().build(payload="Pong")
        replier.reply(response_message=response_message)


class RequestMessageHandlerImpl2(RequestMessageHandler):
    """this is a callback for request message"""

    def __init__(self, messaging_service=None):
        super().__init__()
        self._messaging_service = messaging_service

    def on_message(self, message: 'InboundMessage', replier: 'Replier'):
        topic = message.get_destination_name()
        payload_as_bytes = message.get_payload_as_bytes()
        payload_as_string = message.get_payload_as_string()
        print("\n" + f"Receiver B \n"
                     f"CALLBACK: Message Received on Topic: {topic}.\n"
                     f"Message Bytes: {payload_as_bytes} \n"
                     f"Message String: {payload_as_string}")
        response_message: OutboundMessage = self._messaging_service.message_builder().build(payload="Pong")
        replier.reply(response_message=response_message)


class HowToUseShareNameWithRequestReplyPattern:
    """class contains methods on different ways to publish a request reply message"""

    @staticmethod
    def publish_request_and_process_response_message_async(service: MessagingService, request_destination: Topic,
                                                           reply_timeout: int):
        """Mimics microservice that performs a async request
        Args:
            service: connected messaging service
            request_destination: where to send a request (it is same for requests and responses)
            reply_timeout: the reply timeout
        """
        topic = Topic.of(request_destination)
        requester: RequestReplyMessagePublisher = service.request_reply() \
            .create_request_reply_message_publisher_builder().build().start()

        ping_message = service.message_builder().build(payload='Ping',
                                                       additional_message_properties={SEQUENCE_NUMBER: 123})

        publish_request_async = requester.publish(request_message=ping_message,
                                                  request_destination=topic,
                                                  reply_timeout=reply_timeout)
        # we can get the reply from the future
        print(publish_request_async.result())

    @staticmethod
    def request_reply_message_consume(messaging_service: MessagingService, consumer_subscription: str):
        """This method will create an receiver instance to receive str or byte array type message"""
        try:
            topic_subscription = TopicSubscription.of(consumer_subscription)
            group_name = ShareName.of('test')

            receiver = messaging_service.request_reply(). \
                create_request_reply_message_receiver_builder().build(request_topic_subscription=topic_subscription,
                                                                      share_name=group_name)
            receiver.start()
            message_handler = RequestMessageHandlerImpl(messaging_service=messaging_service)
            receiver.receive_message(message_handler)
            print(f"Subscribed to: {consumer_subscription}")
            while True:
                global MAX_SLEEP
                if MAX_SLEEP <= 0:
                    break
                else:
                    MAX_SLEEP -= 1
                    time.sleep(1)
        finally:
            messaging_service.disconnect()
            receiver.terminate(0)

    @staticmethod
    def request_reply_message_consume2(messaging_service: MessagingService, consumer_subscription: str):
        """This method will create an receiver instance to receive str or byte array type message"""
        try:
            topic_subscription = TopicSubscription.of(consumer_subscription)
            group_name = ShareName.of('test')

            receiver = messaging_service.request_reply(). \
                create_request_reply_message_receiver_builder().build(request_topic_subscription=topic_subscription,
                                                                      share_name=group_name)
            receiver.start()
            message_handler = RequestMessageHandlerImpl2(messaging_service=messaging_service)
            receiver.receive_message(message_handler)
            print(f"Subscribed to: {consumer_subscription}")
            while True:
                global MAX_SLEEP
                if MAX_SLEEP <= 0:
                    break
                else:
                    MAX_SLEEP -= 1
                    time.sleep(1)
        finally:
            messaging_service.disconnect()
            receiver.terminate(0)

    @staticmethod
    def run_subscribers(service, consumer_subscription, reply_timeout):
        """
        :return:
        """

        print("Execute request reply consume - String")
        with ThreadPoolExecutor(max_workers=3) as e:
            e.submit(HowToUseShareNameWithRequestReplyPattern.request_reply_message_consume, messaging_service=service,
                     consumer_subscription=consumer_subscription)
            e.submit(HowToUseShareNameWithRequestReplyPattern.request_reply_message_consume2, messaging_service=service,
                     consumer_subscription=consumer_subscription)
            for counter in range(1, 3):
                e.submit(HowToUseShareNameWithRequestReplyPattern.publish_request_and_process_response_message_async,
                         service=service,
                         request_destination=consumer_subscription, reply_timeout=reply_timeout)

    @staticmethod
    def run():
        service = MessagingService.builder().from_properties(boot.broker_properties()).build()
        service.connect_async()
        consumer_subscription = 'request_reply/pub_sub/sampler'
        reply_timeout = 5000

        HowToUseShareNameWithRequestReplyPattern.run_subscribers(service=service,
                                                                 consumer_subscription=consumer_subscription,
                                                                 reply_timeout=reply_timeout)


if __name__ == '__main__':
    HowToUseShareNameWithRequestReplyPattern.run()
