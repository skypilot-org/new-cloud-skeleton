'''
This file should be placed at sky/skylet/providers/{cloudname}/node_provider.py

Methods that start with an underscore (_) are specific to SkyPilot,
and not part of the ray NodeProvider class definition.

Template Usage:
    - Replace all the FILL_INs with your own code.
'''

import logging
from typing import Any, Dict, List, Optional

from threading import RLock

from ray.autoscaler.node_provider import NodeProvider
from ray.autoscaler.tags import TAG_RAY_CLUSTER_NAME


# FILL_IN: Import your python cloud library here.
# Replace library usage found in this template.
# A wrapper/helper is recommended to keep the code clean.
import fluffycloud_api as fc_api

logger = logging.getLogger(__name__)


class FluffyCloudError(Exception):
    pass


def synchronized(func):
    def wrapper(self, *args, **kwargs):
        self.lock.acquire()
        try:
            return func(self, *args, **kwargs)
        finally:
            self.lock.release()

    return wrapper


class FluffyCloudNodeProvider(NodeProvider):
    """Node Provider for FluffyCloud."""

    def __init__(self, provider_config, cluster_name):
        NodeProvider.__init__(self, provider_config, cluster_name)

        self.lock = RLock()
        self.cached_nodes = {}

        # FILL_IN: Load credentials if needed for your cloud library.
        self.api_key =  # FILL_IN: Read from credentials file
        self.ssh_key_name =  # FILL_IN: Read from credentials file

    def non_terminated_nodes(self, tag_filters: Dict[str, str]) -> List[str]:
        """Return a list of node ids filtered by the specified tags dict.

        This list must not include terminated nodes. For performance reasons,
        providers are allowed to cache the result of a call to
        non_terminated_nodes() to serve single-node queries
        (e.g. is_running(node_id)). This means that non_terminated_nodes()
        must be called again to refresh results.
        """
        nodes = self._get_filtered_nodes(tag_filters=tag_filters)

        # TEMPLATE ACTION: Filter out terminated nodes

        return [node_id for node_id, _ in nodes.items()]

    def is_running(self, node_id: str) -> bool:
        """Return whether the specified node is running."""
        return self._get_cached_node(node_id=node_id) is not None

    def is_terminated(self, node_id: str) -> bool:
        """Return whether the specified node is terminated."""
        return self._get_cached_node(node_id=node_id) is None

    def node_tags(self, node_id: str) -> Dict[str, str]:
        """Returns the tags of the given node (string dict)."""
        return self._get_cached_node(node_id=node_id)['tags']

    def external_ip(self, node_id: str) -> str:
        """Returns the external ip of the given node."""
        return self._get_cached_node(node_id=node_id)['ip']

    def internal_ip(self, node_id: str) -> str:
        """Returns the internal ip (Ray ip) of the given node."""
        return self._get_cached_node(node_id=node_id)['ip']

    def create_node(self, node_config: Dict[str, Any], tags: Dict[str, str], count: int) -> Optional[Dict[str, Any]]:
        """Creates a number of nodes within the namespace."""
        # Get the tags
        config_tags = node_config.get('tags', {}).copy()
        config_tags.update(tags)
        config_tags[TAG_RAY_CLUSTER_NAME] = self.cluster_name

        # Create nodes
        ttype = node_config['InstanceType']
        region = self.provider_config['region']

        for _ in range(count):
            instance_id = fc_api.launch(name=self.cluster_name,
                                        instance_type=ttype,
                                        region=region,
                                        api_key=self.api_key,
                                        ssh_key_name=self.ssh_key_name)

        if instance_id is None:
            raise FluffyCloudError('Failed to launch instance.')

        fc_api.set_tags(instance_id, config_tags, self.api_key)

        # FILL_IN: Only return after all nodes are booted.
        # If needed poll fc_api.list_instances() to wait for status == 'running'

    @synchronized
    def set_node_tags(self, node_id: str, tags: Dict[str, str]) -> None:
        """Sets the tag values (string dict) for the specified node."""
        node = self._get_node(node_id)
        node['tags'].update(tags)
        fc_api.set_tags(node_id, node['tags'], self.api_key)  # FILL_IN

    def terminate_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Terminates the specified node."""
        fc_api.remove(node_id, self.api_key)  # FILL_IN

    @synchronized
    def _get_filtered_nodes(self, tag_filters: Dict[str, str]) -> Dict[str, Any]:
        '''
        SkyPilot Method
        Caches the nodes with the given tag_filters.

        Return Example:
        {
            instance_id_1: {
                status: ...,
                tags: ...,
                name: ...,
                ip: ....
            },
            instance_id_2: {...},
            ...
        }

        Each instance needs to have a dictionary with the following keys:
            - status: str
            - tags: Dict[str, str]
            - name: str
            - ip: str
        '''
        instances = fc_api.list_instances(self.api_key)  # FILL_IN

        new_cache = {}
        for instance_id, instance in instances.items():
            if instance['status'] != 'running':
                continue
            if any(tag in instance['tags'] for tag in tag_filters):
                new_cache[instance_id] = instance

        self.cached_nodes = new_cache
        return self.cached_nodes

    def _get_node(self, node_id: str):
        '''
        SkyPilot Method
        Returns the node with the given node_id, if it exists.
        '''
        self._get_filtered_nodes({})  # Side effect: updates cache
        return self.cached_nodes.get(node_id, None)

    def _get_cached_node(self, node_id):
        '''
        SkyPilot Method
        Returns the node with the given node_id, if it is cached.
        '''
        if node_id in self.cached_nodes:
            return self.cached_nodes[node_id]
        return self._get_node(node_id=node_id)
