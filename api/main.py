from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Company Agents API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to Company Agents API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service":  "company-agents-api"}

@app.post("/agents/run")
async def run_agent(agent_name: str, task: str):
    return {
        "agent":  agent_name,
        "task": task,
        "status":  "running",
        "result": "Agent execution started"
    }

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
