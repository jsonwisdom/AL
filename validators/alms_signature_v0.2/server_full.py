from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/verify/full")
def verify_full():
    return {
        "status": "BOOTSTRAP_OK",
        "message": "ALMS full verifier online"
    }
