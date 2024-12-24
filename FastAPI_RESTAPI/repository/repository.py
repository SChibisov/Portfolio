from typing import List

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from models.models import UserDB, ProductDB, CartDB
from repository.base import get_session


SELECT_ALL_USERS    = text("SELECT * FROM public.users")
SELECT_USER_BY_ID   = text("SELECT * FROM public.users WHERE id=:id")
INSERT_USER         = text("INSERT INTO public.users (login, email, age) VALUES (:login, :email, :age)")
UPDATE_USER         = text("UPDATE public.users SET login=:login, email=:email, age=:age WHERE id=:id")
DELETE_USER         = text("DELETE FROM public.users WHERE id=:id")


SELECT_ALL_PRODUCTS         = text("SELECT * FROM public.products")
SELECT_PRODUCT_BY_ID        = text("SELECT * FROM public.products WHERE id=:id")
INSERT_PRODUCT              = text("""INSERT INTO public.products (product_name, product_cnt, is_available)
                                      VALUES (:product_name, :product_cnt, :is_available)""")
UPDATE_PRODUCT              = text("""UPDATE public.products 
                                      SET product_name=:product_name, 
                                          product_cnt=:product_cnt, 
                                          is_available=:is_available 
                                      WHERE id=:id""")
UPDATE_PRODUCT_COUNT        = text("UPDATE public.products SET product_cnt=:product_cnt,"
                                   " is_available=:is_available WHERE id=:id")
UPDATE_PRODUCT_AVAILABILITY = text("UPDATE public.products SET is_available=:is_available WHERE id=:id")
DELETE_PRODUCT              = text("DELETE FROM public.products WHERE id=:id")


SELECT_CARTS_BY_USER_ID     = text("""SELECT carts.id               AS id, 
                                         carts.user_id          AS user_id, 
                                         carts.product_id       AS product_id, 
                                         products.product_name  AS product_name, 
                                         carts.product_count    AS product_count  
                                   FROM public.carts AS carts
                                   LEFT JOIN public.products products ON carts.product_id = products.id
                                   WHERE user_id=:user_id""")
INSERT_USER_CART            = text("""INSERT INTO public.carts (user_id, product_id, product_count) 
                           VALUES (:user_id, :product_id, :product_count)""")
UPDATE_USER_CART            = text("""UPDATE public.carts 
                           SET user_id=:user_id, product_id=:product_id, product_count=:product_count 
                           WHERE id=:id""")
DELETE_CART                 = text("DELETE FROM public.carts WHERE id=:id")


class UsersRepository:
    @staticmethod
    def get_users() -> List[UserDB]:
        users: List[UserDB] = []
        session = get_session()
        try:
            result_set = session.execute(SELECT_ALL_USERS).mappings().all()
            if len(result_set) != 0:
                for result in result_set:
                    user = UserDB()
                    user.id = result.id
                    user.login = result.login
                    user.email = result.email
                    user.age = result.age

                    users.append(user)
        finally:
            session.close()

        return users

    @staticmethod
    def get_user_by_id(user_id: int) -> UserDB:
        user: UserDB = None
        session = get_session()
        try:
            result_set = session.execute(SELECT_USER_BY_ID, {"id": user_id}).fetchone()
            if result_set is not None:
                user = UserDB()
                user.id = result_set.id
                user.login = result_set.login
                user.email = result_set.email
                user.age = result_set.age

        finally:
            session.close()

        return user

    @staticmethod
    def create_user(user: UserDB) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "login": user.login,
                "email": user.email,
                "age": user.age
            }
            session.execute(INSERT_USER, query_parameters)
            session.commit()

        except SQLAlchemyError:
            return False
        finally:
            session.close()

        return True

    @staticmethod
    def update_user(user_id: int, login: str, email: str, age: int) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "id": user_id,
                "login": login,
                "email": email,
                "age": age
            }
            session.execute(UPDATE_USER, query_parameters)
            session.commit()

        except SQLAlchemyError:
            return False
        finally:
            session.close()

        return True

    @staticmethod
    def delete_user(user_id: int) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "id": user_id
            }
            session.execute(DELETE_USER, query_parameters)
            session.commit()
        except SQLAlchemyError:
            return False
        finally:
            session.close()

        return True


