from typing import List, Optional

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import KoD
from kama_sdk.model.action.base import action
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.base.model import Model
from kama_sdk.model.operation.stage import Stage


class Operation(Model):

  @cached_property
  def stages(self) -> List[Stage]:
    """
    Loads the Stages associated with the Operation.
    :return: list of Stage instances.
    """
    return self.inflate_children(Stage, prop=STAGES_KEY)

  def stage(self, stage_id: str) -> Stage:
    """
    Finds the Stage by key and inflates (instantiates) into a Stage instance.
    :param stage_id: identifier for desired Stage.
    :return: Stage instance.
    """
    matcher = lambda stage: stage.id() == stage_id
    return next(filter(matcher, self.stages), None)

  @cached_property
  def preflight_action_kod(self) -> Optional[KoD]:
    inflated: Action = self.inflate_child(
      Action,
      prop=PREFLIGHT_ACTION_KEY
    )

    return {
      **inflated.serialize(),
      action.TELEM_EVENT_TYPE_KEY: action.PREFLIGHT_EVENT_TYPE
    }


STAGES_KEY = 'stages'
PREFLIGHT_ACTION_KEY = 'preflight_action'
