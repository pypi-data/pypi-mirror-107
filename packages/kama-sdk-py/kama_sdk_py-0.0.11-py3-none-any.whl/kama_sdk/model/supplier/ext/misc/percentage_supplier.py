from typing import Optional

from werkzeug.utils import cached_property

from kama_sdk.core.core.utils import perr
from kama_sdk.model.supplier.base.supplier import Supplier


class PercentageSupplier(Supplier):

  @cached_property
  def numerator(self) -> Optional[float]:
    return self.get_prop(NUMERATOR_KEY)

  @cached_property
  def denominator(self) -> Optional[float]:
    return self.get_prop(DENOMINATOR_KEY)

  @cached_property
  def rounding(self):
    return self.get_prop(ROUNDING_KEY, 0)

  def fraction(self) -> float:
    explicit = self.get_prop(FRACTION_KEY)
    if explicit is not None:
      return float(explicit)
    else:
      numerator = self.numerator or 0
      denominator = self.denominator or 0
      return numerator / denominator

  def resolve(self) -> float:
    try:
      fraction = self.fraction()
      return round(fraction * 100.0, self.rounding)
    except:
      perr(self, f"failed to make pct", True)
      return 0


NUMERATOR_KEY = 'numerator'
DENOMINATOR_KEY = 'denominator'
FRACTION_KEY = 'fraction'
ROUNDING_KEY = 'rounding'
