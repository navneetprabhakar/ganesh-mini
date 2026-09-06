from solution import MachineMonitor

caught = None
try:
    MachineMonitor(10 ** 400, 100, [0, 0, 0])
except Exception as error:
    caught = error
assert isinstance(caught, ValueError), f"out-of-range integer raised {type(caught).__name__}"
