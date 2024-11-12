from enum import Enum, unique


@unique
class ErrorEnum(Enum):
    SUCCEEDED = {1: "Operation succeeded"}
    NOT_SUPPORTED = {1001: "Your query statement is currently not supported by the system"}
    INVALID_ID = {2001: "Invalid id"}
    UPDATE_EMPTY = {2002: "The updated attribute is empty"}
    UNKNOWN_ERROR = {9999: "Unknown error."}

    def get_code(self):
        return list(self.value.keys())[0]

    def get_message(self):
        return list(self.value.values())[0]


@unique
class Sex(Enum):
    MALE = "Male"
    FEMALE = "Female"
