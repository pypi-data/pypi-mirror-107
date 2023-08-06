# pubsubplus-python-client
#
# Copyright 2021 Solace Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module contains the implementation class and methods for the DirectMessageReceiverBuilder"""
# pylint: disable=missing-class-docstring, missing-function-docstring
import logging
from enum import Enum
from typing import List

from solace.messaging.builder._impl._message_receiver_builder import _MessageReceiverBuilder
from solace.messaging.builder.direct_message_receiver_builder import DirectMessageReceiverBuilder
from solace.messaging.receiver._impl._direct_message_receiver import _DirectMessageReceiver
from solace.messaging.receiver._impl._receiver_utilities import validate_subscription_type
from solace.messaging.resources.share_name import ShareName, _ShareName
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace.messaging.utils._solace_utilities import is_type_matches
from solace.messaging.config.solace_properties import receiver_properties
from solace.messaging.config.solace_constants import receiver_constants

logger = logging.getLogger('solace.messaging.receiver')


class DirectMessageReceiverBackPressure(Enum):  # pydoc: no  # pylint: disable=missing-class-docstring
    # class which extends Enum to hold the direct receiver back pressure
    # these enum are internal only and are used for quick comparisons
    # in direct receivers

    # Unbound buffer which will continue to add capacity as needed until memory failure.
    Elastic = 0  # pylint: disable=invalid-name


class _DirectMessageReceiverBuilder(_MessageReceiverBuilder, DirectMessageReceiverBuilder):

    def __init__(self, messaging_service):
        super().__init__(messaging_service)
        self._receiver_back_pressure_type: DirectMessageReceiverBackPressure = DirectMessageReceiverBackPressure.Elastic

    def with_subscriptions(self, subscriptions: List[TopicSubscription]) -> 'DirectMessageReceiverBuilder':
        #
        # Add a list of subscriptions to be applied to all DirectMessageReceiver subsequently created with
        # this builder.
        # Args:
        #     subscriptions (List[TopicSubscription]): subscriptions list of topic subscriptions to be added
        # Returns:
        #     DirectMessageReceiverBuilder instance for method chaining
        #
        is_type_matches(subscriptions, List, logger=logger)
        self._topic_subscriptions = list()
        for topic in subscriptions:
            validate_subscription_type(subscription=topic, logger=logger)
            self._topic_subscriptions.append(topic.get_name())
        return self

    def from_properties(self, configuration: dict) -> 'DirectMessageReceiverBuilder':
        #
        # Set DirectMessageReceiver properties from the dictionary of (property,value) tuples.
        # Args:
        #     configuration (dict): configuration properties
        # Returns:
        #     DirectMessageReceiverBuilder instance for method chaining
        #
        is_type_matches(configuration, dict, logger=logger)
        self.__build_back_pressure_from_props(configuration)
        return self

    def build(self, shared_subscription_group: ShareName = None) -> 'DirectMessageReceiver':
        topic_dict = dict()
        topic_dict['subscriptions'] = self._topic_subscriptions
        if shared_subscription_group:
            is_type_matches(shared_subscription_group, ShareName, logger=logger)
            name = shared_subscription_group.get_name()
            share_name = _ShareName(name)
            share_name.validate()
            topic_dict['group_name'] = name
        return _DirectMessageReceiver(self._messaging_service, topic_dict)

    def on_back_pressure_elastic(self) -> DirectMessageReceiverBuilder:
        #
        # :py:class:`solace.messaging.receiver.direct_message_receiver.DirectMessageReceiver` that are built
        # will buffer all incoming messages until memory is exhausted.
        #
        # Usage of this strategy can lead to memory shortage situations and can cause applications to crash.
        # This strategy may be useful for microservices which are running in a managed environment that can
        # detect crashes and perform restarts of a microservice.
        # Returns:
        #     DirectMessageReceiverBuilder for method chaining.
        #
        self._receiver_back_pressure_type = DirectMessageReceiverBackPressure.Elastic
        logger.debug('Enabled elastic back pressure for direct message receiver; buffer/queue capacity: MAX')
        return self

    def __build_back_pressure_from_props(self, configuration: dict):
        if receiver_properties.DIRECT_BACK_PRESSURE_STRATEGY in configuration.keys():
            if configuration[receiver_properties.DIRECT_BACK_PRESSURE_STRATEGY] \
                    == receiver_constants.RECEIVER_BACK_PRESSURE_STRATEGY_ELASTIC:
                self.on_back_pressure_elastic()
