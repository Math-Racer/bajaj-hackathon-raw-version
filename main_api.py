
from fastapi import FastAPI, HTTPException, Header, Request
from typing import Optional
import json
from pdf_qa_chatgpt import mainfunc as pdf_qa_main
import os

app = FastAPI()

EXPECTED_TOKEN = "6e6de8c174e72f2501628ae7ddc119732bc8c34a72097f682a2bf339db673dd7"

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"status": "ok"}


@app.post("/api/v1/hackrx/run")
async def run_qa(request: Request, authorization: Optional[str] = Header(None)):
    if authorization != f"Bearer {EXPECTED_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    try:
        input_json = await request.body()
        input_json_str = input_json.decode("utf-8")
        result_json = pdf_qa_main(input_json_str)
        result = json.loads(result_json)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  
    uvicorn.run("main_api:app", host="0.0.0.0", port=port)


# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 8000))  
#     uvicorn.run("main_api:app", port=port)
