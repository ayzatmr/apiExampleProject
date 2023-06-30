from enum import IntEnum


class HttpStatus(IntEnum):
    Ok = 200
    Created = 201
    Accepted = 202
    Deleted = 204
    Validation_Error = 400
    Bad_Credentials = 401
    Forbidden = 403
    Not_Found = 404
    Already_Exists = 409
    Too_Many_Requests = 429
