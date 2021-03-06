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

from test import SchemaRegistryFailoverTest
import time

# Specify retry frequency and retry window
# For a clean kill of master, where master election
# should be very fast, expect about 10 retries w/.02 seconds between tries
# should be sufficient


# For a kill -9, master reelection won't take place until zookeeper timeout, or about 4 seconds
class MasterCleanFailover(SchemaRegistryFailoverTest):
    """
    Begin registering schemas; part way through, cleanly kill the master.
    """
    def __init__(self, test_context):
        # Expect leader reelection to take less than .2 sec in a clean shutdown
        super(MasterCleanFailover, self).__init__(
            test_context, num_zk=1, num_brokers=1, num_schema_registry=3, retry_wait_sec=.02, num_retries=100)

    def drive_failures(self):
        """
        Wait a bit, and then kill the master node cleanly.
        """
        time.sleep(3)
        master_node = self.schema_registry.get_master_node()
        self.schema_registry.stop_node(master_node)


class MasterHardFailover(SchemaRegistryFailoverTest):
    """
    Begin registering schemas; part way through, hard kill the master (kill -9)
    """
    def __init__(self, test_context):
        # Default zookeeper session timeout is 10 seconds
        super(MasterHardFailover, self).__init__(
            test_context, num_zk=1, num_brokers=1, num_schema_registry=3, retry_wait_sec=.1, num_retries=1500)

    def drive_failures(self):
        """
        Wait a bit, and then kill -9 the master
        """
        time.sleep(3)
        master_node = self.schema_registry.get_master_node()
        self.schema_registry.stop_node(master_node, clean_shutdown=False)


class CleanBounce(SchemaRegistryFailoverTest):
    def __init__(self, test_context):
        # Expect leader reelection to take less than .2 sec in a clean shutdown
        super(CleanBounce, self).__init__(
            test_context, num_zk=1, num_brokers=1, num_schema_registry=3, retry_wait_sec=.02, num_retries=100)

    def drive_failures(self):
        """
        Bounce master several times - i.e. kill master with SIGTERM aka kill aka kill -15 and restart
        """
        # Bounce leader several times with some wait in-between
        for i in range(5):
            prev_master_node = self.schema_registry.get_master_node()
            self.schema_registry.restart_node(prev_master_node, wait_sec=5)


class HardBounce(SchemaRegistryFailoverTest):
    def __init__(self, test_context):
        super(HardBounce, self).__init__(
            test_context, num_zk=1, num_brokers=1, num_schema_registry=3, retry_wait_sec=.3, num_retries=100)

    def drive_failures(self):
        """
        Bounce master several times - i.e. kill master with SIGKILL aka kill -9 and restart
        """
        # Bounce leader several times with some wait in-between
        for i in range(6):
            prev_master_node = self.schema_registry.get_master_node()
            self.schema_registry.restart_node(prev_master_node, wait_sec=5, clean_shutdown=False)

