"""Utility module to work with JSON"""
import json
import uuid


# SMB2 saves GUIDs in blob form, which Python makes bytes
# Convert it to UUID form to save to file
# then check if the type is guid coming back.
class BytesEncoder(json.JSONEncoder):
    """Encodes GUIDs as JSON objects to make them easily retrievable

    Functions:
    default - called by the json module to encode objects
    """

    def default(self, obj):
        if isinstance(obj, bytes):
            return {
                "_type": "guid",
                "value": uuid.UUID(bytes=obj).hex
            }
        return super(BytesEncoder, self).default(obj)


class BytesDecoder(json.JSONDecoder):
    """Decodes GUIDs back to bytes for the database

    Functions:
    __init__ - Constructor for the class, replaces original object_hook
    object_hook - called by the json module to decode objects
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook,
                                  *args, **kwargs)

    def object_hook(self, obj):
        if '_type' not in obj:
            return obj
        type = obj['_type']
        if type == 'guid':
            return uuid.UUID(obj['value']).bytes
        return obj
