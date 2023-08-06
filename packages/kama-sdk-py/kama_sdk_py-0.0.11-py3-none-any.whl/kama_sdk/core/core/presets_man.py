from typing import List, Optional, Dict

from kama_sdk.core.core import utils, job_client
from kama_sdk.core.core.config_man import config_man
from kama_sdk.model.action.base import action
from kama_sdk.model.supplier.base.provider import Provider
from kama_sdk.model.supplier.base.supplier import Supplier
from kama_sdk.model.variable.manifest_variable import ManifestVariable


def ser_preset(provider: Provider, var_models: List[ManifestVariable]):
  assignments = provider.resolve()
  flat_assigns = utils.deep2flat(assignments)

  def find_var(key: str) -> Optional[ManifestVariable]:
    disc = lambda model: model.id() == key
    return next(filter(disc, var_models), None)

  var_bundles = []
  for k, v in flat_assigns.items():
    var_model = find_var(k)
    var_bundles.append(dict(
      id=k,
      info=var_model.info if var_model else None,
      new_value=v,
      old_value=var_model.current_value(reload=False) if var_model else None
    ))

  return dict(
    id=provider.id(),
    title=provider.title,
    info=provider.info,
    variables=var_bundles,
    is_complete=provider.resolve_prop('is_complete', lookback=False),
    is_default=provider.resolve_prop('is_default', lookback=False)
  )


def load_all(space_id: str):
  config_man.invalidate_cmap()
  selector = dict(type='preset', space=space_id)
  presets = Supplier.inflate_all(selector=selector)
  var_models = ManifestVariable.inflate_all(selector=dict(space=space_id))
  return [ser_preset(p, var_models) for p in presets]


def load_and_start_apply_job(preset_id: str, space_id: str, whitelist: List[str]):
  config_man.invalidate_cmap()
  selector = dict(type='preset', space=space_id)
  supplier = Supplier.inflate(preset_id, selector=selector)

  if supplier.resolve_prop('is_default', lookback=0):
    assignments = {}
  else:
    all_flat_assigns: Dict = utils.deep2flat(supplier.resolve())
    flat_assigns = {k: v for k, v in all_flat_assigns.items() if k in whitelist}
    assignments = utils.flat2deep(flat_assigns)

  return job_client.enqueue_action(
    'sdk.action.safely_apply_application_manifest_e2e_action',
    values=assignments,
    **{action.TELEM_EVENT_TYPE_KEY: action.SET_VAR_EVENT_TYPE}
  )
