from typing import List
from time import sleep
from datetime import datetime
import attrs
from threading import Thread
from qa_lib import DependencyManager
from qa_lib.utils import logger

CYCLE_FUND_SEC = 60 * 2
CYCLE_FUND_SLEEP_SEC = 10

@attrs.define
class LoadTest:
  context: DependencyManager

  _last_fund = attrs.field(init=False, default=0)

  def run(self, n: int):
    try:
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

    thread = Thread(target=self.funder)
    threads.append(thread)

    for thread in threads:
      thread.start()

    for thread in threads:
      thread.join()

  def funder(self):
    while True:
      try:
        now = datetime.now().timestamp()
        if now - self._last_fund > CYCLE_FUND_SEC:
          self.context.simple_user_hive.fund()
          self._last_fund = now
      except Exception as e:
        logger.error(f'error while funding: {e}')
      sleep(CYCLE_FUND_SLEEP_SEC)
