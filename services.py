import model
from repository import AbstractRepository

class InvalidSku(Exception):
    pass

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(line: model.OrderLine, repo: AbstractRepository, session):
    if not is_valid_sku(line.sku, repo.list()):
        raise InvalidSku(f"Invalid sku {line.sku}")
    
    batchref = model.allocate(line, repo.list())
    session.commit()
    return batchref