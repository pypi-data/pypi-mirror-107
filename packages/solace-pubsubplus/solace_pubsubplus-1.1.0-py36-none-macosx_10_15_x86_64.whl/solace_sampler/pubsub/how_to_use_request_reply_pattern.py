"""sampler for request reply message publishing and receiving"""
from concurrent.futures.thread import ThreadPoolExecutor

from solace.messaging.config.solace_properties.message_properties import SEQUENCE_NUMBER
from solace.messaging.messaging_service import MessagingService
from solace.messaging.publisher.outbound_message import OutboundMessage
from solace.messaging.publisher.request_reply_message_publisher import RequestReplyMessagePublisher
from solace.messaging.receiver.request_reply_message_receiver import RequestReplyMessageReceiver, \
    RequestMessageHandler, Replier
from solace.messaging.resources.topic import Topic
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace_sampler.sampler_master import SamplerMaster


class RequestMessageHandlerImpl(RequestMessageHandler):
    """this is a callback for request message"""

    def __init__(self, messaging_service=None):
        super().__init__()
        self._messaging_service = messaging_service

    def on_message(self, message: 'InboundMessage', replier: 'Replier'):
        message.get_destination_name()

        response_message: OutboundMessage = self._messaging_service.message_builder().build(payload="Pong")
        replier.reply(response_message=response_message)


class HowToUseRequestReplyPattern:
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

        requester: RequestReplyMessagePublisher = service.request_reply() \
            .create_request_reply_message_publisher_builder().build().start()

        ping_message = service.message_builder().build(payload='Ping',
                                                       additional_message_properties={SEQUENCE_NUMBER: 123})

        publish_request_async = requester.publish(request_message=ping_message,
                                                  request_destination=request_destination,
                                                  reply_timeout=reply_timeout)
        # we can get the reply from the future
        print(publish_request_async.result())

    @staticmethod
    def publish_request_and_process_response_message_blocking(service: MessagingService, request_destination: Topic,
                                                              reply_timeout: int):
        """Mimics microservice that performs a blocking request

        Args:
            service: connected messaging service
            request_destination: where to send a request (it is same for requests and responses)
            reply_timeout: the reply timeout
        """
        requester: RequestReplyMessagePublisher = service.request_reply() \
            .create_request_reply_message_publisher_builder().build().start()

        ping_message: OutboundMessage = service.message_builder().build(payload='Ping')
        try:

            reply = requester.publish_await_response(request_message=ping_message,
                                                     request_destination=request_destination,
                                                     reply_timeout=reply_timeout)
            print(f"reply: {reply}")
        except TimeoutError as e:
            print(e)

    @staticmethod
    def receive_request_and_send_response_message(service: MessagingService, for_requests: TopicSubscription):
        """Mimics microservice that performs a response

        Args:
            service: connected messaging service
            for_requests: where to expect requests
        """

        request_receiver: RequestReplyMessageReceiver = service.request_reply() \
            .create_request_reply_message_receiver_builder().build(for_requests).start()

        message_handler = RequestMessageHandlerImpl(messaging_service=service)

        request_receiver.receive_message(message_handler)

    @staticmethod
    def async_request_and_response(service: MessagingService, request_destination: Topic,
                                   for_requests: TopicSubscription, reply_timeout: int):
        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(HowToUseRequestReplyPattern.receive_request_and_send_response_message,
                     service=service,
                     for_requests=for_requests)
            e.submit(HowToUseRequestReplyPattern.publish_request_and_process_response_message_async,
                     service=service,
                     request_destination=request_destination,
                     reply_timeout=reply_timeout)

    @staticmethod
    def blocking_request_and_response(service: MessagingService, request_destination: Topic,
                                      for_requests: TopicSubscription, reply_timeout: int):

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(HowToUseRequestReplyPattern.receive_request_and_send_response_message,
                     service=service,
                     for_requests=for_requests)
            e.submit(HowToUseRequestReplyPattern.publish_request_and_process_response_message_blocking,
                     service=service,
                     request_destination=request_destination,
                     reply_timeout=reply_timeout)

    @staticmethod
    def run():
        messaging_service = None
        try:
            reply_timeout = 5000
            topic_name = f'request_reply/pub_sub/sampler'
            topic = Topic.of(topic_name)
            topic_subscription = TopicSubscription.of(topic_name)
            messaging_service = SamplerMaster.connect_messaging_service()

            HowToUseRequestReplyPattern.async_request_and_response(service=messaging_service,
                                                                   request_destination=topic,
                                                                   for_requests=topic_subscription,
                                                                   reply_timeout=reply_timeout)

            HowToUseRequestReplyPattern.blocking_request_and_response(service=messaging_service,
                                                                      request_destination=topic,
                                                                      for_requests=topic_subscription,
                                                                      reply_timeout=reply_timeout)
        finally:
            if messaging_service:
                messaging_service.disconnect()


if __name__ == '__main__':
    HowToUseRequestReplyPattern.run()
