from datetime import datetime

from kama_sdk.core.core.config_man import config_man
from kama_sdk.core.core.types import ErrCapture
from kama_sdk.core.telem import tabs_man
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.action.base.action_errors import ActionError


class CreateBackupAction(Action):
  def perform(self) -> None:
    if tabs_man.supports_persistence():
      try:
        cmap_contents = config_man.serialize()
        tabs_man.create_backup_record(dict(
          event_type='backup_action',
          data=cmap_contents,
          timestamp=datetime.now()
        ))
      except Exception as e:
        raise ActionError(ErrCapture(
          name='Telem backend failure',
          reason=str(e),
          type='backup_telem_failure'
        ))
