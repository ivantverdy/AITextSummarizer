# FastAPI Summarization Service

This is a FastAPI application that provides a summarization service using Hugging Face's BART model.

## Setup Instructions

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/ivantverdy/testAIPickles.git
    cd testAIPickles
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```sh
        source venv/bin/activate
        ```

4. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

5. Create a `.env` file in the root directory and add your Hugging Face API token (Type of the token must be WRITE):

    ```sh
    HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token
    ```

## Run Instructions

1. Start the FastAPI server:

    ```sh
     uvicorn main:app --reload
    ```

    The server will start at `http://127.0.0.1:8000`.

2. Make a POST request to the `/summarize` endpoint to get a summary. You can use the following example code:

    ```python
    import requests

    data = {
        'text': 'Some text'
    }

    response = requests.post(url='http://127.0.0.1:8000/summarize', json=data)

    print(response.json())
    ```

## Logging

- Logs are saved to `history.log` in the root directory.
