from typing import List, Dict, Any

from flask import Blueprint, jsonify, request

from kama_sdk.controllers import ctrl_utils
from kama_sdk.controllers.ctrl_utils import parse_json_body
from kama_sdk.core.core import job_client, utils
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.ktea.ktea_provider import ktea_client
from kama_sdk.model.action.base import action
from kama_sdk.model.base import model
from kama_sdk.model.variable.manifest_variable import ManifestVariable
from kama_sdk.model.variable.variable_category import VariableCategory
from kama_sdk.serializers import variables_ser

BASE = '/api/variables'

controller = Blueprint('variables_controller', __name__)
no_cat = "uncategorized"
ALL_CATS = 'all_categories'


@controller.route(f"{BASE}/categories")
def get_categories():
  categories: List[VariableCategory] = VariableCategory.inflate_all()
  serialized = list(map(variables_ser.serialize_category, categories))
  return jsonify(data=serialized)


@controller.route(f"{BASE}/all")
def get_all():
  config_man.invalidate_cmap()
  categories = sanitize_cat(request.args.get('category'))
  category_filter = {'category': categories} if categories else {}

  variable_models = ManifestVariable.inflate_all(selector={
    **ctrl_utils.space_selector(False),
    **category_filter
  })

  serialize = lambda v: variables_ser.standard(v, reload=False)
  serialized = list(map(serialize, variable_models))
  return jsonify(data=serialized)


def sanitize_cat(raw_cat: Any) -> List[str]:
  if raw_cat:
    try:
      return str(raw_cat).split(',')
    except:
      return []
  else:
    return []


@controller.route(f"{BASE}/defaults")
def manifest_variables_defaults():
  as_dict = config_man.default_vars()
  return jsonify(data=as_dict)


@controller.route(f'{BASE}/populate-defaults')
def populate_defaults():
  space = ctrl_utils.space_id(True, True)
  defaults = ktea_client(space=space).load_default_values()
  config_man.write_manifest_defaults(defaults, space=space)
  config_man.invalidate_cmap()
  return jsonify(data=defaults)


@controller.route(f'{BASE}/detail/<variable_id>')
def get_variable(variable_id):
  """
  Finds and serializes the chart variable.
  :param variable_id: key used to locate the right chart variable.
  :return: serialized chart variable.
  """
  variable_model = ManifestVariable.find_or_synthesize(variable_id)
  serialized = variables_ser.full(variable_model)
  return jsonify(data=serialized)


@controller.route(f'{BASE}/commit-apply', methods=['POST'])
def commit_and_apply_variable_assignments():
  """
  Updates the chart variable with new value.
  :return: status of the update.
  """
  params: Dict = parse_json_body()
  possibly_flat_assignments = params['assignments']
  assignments = utils.flat2deep(possibly_flat_assignments)

  job_id = job_client.enqueue_action(
    'sdk.action.safely_apply_application_manifest_e2e_action',
    values=assignments,
    **{
      action.TELEM_EVENT_TYPE_KEY: action.SET_VAR_EVENT_TYPE,
      model.CONFIG_SPACE_KEY: ctrl_utils.space_id(True, True)
    }
  )

  return jsonify(data=dict(job_id=job_id))


@controller.route(f'{BASE}/commit-unsets', methods=['POST'])
def commit_and_unset_variable():
  """
  Updates the chart variable with new value.
  :return: status of the update.
  """
  params: Dict = parse_json_body()
  victim_keys = params['victim_keys']

  job_id = job_client.enqueue_action(
    'sdk.action.safely_apply_application_manifest_e2e_action_from_unset',
    victim_keys=victim_keys,
    **{
      action.TELEM_EVENT_TYPE_KEY: action.UNSET_VAR_EVENT_TYPE,
      model.CONFIG_SPACE_KEY: ctrl_utils.space_id(True, True)
    }
  )

  return jsonify(data=dict(job_id=job_id))


@controller.route(f'{BASE}/detail/<variable_id>/validate', methods=['POST'])
def validate_variable_value(variable_id):
  """
  Validates the chart variable against
  :param variable_id: key to locate the right chart variable.
  :return: validation status, with tone and message if unsuccessful.
  """
  value = parse_json_body()['value']
  variable_model = ManifestVariable.find_or_synthesize(variable_id)
  eval_result = variable_model.validate(value)
  status = 'valid' if eval_result['met'] else eval_result['tone']
  message = None if eval_result['met'] else eval_result['reason']
  return jsonify(data=dict(status=status, message=message))


space_id_key = 'space'
