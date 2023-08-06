from typing import Optional, TypeVar, Dict, Any

from werkzeug.utils import cached_property

from kama_sdk.core.core import config_man as cman_module, utils
from kama_sdk.core.core.config_man import config_man, def_vars_key, vndr_inj_vars_key, user_vars_key
from kama_sdk.model.variable.generic_variable import GenericVariable
from kama_sdk.model.variable.variable_category import VariableCategory

T = TypeVar('T', bound='ManifestVariable')


class ManifestVariable(GenericVariable):

  @cached_property
  def owner(self) -> str:
    return self.get_prop(OWNER_KEY, user_owner)

  @cached_property
  def default_value(self) -> str:
    defaults = config_man.default_vars(**{
      cman_module.space_kwarg: self.config_space
    })
    return utils.deep_get2(defaults, self.id())

  @cached_property
  def category(self) -> VariableCategory:
    return self.inflate_child(VariableCategory, prop=CATEGORY_KEY)

  def is_user_writable(self) -> bool:
    return self.owner == user_owner

  def is_user_restricted(self) -> bool:
    return not self.is_user_writable()

  def is_safe_to_set(self) -> bool:
    return self.is_user_writable()

  def current_value(self, **kwargs) -> Optional[str]:
    manifest_variables = config_man.manifest_variables(
      **{
        cman_module.space_kwarg: self.config_space,
        **kwargs
      }
    )
    return utils.deep_get2(manifest_variables, self.id())

  def current_or_default_value(self):
    return self.current_value() or self.default_value

  def is_currently_valid(self) -> bool:
    variables = config_man.manifest_variables(**{
      cman_module.space_kwarg: self.config_space
    })
    is_defined = self.id() in utils.deep2flat(variables).keys()
    crt_val = utils.deep_get2(variables, self.id())
    return self.validate(crt_val)['met'] if is_defined else True

  def sources(self) -> Dict[str, Any]:
    source_types = [user_vars_key, vndr_inj_vars_key, def_vars_key]

    def type2val(key: str) -> Any:
      source: Dict = config_man.read_typed_entry(key, **{
        cman_module.space_kwarg: self.config_space
      })
      return utils.deep_get2(source, self.id())

    return {t: type2val(t) for t in source_types}

  # noinspection PyBroadException
  @classmethod
  def find_or_synthesize(cls, manifest_variable_id) -> T:
    try:
      return cls.inflate(manifest_variable_id)
    except:
      return cls.synthesize_var_model(manifest_variable_id)

  @staticmethod
  def synthesize_var_model(key: str):
    return ManifestVariable.inflate({
      'id': key,
      OWNER_KEY: user_owner,
      'title': f'Undocumented Variable {key}',
      'info': f'Undocumented Variable {key}'
    })


OWNER_KEY = 'owner'
CATEGORY_KEY = 'category'

publisher_owner = 'publisher'
publisher_inj_owner = 'publisher-injection'
user_owner = 'user'
