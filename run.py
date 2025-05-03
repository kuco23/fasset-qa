from threading import Thread
from qa_lib import Context, AgentCoreVaultHandler, UserCoreVaultRedeemer

if __name__ == '__main__':
  context = Context()
  acvh = AgentCoreVaultHandler(context)
  ucvr = UserCoreVaultRedeemer(context)

  t1 = Thread(target=acvh.run)
  t2 = Thread(target=ucvr.run)

  t1.start()
  t2.start()

  t1.join()
  t2.join()
