from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
import os
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from pydantic import BaseModel
from logger import logging
load_dotenv()

app = FastAPI()
logging.info("Application started successfully.")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    question: str

class DownloadRequest(BaseModel):
    answer: str

class LLMConfig(BaseModel):
    provider: str
    api_key: str
    model: str    

llm_config = {}

@app.post("/set_llm_config")
async def set_llm_config(config: LLMConfig):
    global llm_config
    llm_config = config.dict()
    return {"message": "LLM config saved successfully!", "config": llm_config}

@app.get("/get_llm_config")
async def get_llm_config():
    return llm_config

@app.post("/query")
async def query_travel_agent(query:QueryRequest, config: dict = Depends(get_llm_config)):
    try:
        print(query)
        graph = GraphBuilder(config=config)
        react_app=graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        # Assuming request is a pydantic object like: {"question": "your text"}
        messages={"messages": [query.question]}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output}
    except Exception as e:
       raise Exception(f"The response failed due to {e}")
    
@app.post("/download")
async def download_travel_plan(data: DownloadRequest):
    filename = save_document(response_text=data.answer)

    return FileResponse(
        path=filename,
        media_type="application/pdf",
        filename="travel_plan.pdf"
    )

