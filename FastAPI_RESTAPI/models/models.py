from pydantic import BaseModel


class User(BaseModel):
    id: int
    login: str
    email: str
    age: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "login": "User",
                    "email": "user@email.com",
                    "age": 20
                }
            ]
        }
    }


class Product(BaseModel):
    id: int
    product_name: str
    product_cnt: int
    is_available: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "product_name": "Table",
                    "product_cnt": 10,
                    "is_available": True
                }
            ]
        }
    }


class Cart(BaseModel):
    id: int
    user_id: int
    product_id: int
    product_count: int
    product_name: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 2,
                    "product_id": 1,
                    "product_name": "Table",
                    "product_count": 20
                }
            ]
        }
    }


class CartPayload(BaseModel):

    product_id: int
    product_count: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "product_id": 1,
                    "product_count": 20
                }
            ]
        }
    }


class UserDB:
    id: int
    login: str
    email: str
    age: int

    def __dict__(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'age': self.age
        }


class ProductDB:
    id: int
    product_name: str
    product_cnt: int
    is_available: bool = True

    def __dict__(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'product_cnt': self.product_cnt,
            'is_available': self.is_available
        }


class CartDB:
    id: int
    user_id: int
    product_id: int
    product_name: str
    product_count: int

    def __dict__(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_count': self.product_count
        }
