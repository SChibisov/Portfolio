from typing import List
from fastapi import APIRouter, Path, HTTPException, status
from models.models import User, Product, Cart, UserDB, ProductDB, CartDB, CartPayload
from repository.repository import UsersRepository, CartRepository, ProductsRepository

user_router = APIRouter()
product_router = APIRouter()
cart_router = APIRouter()


def to_user_db(user: User) -> UserDB:
    db_user = UserDB()
    db_user.id = user.id
    db_user.login = user.login
    db_user.email = user.email
    db_user.age = user.age
    return db_user


def to_user(db_user: UserDB) -> User:
    return User.parse_obj(db_user.__dict__())


def to_product_db(product: Product) -> ProductDB:
    db_product = ProductDB()
    db_product.id = product.id
    db_product.product_name = product.product_name
    db_product.product_cnt = product.product_cnt
    db_product.is_available = product.is_available
    return db_product


def to_product(db_product: ProductDB) -> Product:
    return Product.parse_obj(db_product.__dict__())


def to_cart_db(cart: Cart) -> CartDB:
    db_cart = CartDB()
    db_cart.id = cart.id
    db_cart.user_id = cart.user_id
    db_cart.product_name = cart.product_name
    db_cart.product_count = cart.product_count
    db_cart.product_id = cart.product_id
    return db_cart


def to_cart(db_cart: CartDB) -> Cart:
    return Cart.parse_obj(db_cart.__dict__())


# Users routing

@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(user: User):
    """Создание нового пользователя"""
    existing_user = UsersRepository.get_user_by_id(user.id)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with ID {user.id} already exists")
    db_user = to_user_db(user)
    created_user = UsersRepository.create_user(db_user)
    return created_user


@user_router.get("/", response_model=List[User])
async def retrieve_users():
    """Возвращает список всех пользователей"""
    db_users = UsersRepository.get_users()
    users = []
    for u in db_users:
        user = User.parse_obj(u.__dict__())
        users.append(user)
    return users


@user_router.get("/{user_id}", response_model=User)
async def get_single_user(user_id: int):
    """Возвращает информацию о пользователе по ID"""
    db_user = UsersRepository.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} does not exist")
    return to_user(db_user)


@user_router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    """Обновление информации о пользователе по ID"""
    existing_user = UsersRepository.get_user_by_id(user_id)

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} does not exist")

    result = UsersRepository.update_user(user_id, user.login, user.email, user.age)
    return result


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_user(user_id: int):
    """Удаление пользователя по ID"""
    result = UsersRepository.delete_user(user_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} does not exist")


# Products routing

@product_router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def add_product(product: Product):
    """Создает новый продукт"""
    db_product = to_product_db(product)
    result = ProductsRepository.create_product(db_product)
    return result


@product_router.get("/", response_model=List[Product])
async def retrieve_products():
    """Возвращает список всех продуктов"""
    db_products = ProductsRepository.get_products()
    products = []
    for p in db_products:
        products.append(to_product(p))
    return products


@product_router.get("/{product_id}", response_model=Product)
async def get_single_product(product_id: int):
    """Возвращает продукт по ID"""
    db_product = ProductsRepository.get_product(product_id)

    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with ID {product_id} does not exist")

    return to_product(db_product)


@product_router.put("/{product_id}", response_model=Product)
async def update_product(product_id: int, product_data: Product):
    """Обновляет данные существующего продукта"""
    existing_product = ProductsRepository.get_product(product_id)

    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with ID {product_id} does not exist")

    result = ProductsRepository.update_product(product_id, product_data.product_name, product_data.product_cnt,
                                               product_data.is_available)
    return result


@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_product(product_id: int):
    """Удаляет продукт по ID"""
    result = ProductsRepository.delete_product(product_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with ID {product_id} does not exist")


# Cart routing


def _cart_from(user_id: int, product_id: int, product_count: int) -> CartDB:
    """Это вспомогательная функция для создания объекта корзины"""
    db_cart = CartDB()
    db_cart.user_id = user_id
    db_cart.product_id = product_id
    db_cart.product_count = product_count
    return db_cart


@cart_router.get("/{user_id}", response_model=List[Cart])
async def get_cart_by_user(user_id: int):
    """Получение всех товаров в корзине для данного пользователя"""
    db_carts = CartRepository.get_cart_by_user_id(user_id)

    if len(db_carts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No carts found for user with ID {user_id}")
    carts = []
    for c in db_carts:
        carts.append(to_cart(c))
    return carts


@cart_router.put("/{user_id}", response_model=dict)
async def update_cart(user_id: int, cart_item: CartPayload):
    """Обновление корзины с добавлением товара"""
    user = UsersRepository.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} does not exist")

    # Получаем продукты из репозитория
    product = ProductsRepository.get_product(cart_item.product_id)

    if not product or not product.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not available or does not exist")

    # Проверяем доступное количество
    if product.product_cnt < cart_item.product_count:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough product available")

    # Обновляем количество товаров
    ProductsRepository.update_product_count(cart_item.product_id, product.product_cnt - cart_item.product_count)

    if product.product_cnt == 0:
        ProductsRepository.update_product_availability(cart_item.product_id, False)

    current_cart = _cart_from(user_id, cart_item.product_id, cart_item.product_count)
    CartRepository.create_cart(current_cart)

    return {"message": f"Cart for user with ID {user_id} updated successfully"}


@cart_router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_cart(cart_id: int):
    """Удаление товара из корзины"""
    result = CartRepository.delete_cart(cart_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cart with ID {cart_id} does not exist")
