import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

""" hello world app"""


app = FastAPI()


def hello_there():
    return "hello there"


@app.get("/")
async def hello_world(request: Request):
    name = request.query_params.get("name", "World")
    response = {"message": f"Hello {name}!"}
    return JSONResponse(content=response, headers={"Access-Control-Allow-Origin": "*"})


def start():
    print("Hellooooooo!!!")
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


if __name__ == "__main__":
    start()
