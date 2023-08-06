import json
from typing import Dict

from flask import request

from kama_sdk.core.core import utils
from kama_sdk.model.base import model


def parse_json_body() -> Dict:
  if utils.is_in_cluster():
    payload_str = request.data.decode('unicode-escape')
    truncated = payload_str[1:len(payload_str) - 1]
    as_dict = json.loads(truncated)
    return utils.unmuck_primitives(as_dict)
  else:
    return utils.unmuck_primitives(request.json)


def space_id(force_single: bool, bkp_is_app=False):
  if value := request.args.get('space'):
    csv = list(map(str.strip, value.split(",")))
    return csv[0] if force_single else csv
  else:
    return 'app' if bkp_is_app else None


def space_selector(force_single):
  if space_or_spaces := space_id(force_single):
    return {model.SPACE_LABEL: space_or_spaces}
  else:
    return {}


def selector_kwargs(force_single: bool) -> Dict:
  if space_sel := space_selector(force_single):
    return {model.selector_kwarg: space_sel}
  else:
    return {}
