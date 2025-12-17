import attrs
from .._dependency_manager import DependencyManager


@attrs.frozen
class LoadTest:
  context: DependencyManager

  def run(self):
    self.context.simple_user_hive.run()