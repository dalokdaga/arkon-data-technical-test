import importlib
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from app.api.v1.graphql.wifi_access_schema import Query


schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)

app = FastAPI()
url_module = importlib.import_module("app.api.urls")

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
