from typing import Any

from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import KteaDict
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.model.supplier.base.supplier import Supplier
from kama_sdk.core.core import config_man as cman_module


class PresetAssignmentsSupplier(Supplier):

  def ktea(self) -> KteaDict:
    return self.resolve_prop(
      KTEA_KEY,
      depth=100,
      backup=config_man.read_ktea(**{
        cman_module.space_kwarg: self.config_space
      })
    )

  def _compute(self) -> Any:
    ktea_config = self.ktea()
    client_inst = ktea_client(ktea=ktea_config)
    return client_inst.load_preset(self.source_data())


KTEA_KEY = 'ktea'
