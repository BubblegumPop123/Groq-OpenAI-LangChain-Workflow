from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

class CrawlRequest(BaseModel):
    url: str

@app.post("/crawl")
def crawl_page(request: CrawlRequest):
    try:
        result = subprocess.run(
            ["python", "crawler_script.py", request.url],
            capture_output=True,
            text=True
        )
        logging.info(f"Subprocess finished with return code {result.returncode}")
        if result.returncode != 0:
            logging.error(f"Subprocess error: {result.stderr}")
            raise HTTPException(status_code=500, detail="Error running crawler script")
        elements = json.loads(result.stdout)
        return {"elements": elements}
    except Exception as e:
        logging.error(f"Unexpected error during crawling: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error during crawling: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