class ProductsRepository:
    @staticmethod
    def get_products() -> List[ProductDB]:
        products: List[ProductDB] = []

        session = get_session()
        try:
            result_set = session.execute(SELECT_ALL_PRODUCTS)
            for result in result_set:
                product = ProductDB()
                product.id = result.id
                product.product_name = result.product_name
                product.product_cnt = result.product_cnt
                product.is_available = result.is_available
                products.append(product)

        finally:
            session.close()

        return products

    @staticmethod
    def get_product(product_id: int) -> ProductDB:
        product = None

        session = get_session()
        try:
            query_parameters = {"id": product_id}
            result_set = session.execute(SELECT_PRODUCT_BY_ID, query_parameters).fetchone()

            if result_set is not None:
                product = ProductDB()
                product.id = result_set.id
                product.product_name = result_set.product_name
                product.product_cnt = result_set.product_cnt
                product.is_available = result_set.is_available

        finally:
            session.close()

        return product

    @staticmethod
    def create_product(product: ProductDB) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "product_name": product.product_name,
                "product_cnt": product.product_cnt,
                "is_available": product.product_cnt != 0
            }
            session.execute(INSERT_PRODUCT, query_parameters)
            session.commit()

        except SQLAlchemyError:
            return False
        finally:
            session.close()

        return True

    @staticmethod
    def update_product_count(product_id: int, count: int) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "id": product_id,
                "product_cnt": count,
                "is_available": count > 0
            }
            session.execute(UPDATE_PRODUCT_COUNT, query_parameters)
            session.commit()

        except SQLAlchemyError:
            return False
        finally:
            session.close()

        return True

    @staticmethod
    def update_product_availability(product_id: int, availability: bool) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "id": product_id,
                "is_available": availability
            }
            session.execute(UPDATE_PRODUCT_AVAILABILITY, query_parameters)
            session.commit()

        except SQLAlchemyError:
            return False
        finally:
            session.close()

        return True

    @staticmethod
    def update_product(product_id: int, product_name: str, product_cnt: int, is_available: bool) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "id": product_id,
                "product_name": product_name,
                "product_cnt": product_cnt,
                "is_available": is_available
            }
            session.execute(UPDATE_PRODUCT, query_parameters)
            session.commit()

        except SQLAlchemyError:
            return False
        finally:
            session.close()

        return True

    @staticmethod
    def delete_product(product_id: int) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "id": product_id
            }
            session.execute(DELETE_PRODUCT, query_parameters)
            session.commit()

        except SQLAlchemyError:
            return False
        finally:
            session.close()


class CartRepository:
    @staticmethod
    def get_cart_by_user_id(user_id: int) -> List[CartDB]:
        user_carts: List[CartDB] = []

        session = get_session()
        try:
            query_parameters = {"user_id": user_id}
            result_set = session.execute(SELECT_CARTS_BY_USER_ID, query_parameters)

            for result in result_set:
                cart: CartDB = CartDB()
                cart.id = result.id
                cart.user_id = result.user_id
                cart.product_id = result.product_id
                cart.product_name = result.product_name
                cart.product_count = result.product_count

                user_carts.append(cart)

        finally:
            session.close()

        return user_carts

    @staticmethod
    def create_cart(cart: CartDB) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "user_id": cart.user_id,
                "product_id": cart.product_id,
                "product_count": cart.product_count,
            }
            session.execute(INSERT_USER_CART, query_parameters)
            session.commit()

        except SQLAlchemyError:
            return False
        finally:
            session.close()

        return True

    @staticmethod
    def update_cart(cart: CartDB) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "id": cart.id,
                "user_id": cart.user_id,
                "product_id": cart.product_id,
                "product_count": cart.product_count,
            }
            session.execute(UPDATE_USER_CART, query_parameters)
            session.commit()

        except SQLAlchemyError:
            return False
        finally:
            session.close()

        return True

    @staticmethod
    def delete_cart(cart_id: int) -> bool:
        session = get_session()
        try:
            query_parameters = {
                "id": cart_id
            }
            session.execute(DELETE_CART, query_parameters)
            session.commit()

        except SQLAlchemyError:
            return False
        finally:
            session.close()

        return True
