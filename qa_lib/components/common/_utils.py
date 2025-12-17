from typing import List, Dict
from attrs import frozen
from os.path import exists
from qa_lib.components.params import ParamLoader


@frozen
class CommonUtils:
  params: ParamLoader

  def user_bots_env(self) -> List[Dict[str, str]]:
    ret = []
    i = 0
    while True:
      config = self.params.config.load_test.fasset_user_config_file_path.format(i)
      secrets = self.params.config.load_test.fasset_user_secrets_file_path.format(i)
      if exists(config) and exists(secrets):
        ret.append({
          'FASSET_USER_CONFIG': config,
          'FASSET_USER_SECRETS': secrets
        })
      else:
        break
      i += 1
    return ret

  def uba_to_lots(self, amount: int) -> int:
    return amount // self.params.lot_size

  def uba_to_tokens(self, amount: int) -> float:
    return amount / 10 ** self.params.token_decimals