from typing import Optional

from k8kat.res.svc.kat_svc import KatSvc
from werkzeug.utils import cached_property

from kama_sdk.core.core.types import EndpointDict
from kama_sdk.model.supplier.base.supplier import Supplier


class BestSvcUrlSupplier(Supplier):

  @cached_property
  def svc(self) -> KatSvc:
    return self.source_data()

  def _compute(self) -> Optional[EndpointDict]:
    if ingress_val := self.ingress_addr():
      return {'url': ingress_val, 'type': 'ingress'}
    else:
      port_part = f":{self.port}" if self.port else ''
      available_ip = self.svc.external_ip or self.svc.internal_ip
      url = f"{available_ip}{port_part}"
      return {'url': url, 'type': self.svc.type}

  @cached_property
  def port(self) -> Optional[str]:
    return self.get_prop(PORT_KEY) or self.infer_port()

  def infer_url(self) -> Optional[str]:
    return self.svc.external_ip or \
           self.svc.internal_ip

  def infer_port(self) -> str:
    value = str(self.svc.first_tcp_port_num())
    return value if not value == '80' else ''

  def ingress_addr(self) -> Optional[str]:
    return None


PORT_KEY = 'port'
