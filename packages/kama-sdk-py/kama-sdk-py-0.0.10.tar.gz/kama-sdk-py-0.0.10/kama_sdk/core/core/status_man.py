from typing import Optional

from kama_sdk.core.core import hub_api_client, kaml_man, consts
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.utils import pwar, perr
from kama_sdk.model.supplier.predicate.predicate import Predicate


def compute_all_statuses():
  statuses = {}
  for space_id in ['app', *kaml_man.kaml_ids()]:
    if computer := space_status_computer(space_id):
      computed_outcome = None
      try:
        computed_outcome = computer.resolve()
      except Exception:
        perr(__name__, f"status comp for space {space_id}", True)
      if computed_outcome is not None:
        status = consts.rng if computed_outcome else consts.brk
        config_man.write_status(status, space=space_id)
        statuses[space_id] = status
      else:
        statuses[space_id] = consts.err
    else:
      pwar(__name__, f"space manager {space_id} has no status computer!")
      statuses[space_id] = consts.err
  return statuses


def space_status_computer(space_id: str) -> Optional[Predicate]:
  kwargs = {'selector': {'space': space_id, 'role': 'status-computer'}}
  return Predicate.inflate_single(**kwargs)


def upload_all_statuses():
  outcomes = {}
  for space in ['app', *kaml_man.registered_kamls_ids()]:
    outcomes[space] = upload_status(space=space)
  return outcomes


def upload_status(**kwargs) -> bool:
  if config_man.is_training_mode():
    return False

  config_man.invalidate_cmap()
  status = config_man.application_status(**kwargs)
  ktea = config_man.read_ktea(**kwargs)
  kama = config_man.read_kama(**kwargs)
  last_updated = config_man.last_updated(**kwargs)

  data = {
    'status': status,
    'ktea_type': ktea.get('type'),
    'ktea_version': ktea.get('version'),
    'kama_type': kama.get('type'),
    'kama_version': kama.get('version'),
    'synced_at': str(last_updated),
  }

  payload = dict(install=data)
  response = hub_api_client.patch('/install', payload, **kwargs)
  print(f"[kama_sdk:telem_man] upload status resp {response}")
  return response.status_code < 205
