from . import schemas

def __mock_pet() -> schemas.Pet:
    pet = schemas.Pet(
        id=1,
        name="cat",
        )
    return pet



def list() -> list[schemas.Pet]:
    pet = __mock_pet()
    return [pet]


def get(id: int) -> schemas.Pet:
    pet = __mock_pet()
    return pet
