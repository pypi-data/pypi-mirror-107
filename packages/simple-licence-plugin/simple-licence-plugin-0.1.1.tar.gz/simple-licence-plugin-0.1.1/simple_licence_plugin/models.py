""" models used during the licence plugin calls """

from typing import List
from pydantic import BaseModel


class AuditEventBase(BaseModel):
    """
    Base Model to use for the Audit Event received from
    `_call_home()` in simple_licence_plugin.utils.

    An example where we also inherit `DocumentDBTimeStampedModel` which
    provides the functionality for writing to our database.

    .. code-block:: python

        class AuditEvent(AuditEventBase):
            @classmethod
            def get_db_collection(cls) -> str:
                return f"{dm_settings.COLLECTION_PREFIX}auditevents"


        event = AuditEvent()
        event.save()
    """

    product: str = ""
    product_version: str = ""
    licensee: str = ""
    licence_issued: str = ""
    expiry: str = ""
    audit_url: str = ""
    features: List[str] = []
    container_id: str = ""
    username: str = ""
    node: str = ""
    python_version: str = ""
    platform: str = ""
    distro: str = ""
