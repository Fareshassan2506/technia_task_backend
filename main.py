from fastapi import FastAPI
from routers import auth, real_estate, hr  # Import the real estate router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Replace with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Include routers
app.include_router(auth.auth_router, prefix="/auth", tags=["Auth"])
app.include_router(real_estate.real_estate_router, prefix="/real-estate", tags=["Real Estate"])
app.include_router(hr.hr_router, prefix="/hr", tags=["HR"])

@app.get("/")
def root():
    return {"message": "FastAPI is working!"}
