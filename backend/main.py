from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controller.home import router  
from controller.aiforex import predict_ticker

app = FastAPI()

app.mount("/src/css", StaticFiles(directory="/home/null/code/trading/frontend/src/css"), name="css_static")
app.mount("/src/js", StaticFiles(directory="/home/null/code/trading/frontend/src/js"), name="js_static")

app.include_router(router)

app.add_api_route("/predict/{ticker}", predict_ticker, methods=["GET"])