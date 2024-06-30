import uvicorn
from fastapi import FastAPI, Request, Body, Response
import json
import logging
import traceback
import os
import platform
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub

# Initialize the FastAPI app
app = FastAPI()

# Load HUGGINGFACEHUB_API_TOKEN from a .env file
load_dotenv()

# Define the startup event to set up the logging
@app.on_event("startup")
def setup_server():
    # Check if the log file exists, if not, create it
    if not os.path.exists("history.log"):
        try:
            if platform.system() == 'Windows':
                open('history.log', 'w').close()
            else:
                os.mknod('history.log')
        except FileExistsError:
            pass
    # Set up logging to write to the log file
    logging.basicConfig(filename='history.log', level=logging.DEBUG)


# POST endpoint for summarization
@app.post("/summarize")
async def summarize(request: Request, request_data: dict = Body(...)):
    try:
        # Log the incoming request
        logging.info("Got request in /summarize")

        # Get text from the request data
        text = request_data.get("text", "")

        # Creating HuggingFace summarizer with the BART model
        summarizer = HuggingFaceHub(
            repo_id="facebook/bart-large-cnn",
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            model_kwargs={"temperature": 0, "max_length": 180}
        )

        # Generate the summary
        result = summarizer(f"Summarize this: {text}")
        logging.info("Successful summarization")
        # Return the result as a JSON response
        return Response(
            content=json.dumps(result, indent=4, ensure_ascii=False),
            status_code=200,
            media_type="application/json"
        )

    except Exception:
        # Log the error traceback if an exception occurs
        logging.error(traceback.format_exc())
        return Response(
            content=json.dumps({"error": 'Got error in processing'}),
            status_code=400,
            media_type="application/json"
        )


# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
