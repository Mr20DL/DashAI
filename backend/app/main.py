from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.ml.engine import process_and_predict
from app.ml.insights import generate_business_advice
from app import models, database

# 1. Crear las tablas en la Base de Datos al iniciar
# Esta es la línea mágica que te faltaba para que Postgres cree la tabla "predictions"
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="DashAI API", version="1.0.0")

# Configuración CORS (Para cuando conectemos el Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de la DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "DashAI API is running con Database 🚀"}

@app.post("/predict")
async def predict_sales(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    try:
        contents = await file.read()
        
        # Lógica ML
        result_data = process_and_predict(contents)
        ai_insight = generate_business_advice(result_data["resumen"])
        
        # GUARDAR EN DB
        db_prediction = models.PredictionHistory(
            filename=file.filename,
            total_sales_predicted=result_data["resumen"]["prediccion_mes_siguiente"],
            advice_given=ai_insight["text"]
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        return {
            "status": "success",
            "db_id": db_prediction.id,
            "data": result_data,
            "insight": ai_insight
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ESTE ES EL ENDPOINT QUE FALTABA
@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    return db.query(models.PredictionHistory).all()