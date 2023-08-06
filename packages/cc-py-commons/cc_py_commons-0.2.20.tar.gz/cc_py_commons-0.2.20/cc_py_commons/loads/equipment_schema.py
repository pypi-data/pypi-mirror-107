from marshmallow import fields, EXCLUDE
from cc_py_commons.schemas.camel_case_schema import CamelCaseSchema

class EquipmentSchema(CamelCaseSchema):
  class Meta:
      unknown = EXCLUDE
  
  id = fields.UUID()
  name = fields.String()