import json
import typing
from typing import Dict, Iterator, List, Optional, Tuple

from sky import clouds
from sky import status_lib
from sky.clouds import service_catalog

if typing.TYPE_CHECKING:
    # Renaming to avoid shadowing variables.
    from sky import resources as resources_lib

import fluffycloud_api as fc_api

_CREDENTIAL_FILES = [
    # credential files for FluffyCloud,
]


@clouds.CLOUD_REGISTRY.register
class FluffyCloud(clouds.Cloud):

    _REPR = 'FluffyCloud'
    _CLOUD_UNSUPPORTED_FEATURES = {
        clouds.CloudImplementationFeatures.STOP: 'FluffyCloud does not support stopping VMs.',
        clouds.CloudImplementationFeatures.AUTOSTOP: 'FluffyCloud does not support stopping VMs.',
        clouds.CloudImplementationFeatures.MULTI_NODE: 'Multi-node is not supported by the FluffyCloud implementation yet.'
    }
    ########
    # TODO #
    ########
    _MAX_CLUSTER_NAME_LEN_LIMIT =  # TODO

    _regions: List[clouds.Region] = []

    @classmethod
    def _cloud_unsupported_features(
            cls) -> Dict[clouds.CloudImplementationFeatures, str]:
        return cls._CLOUD_UNSUPPORTED_FEATURES

    @classmethod
    def _max_cluster_name_length(cls) -> Optional[int]:
        return cls._MAX_CLUSTER_NAME_LEN_LIMIT

    @classmethod
    def regions(cls) -> List[clouds.Region]:
        if not cls._regions:
            ########
            # TODO #
            ########
            # Add the region from catalog entry
            cls._regions = [
                clouds.Region(...),
            ]
        return cls._regions

    @classmethod
    def regions_with_offering(cls, instance_type: Optional[str],
                              accelerators: Optional[Dict[str, int]],
                              use_spot: bool, region: Optional[str],
                              zone: Optional[str]) -> List[clouds.Region]:
        assert zone is None, 'FluffyCloud does not support zones.'
        del accelerators, zone  # unused
        if use_spot:
            return []
        if instance_type is None:
            # Fall back to default regions
            regions = cls.regions()
        else:
            regions = service_catalog.get_region_zones_for_instance_type(
                instance_type, use_spot, 'fluffycloud')

        if region is not None:
            regions = [r for r in regions if r.name == region]
        return regions

    @classmethod
    def get_vcpus_mem_from_instance_type(
        cls,
        instance_type: str,
    ) -> Tuple[Optional[float], Optional[float]]:
        # FILL_IN: cloudname
        return service_catalog.get_vcpus_mem_from_instance_type(instance_type, clouds='<cloudname>')

    @classmethod
    def zones_provision_loop(
        cls,
        *,
        region: str,
        num_nodes: int,
        instance_type: Optional[str] = None,
        accelerators: Optional[Dict[str, int]] = None,
        use_spot: bool = False,
    ) -> Iterator[None]:
        del num_nodes  # unused
        regions = cls.regions_with_offering(instance_type,
                                            accelerators,
                                            use_spot,
                                            region=region,
                                            zone=None)
        for r in regions:
            assert r.zones is None, r
            yield r.zones

    def instance_type_to_hourly_cost(self,
                                     instance_type: str,
                                     use_spot: bool,
                                     region: Optional[str] = None,
                                     zone: Optional[str] = None) -> float:
        return service_catalog.get_hourly_cost(instance_type,
                                               use_spot=use_spot,
                                               region=region,
                                               zone=zone,
                                               clouds='fluffycloud')

    def accelerators_to_hourly_cost(self,
                                    accelerators: Dict[str, int],
                                    use_spot: bool,
                                    region: Optional[str] = None,
                                    zone: Optional[str] = None) -> float:
        del accelerators, use_spot, region, zone  # unused
        # FILL_IN: If accelerator costs are not included in instance_type cost,
        # return the cost of the accelerators here. If accelerators are
        # included in instance_type cost, return 0.0.
        return 0.0

    def get_egress_cost(self, num_gigabytes: float) -> float:
        ########
        # TODO #
        ########
        # Change if your cloud has egress cost. (You can do this later;
        # `return 0.0` is a good placeholder.)
        return 0.0

    def __repr__(self):
        return 'FluffyCloud'

    def is_same_cloud(self, other: clouds.Cloud) -> bool:
        # Returns true if the two clouds are the same cloud type.
        return isinstance(other, FluffyCloud)

    @classmethod
    def get_default_instance_type(cls, cpus: Optional[str] = None) -> Optional[str]:
        return service_catalog.get_default_instance_type(cpus=cpus, clouds='fluffycloud')

    @classmethod
    def get_accelerators_from_instance_type(
        cls,
        instance_type: str,
    ) -> Optional[Dict[str, int]]:
        return service_catalog.get_accelerators_from_instance_type(
            instance_type, clouds='fluffycloud')

    @classmethod
    def get_vcpus_from_instance_type(
        cls,
        instance_type: str,
    ) -> Optional[float]:
        return service_catalog.get_vcpus_from_instance_type(instance_type,
                                                            clouds='fluffycloud')

    @classmethod
    def get_zone_shell_cmd(cls) -> Optional[str]:
        return None

    def make_deploy_resources_variables(
            self, resources: 'resources_lib.Resources',
            region: Optional['clouds.Region'],
            zones: Optional[List['clouds.Zone']]) -> Dict[str, Optional[str]]:
        del zones
        if region is None:
            region = self._get_default_region()

        r = resources
        acc_dict = self.get_accelerators_from_instance_type(r.instance_type)
        if acc_dict is not None:
            custom_resources = json.dumps(acc_dict, separators=(',', ':'))
        else:
            custom_resources = None

        return {
            'instance_type': resources.instance_type,
            'custom_resources': custom_resources,
            'region': region.name,
        }

    def _get_feasible_launchable_resources(self,
                                           resources: 'resources_lib.Resources'):
        if resources.use_spot:
            return ([], [])
        if resources.instance_type is not None:
            assert resources.is_launchable(), resources
            resources = resources.copy(accelerators=None)
            return ([resources], [])

        def _make(instance_list):
            resource_list = []
            for instance_type in instance_list:
                r = resources.copy(
                    cloud=FluffyCloud(),
                    instance_type=instance_type,
                    ########
                    # TODO #
                    ########
                    # Set to None if don't separately bill / attach
                    # accelerators.
                    accelerators=None,
                    cpus=None,
                )
                resource_list.append(r)
            return resource_list

        # Currently, handle a filter on accelerators only.
        accelerators = resources.accelerators
        if accelerators is None:
            # Return a default instance type
            default_instance_type = FluffyCloud.get_default_instance_type(
                cpus=resources.cpus)
            if default_instance_type is None:
                return ([], [])
            else:
                return (_make([default_instance_type]), [])

        assert len(accelerators) == 1, resources
        acc, acc_count = list(accelerators.items())[0]
        (instance_list, fuzzy_candidate_list
         ) = service_catalog.get_instance_type_for_accelerator(
            acc,
            acc_count,
            use_spot=resources.use_spot,
            cpus=resources.cpus,
            region=resources.region,
            zone=resources.zone,
            clouds='fluffycloud')
        if instance_list is None:
            return ([], fuzzy_candidate_list)
        return (_make(instance_list), fuzzy_candidate_list)

    def check_credentials(self) -> Tuple[bool, Optional[str]]:
        ########
        # TODO #
        ########
        # Verify locally stored credentials are correct.

    def get_credential_file_mounts(self) -> Dict[str, str]:
        ########
        # TODO #
        ########
        # Return dictionary of credential file paths. This may look
        # something like:
        # return {
        #     f'~/.fluffycloud/{filename}': f'~/.fluffycloud/{filename}'
        #     for filename in _CREDENTIAL_FILES
        # }

    def get_current_user_identity(self) -> Optional[str]:
        # NOTE: used for very advanced SkyPilot functionality
        # Can implement later if desired
        return None

    def instance_type_exists(self, instance_type: str) -> bool:
        return service_catalog.instance_type_exists(instance_type, 'fluffycloud')

    def validate_region_zone(self, region: Optional[str], zone: Optional[str]):
        return service_catalog.validate_region_zone(region,
                                                    zone,
                                                    clouds='fluffycloud')

    def accelerator_in_region_or_zone(self,
                                      accelerator: str,
                                      acc_count: int,
                                      region: Optional[str] = None,
                                      zone: Optional[str] = None) -> bool:
        return service_catalog.accelerator_in_region_or_zone(
            accelerator, acc_count, region, zone, 'fluffycloud')

    @classmethod
    def query_status(cls, name: str, tag_filters: Dict[str, str],
                     region: Optional[str], zone: Optional[str],
                     **kwargs) -> List[status_lib.ClusterStatus]:
        del tag_filters, region, zone, kwargs  # Unused.

        # FILL_IN: For the status map, map the FluffyCloud status to the SkyPilot status.
        # SkyPilot status is defined in sky/status_lib.py
        # Example: status_map = {'CREATING': status_lib.ClusterStatus.INIT, ...}
        # The keys are the FluffyCloud status, and the values are the SkyPilot status.
        status_map = {
            'CREATING': status_lib.ClusterStatus.INIT,
            'EDITING': status_lib.ClusterStatus.INIT,
            'RUNNING': status_lib.ClusterStatus.UP,
            'STARTING': status_lib.ClusterStatus.INIT,
            'RESTARTING': status_lib.ClusterStatus.INIT,
            'STOPPING': status_lib.ClusterStatus.STOPPED,
            'STOPPED': status_lib.ClusterStatus.STOPPED,
            'TERMINATING': None,
            'TERMINATED': None,
        }
        status_list = []
        vms = fc_api.list_instances()
        for node in vms:
            if node['name'] == name:
                node_status = status_map[node['status']]
                if node_status is not None:
                    status_list.append(node_status)
        return status_list
