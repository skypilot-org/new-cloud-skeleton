# Setup Code

This code is executed after a cluster is launched (via ssh). Most of this code is very similar to the existing setup code for other clouds, and may almost be a copy-paste.

Create a copy of `fluffycloud-ray.yml.js` and place it at `sky/templates/{cloudname-ray.yml.j2`

## Ray Backend

Open `sky/backends/cloud_vm_ray_backend.py` and edit the `_get_cluster_config_template` function to include the new cloud.
