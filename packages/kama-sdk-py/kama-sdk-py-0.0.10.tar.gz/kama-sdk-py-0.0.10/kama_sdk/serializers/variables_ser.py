from typing import Dict

from kama_sdk.model.input import input_serializer
from kama_sdk.model.variable.manifest_variable import ManifestVariable
from kama_sdk.model.variable.variable_category import VariableCategory
from kama_sdk.serializers import common_serializers


def serialize_category(category: VariableCategory) -> Dict:
  return {
    **common_serializers.ser_meta(category),
    'graphic_type': category.graphic_type,
    'graphic': category.graphic
  }


def standard(cv: ManifestVariable, **kwargs):
  return dict(
    id=cv.id(),
    title=cv.title,
    is_user_writable=cv.is_user_writable(),
    info=cv.info,
    value=cv.current_value(**kwargs),
    sources=cv.sources(),
    is_valid=cv.is_currently_valid(),
    config_space=cv.config_space
  )


def full(cv: ManifestVariable):
  """
  Extended serializer for the ChartVariable instance, which also includes includes
  details about the associated field.
  :param cv: ChartVariable class instance.
  :return: extended serialized ChartVariable object (dict).
  """
  return dict(
    **standard(cv),
    **input_serializer.in_variable(cv.input_model)
  )
