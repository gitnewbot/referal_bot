#! venv/bin/python3

from common import engine
from common.models import Base

Base.metadata.create_all(engine)

print('complete')