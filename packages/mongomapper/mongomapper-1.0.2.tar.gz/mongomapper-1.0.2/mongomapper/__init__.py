from bson.objectid import ObjectId
from bson.codec_options import TypeRegistry, CodecOptions

from .utils import classproperty

from .base import BaseSchema, db
from .reference import Reference
from .query import Query

from .encoders import DateEncoder

type_registry = TypeRegistry([DateEncoder()])

class Schema(BaseSchema):
  @classproperty
  def collection(cls):
    return db.get_collection(cls.__collection_name__, codec_options=CodecOptions(type_registry=type_registry))

  @property
  def reference(self):
    return Reference(self.__class__)(self._id)
  
  @classproperty
  def query(self):
    return Query(model=self)
  
  class Config:
    json_encoders = {
      ObjectId: lambda oid: str(oid),
      Reference: lambda ref: str(ref)
    }