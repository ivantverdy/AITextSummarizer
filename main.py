import uvicorn
from fastapi import FastAPI, Request, Body, Response
import json
import logging
import traceback
import os
import platform
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub

app = FastAPI()
load_dotenv()


@app.on_event("startup")
def setup_server():
    if not os.path.exists("history.log"):
        try:
            if platform.system() == 'Windows':
                open('history.log', 'w').close()
            else:
                os.mknod('history.log')
        except FileExistsError:
            pass
    logging.basicConfig(filename='history.log', level=logging.DEBUG)


@app.post("/summarize")
async def summarize(request: Request, request_data: dict = Body(...)):
    try:
        logging.info("Got request in /summarize")
        text = request_data.get("text", "")

        summarizer = HuggingFaceHub(
            repo_id="facebook/bart-large-cnn",
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            model_kwargs={"temperature": 0, "max_length": 180}
        )

        result = summarizer(f"Summarize this: {text}")

        return Response(
            content=json.dumps(result, indent=4, ensure_ascii=False),
            status_code=200,
            media_type="application/json"
        )

    except Exception:
        logging.error(traceback.format_exc())
        return Response(
            content=json.dumps({"error": 'Got error in processing'}),
            status_code=400,
            media_type="application/json"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
