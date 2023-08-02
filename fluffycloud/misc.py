#############################
# Location: `sky/__init__.py`
#############################
...
# Aliases.
...
Local = clouds.Local
# TODO Add this
FluffyCloud = clouds.FluffyCloud
...
__all__ = [
    ...
    # TODO Add this
    'FluffyCloud'
    ...
]

###################################
# Location: `sky/authentication.py`
###################################
...
def setup_fluffycloud_authentication(config: Dict[str, Any]) -> Dict[str, Any]:
    get_or_generate_keys()

    ########
    # TODO #
    ########
    # TODO Ensure sky public key is registered on FluffyCloud
    # If there is an API to add an ssh key to FluffyCloud, it will be
    # useful here. If not, you can tell users to register the key
    # themselves as part of FluffyCloud setup.

    # Need to use ~ relative path because Ray uses the same
    # path for finding the public key path on both local and head node.
    config['auth']['ssh_public_key'] = PUBLIC_SSH_KEY_PATH

    file_mounts = config['file_mounts']
    file_mounts[PUBLIC_SSH_KEY_PATH] = PUBLIC_SSH_KEY_PATH
    config['file_mounts'] = file_mounts

    return config
...

###########################################
# Location: `sky/backends/backend_utils.py`
###########################################
...
def _add_auth_to_cluster_config(cloud: clouds.Cloud, cluster_config_file: str):
    ...
    elif isinstance(cloud, clouds.Azure):
        config = auth.setup_azure_authentication(config)
    # TODO Add this
    elif isinstance(cloud, clouds.FluffyCloud):
        config = auth.setup_fluffycloud_authentication(config)
    ...
...
def _query_status_fluffycloud(
        cluster: str,
        ray_config: Dict[str, Any],
) -> List[global_user_state.ClusterStatus]:
    status_map = {
        ########
        # TODO #
        ########
        # Call list_instances to get the status of the cluster.
        # See _query_status_azure() as a example.
    }
...
_QUERY_STATUS_FUNCS = {
    ...
    # TODO Add this
    'FluffyCloud': _query_status_fluffycloud,
    ...
}
...

####################################
# Location: `sky/clouds/__init__.py`
####################################
...
from sky.clouds.gcp import GCP
# Add this
from sky.clouds.fluffycloud import FluffyCloud
...

__all__ = [
    ...
    # TODO Add this
    'FluffyCloud',
    ...
]
...

####################################################
# Location: `sky/clouds/service_catalog/__init__.py`
####################################################
CloudFilter = Optional[Union[List[str], str]]
_ALL_CLOUDS = ('aws', 'azure', 'gcp', 'fluffycloud' # TODO Add this)

#############################
# Location: `sky/registry.py`
#############################
_CLOUD = [
    ...
    # TODO Add this
    clouds.FluffyCloud()
    ...
]
...

########################################
# Location: `sky/setup_file/MANIFEST.in`
########################################
...
# TODO Add this
include sky/skylet/providers/fluffycloud/*
...
