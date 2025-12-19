from typing import Optional
import typer
from qa_lib import DependencyManager
from qa_lib.runners.load_test import LoadTest


app = typer.Typer()
ctx = DependencyManager()

@app.command()
def mint_redeem(user_count: Optional[int] = 0):
  max_user_count = len(ctx.simple_user_bots)
  if user_count == 0:
    user_count = max_user_count
  assert user_count <= max_user_count, f'only {max_user_count} found in config'
  LoadTest(ctx).run(user_count)

@app.command()
def redeem_all():
  raise NotImplemented()