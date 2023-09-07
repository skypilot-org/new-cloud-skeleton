# Node Provider

NodeProvider is the interface that ray uses to interact with cloud providers. First, you should read through the NodeProvider class definition [here](https://github.com/ray-project/ray/blob/master/python/ray/autoscaler/node_provider.py). The docstrings give a good idea of what the NodeProvider class is.

## Implementing a Node Provider

1. Create the directory `sky/skylet/providers/{cloud_name}`
2. Add `__init__.py` to the directory and add the following code:

    ```python
    from sky.skylet.providers.{cloud_name}.node_provider import {CloudName}NodeProvider
    ```

3. Copy the `node_provider.py` template into the directory.
4. Complete the template. The template has comments to guide you through the process.
