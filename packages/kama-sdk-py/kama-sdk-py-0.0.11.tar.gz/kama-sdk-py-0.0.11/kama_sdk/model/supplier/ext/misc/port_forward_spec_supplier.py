from typing import Optional

from k8kat.res.svc.kat_svc import KatSvc
from kubernetes.client import V1EndpointAddress, V1ObjectReference
from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.core.core.types import PortForwardSpec
from kama_sdk.model.supplier.base.supplier import Supplier


class PortForwardSpecSupplier(Supplier):

  def source_data(self) -> Optional[KatSvc]:
    return super(PortForwardSpecSupplier, self).source_data()

  @cached_property
  def expl_port(self):
    return self.get_prop(PORT_KEY)

  def _compute(self) -> Optional[PortForwardSpec]:
    svc = self.source_data()
    winner = None
    backend_dicts = svc.flat_endpoints() or []
    for backend_dict in utils.compact(backend_dicts):
      address: V1EndpointAddress = backend_dict
      target_ref: V1ObjectReference = address.target_ref
      if target_ref and target_ref.kind == 'Pod':
        winner = target_ref
        break

    if winner:
      return PortForwardSpec(
        namespace=winner.namespace,
        pod_name=winner.name,
        pod_port=int(self.expl_port or svc.first_tcp_port_num() or '80')
      )


PORT_KEY = 'port'
