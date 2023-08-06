# pubsubplus-python-client
#
# Copyright 2021 Solace Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# pylint: disable=trailing-whitespace

"""This module contains the acceptable dictionary values for the keys found in
:py:class:`solace.messaging.config.solace_properties.receiver_properties`.
These keys are used to configure the properties of
:py:class:`solace.messaging.receiver.message_receiver.MessageReceiver`."""

RECEIVER_BACK_PRESSURE_STRATEGY_ELASTIC = "ELASTIC"
"""This is a constant containing the acceptable value of the
:py:const:`solace.messaging.config.solace_properties.receiver_properties.DIRECT_BACK_PRESSURE_STRATEGY`
property key. This property-constant mapping can be used in a dict typed configuration
object to configure back pressure for a direct receiver through the
:py:meth:`solace.messaging.builder.direct_message_receiver_builder.from_properties`
method. This method is an alternative to the direct means of setting the back pressure of a
direct receiver through the
:py:meth:`solace.messaging.builder.direct_message_receiver_builder.on_back_pressure_elastic`
method."""

PERSISTENT_REPLAY_ALL = "REPLAY_ALL"  # Replay all the messages from the replay log
"""This is a constant containing the acceptable value of the
:py:const:`solace.messaging.config.solace_properties.receiver_properties.PERSISTENT_MESSAGE_REPLAY_STRATEGY`
property key. This property-constant mapping can be used in a dict typed configuration
object to configure message replay for all messages for persistent receiver through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.from_properties`
method. This method is an alternative to the direct means of setting the replay strategy of a
persistent receiver through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.with_message_replay`
method."""

PERSISTENT_REPLAY_TIME_BASED = "REPLAY_TIME_BASED"  # Replay messages from a specified start time
"""This is a constant containing the acceptable value of the
:py:const:`solace.messaging.config.solace_properties.receiver_properties.PERSISTENT_MESSAGE_REPLAY_STRATEGY`
property key. This property-constant mapping can be used in a dict typed configuration
object to configure message replay from a point of time in replay log for persistent receiver through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.from_properties`
method. This method is an alternative to the direct means of setting the replay strategy of a
persistent receiver through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.with_message_replay`
method."""

PERSISTENT_RECEIVER_DO_NOT_CREATE_MISSING_RESOURCES = "DO_NOT_CREATE"
"""This is a constant containing the acceptable value of the
:py:const:`solace.messaging.config.solace_properties.receiver_properties.PERSISTENT_MISSING_RESOURCE_CREATION_STRATEGY`
property key. This constant represents a strategy to avoid the creation of any 
potentially missing resources (i.e. queues) on a broker. This property-constant mapping
can be used in a dict typed configuration object to configure the strategy for creating
missing resources through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.PersistentMessageReceiverBuilder.from_properties`
method. This method is an alternative to the direct means of setting the missing
resource creation strategy of a persistent message receiver through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.PersistentMessageReceiverBuilder.with_missing_resources_creation_strategy`
method.
"""

PERSISTENT_RECEIVER_CREATE_ON_START_MISSING_RESOURCES = "CREATE_ON_START"
"""This is a constant containing the acceptable value of the
:py:const:`solace.messaging.config.solace_properties.receiver_properties.PERSISTENT_MISSING_RESOURCE_CREATION_STRATEGY`
property key. This constant represents a strategy that tries to create all potentially 
missing resources (i.e. queues) on a broker when the receiver starts.This property-constant mapping
can be used in a dict typed configuration object to configure the strategy for creating
missing resources through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.PersistentMessageReceiverBuilder.from_properties`
method. This method is an alternative to the direct means of setting the missing
resource creation strategy of a persistent message receiver through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.PersistentMessageReceiverBuilder.with_missing_resources_creation_strategy`
method.
"""

PERSISTENT_RECEIVER_AUTO_ACK = "AUTO_ACK"
"""This is a constant containing the acceptable value of the
:py:const:`solace.messaging.config.solace_properties.receiver_properties.PERSISTENT_MESSAGE_ACK_STRATEGY`
property key. This constant represents a strategy for the auto-acknowledgement 
of messages before they are processed by the application with any of receive methods.
This property-constant mapping can be used in a dict typed configuration object to 
configure the strategy for acknowledging received messages through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.PersistentMessageReceiverBuilder.from_properties`
method. This method is an alternative to the direct means of setting the strategy
for acknowledging messages received by a persistent message receiver through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.PersistentMessageReceiverBuilder.with_message_auto_acknowledgement`
method.
"""

PERSISTENT_RECEIVER_CLIENT_ACK = "CLIENT_ACK"
"""This is a constant containing the acceptable value of the
:py:const:`solace.messaging.config.solace_properties.receiver_properties.PERSISTENT_MESSAGE_ACK_STRATEGY`
property key. This constant represents a strategy for the manual acknowledgement of
messages by the client. This property-constant mapping can be used in a dict typed
configuration object to configure the strategy for acknowledging received messages
through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.PersistentMessageReceiverBuilder.from_properties`
method. This method is an alternative to the direct means of setting the strategy
for acknowledging messages received by a persistent message receiver through the
:py:meth:`solace.messaging.builder.persistent_message_receiver_builder.PersistentMessageReceiverBuilder.with_message_client_acknowledgement`
method.
"""