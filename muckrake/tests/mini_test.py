# Copyright 2015 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ducktape.tests.test import Test

from muckrake.services.zookeeper import ZookeeperService
from muckrake.services.kafka import KafkaService


class MiniTest(Test):
    def __init__(self, test_context):
        super(MiniTest, self).__init__(test_context=test_context)

        self.zk = ZookeeperService(test_context, 1)
        self.kafka = KafkaService(test_context, 1, self.zk)

    def test(self):
        self.zk.start()
        self.kafka.start()

