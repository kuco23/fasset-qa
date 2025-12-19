from typing import List
import attrs
from threading import Thread
from qa_lib import DependencyManager
from qa_lib.utils import logger


@attrs.frozen
class LoadTest:
  context: DependencyManager

  def run(self, n: int):
    try:
      logger.info('initializing')
      self.context.simple_user_hive.initialize()
      logger.info('starting threads')
      self.attachThreads(n)
    except Exception as e:
      logger.error('stopping threads due to error', e)
      self.context.simple_user_hive.on_finish()

  def attachThreads(self, n: int):

    threads: List[Thread] = []
    for i in range(n):
      fun = lambda i=i: self.context.simple_user_hive.run_thread(i)
      thread = Thread(target=fun)
      threads.append(thread)

    for thread in threads:
      thread.start()

    for thread in threads:
      thread.join()
