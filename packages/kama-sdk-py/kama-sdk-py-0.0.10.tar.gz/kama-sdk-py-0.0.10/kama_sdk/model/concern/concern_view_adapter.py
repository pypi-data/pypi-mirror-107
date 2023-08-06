from typing import TypeVar

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import Reconstructor
from kama_sdk.core.core.utils import perr
from kama_sdk.model.base.model import Model
from kama_sdk.model.concern.concern import Concern
from kama_sdk.model.concern import concern as concern_module

T = TypeVar('T', bound='ConcernViewAdapter')


class ConcernViewAdapter(Model):

  @cached_property
  def concern_shell(self) -> Concern:
    return self.inflate_child(
      Concern,
      prop=CONCERN_SHELL_KEY,
      safely=True
    )

  @classmethod
  def reconstruct(cls, reconstructor: Reconstructor):
    adapter: T = cls.inflate(reconstructor['adapter_ref'])

    if concern_shell_ref := reconstructor.get('concern_ref'):
      concern: Concern = Concern.inflate(concern_shell_ref)
    else:
      concern = adapter.concern_shell

    if not concern:
      sig = f"{adapter.kind()}/{adapter.id()}"
      perr(cls, f"danger no concern for adapter {sig}", False)

    if seed := reconstructor.get('seed'):
      concern.patch({concern_module.SEED_KEY: seed})

    return adapter.patch({'concern': concern})


CONCERN_SHELL_KEY = 'concern_shell'
