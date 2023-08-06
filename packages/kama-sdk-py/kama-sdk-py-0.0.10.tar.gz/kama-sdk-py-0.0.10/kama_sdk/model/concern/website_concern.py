from k8kat.res.svc.kat_svc import KatSvc
from werkzeug.utils import cached_property

from kama_sdk.core.core.types import PortForwardSpec
from kama_sdk.model.concern.concern import Concern
from kama_sdk.model.supplier.ext.misc.port_forward_spec_supplier import PortForwardSpecSupplier


class WebsiteConcern(Concern):
  def svc(self) -> KatSvc:
    return self.get_prop(SVC_KEY)

  def best_url(self) -> str:
    pass



SVC_KEY = 'svc'
PORT_FORWARD_SPEC_KEY = 'port_forward_spec'
