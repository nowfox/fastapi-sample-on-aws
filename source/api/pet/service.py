from . import schemas
from common import constant
from common.logger_utils import get_logger

logger = get_logger(constant.LOGGER_API)

def __mock_pet() -> schemas.Pet:
    pet = schemas.Pet(
        id=1,
        name="cat",
        )
    return pet



def list() -> list[schemas.Pet]:
    pet = __mock_pet()
    logger.info(pet)
    return [pet]


def get(id: int) -> schemas.Pet:
    pet = __mock_pet()
    return pet
