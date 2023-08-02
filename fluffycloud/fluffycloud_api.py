def launch(name:str,
           instance_type:str,
           region:str,
           api_key:str,
           ssh_key_name:str):
    """Launches an INSTANCE_TYPE instance in region REGION with given NAME.
    
    API_KEY is a secret registered with FluffyCloud. It is per-user.
    
    SSH_KEY_NAME corresponds to a ssh key registered with FluffyCloud.
    After launching, the user can ssh into INSTANCE_TYPE with that ssh key.
    
    Returns INSTANCE_ID if successful, otherwise returns None.
    """

def remove(instance_id:str, api_key:str):
    """Removes instance with given INSTANCE_ID."""
    
def set_tags(instance_id:str, tags:Dict, api_key:str)
    """Set tags for instance with given INSTANCE_ID."""
   
def list_instances(api_key:str):
    """Lists instances associated with API_KEY.
    
    Returns a dictionary:
    {
        instance_id_1:
        {
            status: ...,
            tags: ...,
            name: ...,
            ip: ....
        },
        instance_id_2: {...},
        ...
    }
    """
