from qa_lib import Context

context = Context()


resp = context.database_manager.open_core_vault_transfers('0xC2C745DcEB7041520d8983397A42d4e116BC792C')
print(list(map(lambda x: x.__dict__, resp)))