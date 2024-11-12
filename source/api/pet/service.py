import os
import uuid
import boto3
from common import constant
from common.enum import ErrorEnum
from common.exception_handler import BizException
from common.logger_utils import get_logger
from . import schemas

logger = get_logger(constant.LOGGER_API)
dynamodb = boto3.resource("dynamodb")
pet_table = dynamodb.Table(os.getenv("PET_TABLE", "PetSample"))


def create(pet: schemas.PetCreate) -> schemas.Pet:
    item_dict = pet.model_dump(mode="json")
    item_dict["id"] = str(uuid.uuid4())
    pet_table.put_item(Item=item_dict)
    return item_dict


def update(id: str, pet: schemas.PetUpdate) -> schemas.PetUpdate:
    item_dict = pet.model_dump(mode="json", exclude_unset=True)
    if not item_dict:
        raise BizException(ErrorEnum.UPDATE_EMPTY)
    update_expression = "SET " + ", ".join([f"#{k} = :{k}" for k in item_dict.keys()])
    expression_attribute_names = {f"#{k}": k for k in item_dict.keys()}
    expression_attribute_values = {f":{k}": v for k, v in item_dict.items()}
    pet_table.update_item(
        Key={"id": id},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
    )
    return item_dict


def list() -> list[schemas.Pet]:
    response = pet_table.scan()
    items = response["Items"]
    while "LastEvaluatedKey" in response:
        response = pet_table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])
    logger.info(items)
    return items


def get(id: str) -> schemas.Pet:
    response = pet_table.get_item(Key={"id": id})
    logger.info(response)
    if "Item" not in response:
        raise BizException(ErrorEnum.INVALID_ID)
    return response["Item"]


def delete(id: str):
    pet_table.delete_item(Key={"id": id})
