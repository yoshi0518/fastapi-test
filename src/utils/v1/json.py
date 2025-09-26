import base64
import uuid
from datetime import date, datetime
from decimal import Decimal


def type_serializer(obj):
    """json.dumps() のシリアライズ用フック"""
    # decimal => float
    if isinstance(obj, Decimal):
        return float(obj)
    # datetime、date
    elif isinstance(obj, datetime | date):
        return obj.isoformat()
    # uuid
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    # bytes
    elif isinstance(obj, bytes):
        return base64.b64decode(obj).decode("utf-8")
    raise TypeError
