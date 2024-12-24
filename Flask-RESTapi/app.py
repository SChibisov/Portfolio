from flask import Flask
from flask_restful import Api

from routers.users_router import UserRouter, UsersRouter
from routers.products_router import ProductRouter, ProductsRouter
from routers.carts_router import CartRouter


app = Flask(__name__)
api = Api(app)


API_PREFIX = '/api/v1'

api.add_resource(UserRouter,        API_PREFIX + '/users/<int:user_id>')
api.add_resource(UsersRouter,       API_PREFIX + '/users')
api.add_resource(ProductRouter,     API_PREFIX + '/products/<int:product_id>')
api.add_resource(ProductsRouter,    API_PREFIX + '/products')
api.add_resource(CartRouter,        API_PREFIX + '/carts/<int:user_id>')


if __name__ == '__main__':
    app.run(debug=True)
