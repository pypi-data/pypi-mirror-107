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


"""
    Module to handle back pressure configuration in
    :py:class:`solace.messaging.builder.direct_message_receiver_builder.DirectMessageReceiverBuilder`.
"""
from abc import ABC, abstractmethod

__all__ = ["DirectReceiverBackPressureConfiguration"]


class DirectReceiverBackPressureConfiguration(ABC):
    """
    A class that abstracts configuration of back-pressure features
    All methods in this class are mutually exclusive and therefore should be called only once.
    The default back-pressure configuration is to internally handle back pressure. This is equivalent
    to on_back_pressure_elastic().
    """

    @abstractmethod
    def on_back_pressure_elastic(self):
        """
        Configures the receiver to buffer indefinitely, consuming as much memory as required for buffered messages.
        On memory exhaustion receiver behavior is undefined. Elastic, essentially no, back-pressure is an ideal strategy
        for applications that process received messages at a low rate with infrequent small bursts of activity.
        It should not be considered for use in all cases.
        Raises:
            PubSubPlusClientError: When unable to configure the receiver.
        """
