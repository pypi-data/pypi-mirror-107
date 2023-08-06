from datetime import datetime

from flask import Blueprint, jsonify

from kama_sdk.controllers.ctrl_utils import parse_json_body
from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.telem import tabs_man
from kama_sdk.serializers import telem_serializers

controller = Blueprint('telem_controller', __name__)

BASE = '/api/telem'


@controller.route(f'{BASE}/prefs')
def prefs_show():
  return jsonify(ping='pong')


@controller.route(f'{BASE}/prefs', methods=['PATCH'])
def prefs_patch():
  return jsonify(ping='pong')


@controller.route(f'{BASE}/config_backups/new', methods=['POST'])
def new_config_backup():
  attrs = parse_json_body()
  config_backup = dict(
    name=attrs.get('name') or 'none',
    event_type='client_triggered',
    data=config_man.serialize(),
    timestamp=datetime.now()
  )

  if result := tabs_man.create_backup_record(config_backup):
    return jsonify(id=str(result.get('_id')), record=config_backup)
  else:
    return jsonify(error='failed to create'), 400


@controller.route(f'{BASE}/events')
def list_events():
  return jsonify(data=tabs_man.list_events())


@controller.route(f'{BASE}/config_backups/<config_id>')
def get_config_backups(config_id: str):
  if record := tabs_man.get_config_backup(config_id):
    serialized = telem_serializers.ser_config_backup_full(record)
    return jsonify(data=serialized)
  else:
    return jsonify(error='dne'), 404


# @controller.route(f'{BASE}/config_backups/<config_id>', methods=['DELETE'])
# def delete_config_backups(config_id: str):
#   if record := telem_man.get_config_backup(config_id):
#     serialized = telem_serializers.ser_config_backup_full(record)
#     return jsonify(data=serialized)
#   else:
#     return jsonify(error='dne'), 404


@controller.route(f'{BASE}/config_backups')
def config_backups_index():
  records = tabs_man.list_config_backups()
  serializer = telem_serializers.ser_config_backup
  return jsonify(data=list(map(serializer, records)))
