from solution import WorkflowCatalog

catalog = WorkflowCatalog()
for index in range(1200):
    catalog.add(str(index), lambda: None, [str(index - 1)] if index else [])
caught = None
try:
    result = catalog.run("1199")
except Exception as error:
    caught = error
assert caught is None, f"valid acyclic workflow raised {type(caught).__name__}"
assert len(result) == 1200
