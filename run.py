""" from threading import Thread
from qa_lib import DependencyManager, AgentCoreVaultHandler, UserCoreVaultRedeemer

if __name__ == '__main__':
  context = DependencyManager()
  acvh = AgentCoreVaultHandler(context)
  ucvr = UserCoreVaultRedeemer(context)

  t1 = Thread(target=acvh.run)
  t2 = Thread(target=ucvr.run)

  t1.start()
  t2.start()

  t1.join()
  t2.join()
 """

from qa_lib.runners.load_test import LoadTest
from qa_lib import DependencyManager

context = DependencyManager()
LoadTest(context).run()