import os
import sys
import importlib
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))


task_module = importlib.import_module("app.core.common.commands.tasks.process_data")
