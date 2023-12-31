# Cloud E2E Failover

Copy the following functions into sky/backends/cloud_vm_ray_backend.py be sure to update your \<CloudName\>

```python
 def _update_blocklist_on_<cloudname>_error(
            self, launchable_resources: 'resources_lib.Resources',
            region: 'clouds.Region', zones: Optional[List['clouds.Zone']],
            stdout: str, stderr: str):
        del zones  # Unused.
        style = colorama.Style
        stdout_splits = stdout.split('\n')
        stderr_splits = stderr.split('\n')
        errors = [
            s.strip()
            for s in stdout_splits + stderr_splits
            if '<CloudName>Error:' in s.strip()
        ]
        if not errors:
            logger.info('====== stdout ======')
            for s in stdout_splits:
                print(s)
            logger.info('====== stderr ======')
            for s in stderr_splits:
                print(s)
            with ux_utils.print_exception_no_traceback():
                raise RuntimeError('Errors occurred during provision; '
                                   'check logs above.')

        logger.warning(f'Got error(s) in {region.name}:')
        messages = '\n\t'.join(errors)
        logger.warning(f'{style.DIM}\t{messages}{style.RESET_ALL}')
        # NOTE: you can check out other clouds' implementations of this function,
        # which may intelligently block a whole zone / whole region depending on
        # the errors thrown.
        self._blocked_resources.add(launchable_resources.copy(zone=None))
```

Within the `_update_blocklist_on_error` function add your cloud to the handlers dictionary

```python
def _update_blocklist_on_error(
    ...
    handlers = {
        ...
        # TODO Add this
        clouds.FluffyCloud: self._update_blocklist_on_fluffycloud_error,
        ...
    }
    ...
...
```
