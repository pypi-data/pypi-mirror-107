from typing import Optional

from flask import Blueprint, jsonify

from kama_sdk.controllers import ctrl_utils
from kama_sdk.core.core import job_client
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.base import model
from kama_sdk.serializers import action_serializer

controller = Blueprint('actions', __name__)

BASE_PATH = '/api/actions'

@controller.route(f"{BASE_PATH}/types/<_type>")
def list_actions_in_type(_type):
  selector = {'type': _type, **ctrl_utils.space_selector(False)}
  models = Action.inflate_all(**{model.selector_kwarg: selector})
  serializer = action_serializer.serialize_std
  serialized = list(map(serializer, models))
  return dict(data=serialized)


@controller.route(f"{BASE_PATH}/<_id>")
def get_action(_id: str):
  if action := find_action(_id):
    serialized = action_serializer.serialize_std(action)
    return jsonify(data=serialized)
  else:
    return jsonify(error=f"action not found for id='{_id}'"), 404


@controller.route(f"{BASE_PATH}/<_id>/run", methods=['POST'])
def run_action(_id: str):
  if action := find_action(_id):
    job_id = job_client.enqueue_action(action.id())
    return jsonify(status='running', job_id=job_id)
  else:
    return jsonify(error=f"test not found for id='{_id}'"), 404


def find_action(_id: str) -> Optional[Action]:
  return Action.inflate(_id, **ctrl_utils.selector_kwargs(False))
