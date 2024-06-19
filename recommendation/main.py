from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
import httpx
import logging
import asyncio

# Load environment variables from .env file
load_dotenv()

# Define your OpenAI API key
openai.api_key = "input your key"

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the request model
class ActionRecommendationRequest(BaseModel):
    url: str

# Define the get_gpt_command function
def get_gpt_command(filtering_elements, decomposition_steps):
    prompt_template = f"""
    You are an agent controlling a browser. You are given:

    (1) an objective to navigate and interact with the elements on the given URL.
    (2) a list of elements from the page.
    (3) a list of steps decomposed from the user's intent.

    Based on the elements available and the steps provided, issue the following commands:

    SCROLL UP - scroll up one page
    SCROLL DOWN - scroll down one page
    CLICK X - click on a given element by its id
    TYPE X "TEXT" - type the specified text into the input with id X
    TYPESUBMIT X "TEXT" - type the specified text into the input with id X and then press ENTER

    The available elements are:
    {filtering_elements}

    The steps to accomplish are:
    {decomposition_steps}

    Based on the steps and elements, issue the appropriate commands to accomplish the objective.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an agent controlling a browser."},
            {"role": "user", "content": prompt_template},
        ]
    )

    return response.choices[0].message["content"].strip()

# Function to get filtered elements from the filtering service
async def get_filtering_elements(url):
    async with httpx.AsyncClient(timeout=60.0) as client:  # Increase the timeout to 60 seconds
        for attempt in range(5):  # Retry up to 5 times
            try:
                logger.info("Requesting filtering elements for URL: %s (attempt %d)", url, attempt + 1)
                response = await client.post(
                    "http://127.0.0.1:8000/crawl",
                    json={"url": url}
                )
                response.raise_for_status()
                elements = response.json()["elements"]
                logger.info("Filtering elements received: %s", elements)
                return elements
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred while fetching filtering elements: {e.response.status_code} - {e.response.text}")
                raise
            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.error(f"An error occurred while fetching filtering elements: {str(e)}", exc_info=True)
                if attempt < 4:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise

# Function to get decomposition steps from the decomposition service
async def get_decomposition_steps(url):
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            logger.info("Requesting decomposition steps for URL: %s", url)
            response = await client.post(
                "http://127.0.0.1:8001/ask/",
                data={"user_question": f"write me the action steps in bullet points in decomposed mode to follow as an LAM to access {url}. make sure you start with only bullet points. no introduction or anything."}
            )
            response.raise_for_status()
            steps = response.json()["answer"]
            logger.info("Decomposition steps received: %s", steps)
            return steps
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred while fetching decomposition steps: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"An error occurred while fetching decomposition steps: {str(e)}", exc_info=True)
            raise

# Define the root endpoint
@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define the action recommendation endpoint
@app.post('/recommend')
async def recommend_action(request: ActionRecommendationRequest):
    try:
        logger.info("Received request: %s", request.url)
        filtering_elements = await get_filtering_elements(request.url)
        logger.info("Filtered elements: %s", filtering_elements)
        decomposition_steps = await get_decomposition_steps(request.url)
        logger.info("Decomposition steps: %s", decomposition_steps)
        command = get_gpt_command(filtering_elements, decomposition_steps)
        logger.info("Generated command: %s", command)
        return {'recommended_action': command}
    except Exception as e:
        logger.error("Error occurred: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Run the server with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
