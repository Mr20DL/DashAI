# 🚀 DashAI – Intelligent Sales Forecasting

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Available-2496ED?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)

**DashAI** es una plataforma Full Stack diseñada para democratizar el análisis predictivo. Permite a las empresas subir su historial de ventas y obtener proyecciones futuras precisas mediante Machine Learning, acompañadas de consejos estratégicos generados por IA.

---

## 📸 Demo

`![Dashboard Screenshot](./Captura2.png)`

---

## ✨ Características Principales

*   **📊 Dashboard Interactivo:** Visualización de datos históricos y predictivos con gráficos dinámicos (Chart.js).
*   **🔮 Motor de Predicción ML:** Algoritmo de Regresión Lineal (Scikit-learn) que proyecta ingresos a 30 días.
*   **🤖 Consultor IA:** Módulo inteligente que analiza tendencias de crecimiento y genera recomendaciones de negocio (stock, marketing, ofertas).
*   **📂 Carga de Datos:** Procesamiento rápido de archivos CSV con validación automática.
*   **🗄️ Historial Persistente:** Arquitectura robusta con PostgreSQL y Docker para almacenar cada análisis realizado.

---

## 🛠️ Stack Tecnológico

El proyecto sigue una arquitectura moderna y desacoplada:

### **Frontend (Cliente)**
*   **React + Vite:** Rendimiento ultrarrápido.
*   **Tailwind CSS:** Diseño moderno y responsivo.
*   **Chart.js:** Visualización de datos.
*   **Axios:** Comunicación con la API.

### **Backend (Servidor)**
*   **FastAPI (Python):** API REST asíncrona de alto rendimiento.
*   **Pandas & NumPy:** Manipulación y limpieza de datos.
*   **Scikit-learn:** Entrenamiento de modelos predictivos.
*   **SQLAlchemy:** ORM para gestión de base de datos.

### **Infraestructura & DevOps**
*   **Docker Compose:** Orquestación de contenedores.
*   **PostgreSQL:** Base de datos relacional.

---

## 🚀 Instalación y Ejecución Local

Sigue estos pasos para levantar el proyecto en tu máquina.

### Prerrequisitos
*   Git
*   Docker Desktop (debe estar corriendo)
*   Python 3.10+
*   Node.js 18+

### 1. Clonar el repositorio
```bash
git clone https://github.com/Mr20DL/DashAI.git
cd DashAI
```

### 2. Levantar la Base de Datos

Usamos Docker para no tener que instalar PostgreSQL manualmente.

```bash
docker-compose up -d
```

### 3. Configurar el Backend

Abre una terminal en la carpeta backend:

```bash
cd backend
python -m venv venv

# En Windows:
.\venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

El servidor correrá en: http://127.0.0.1:8000

### 4. Configurar el Frontend

Abre una nueva terminal en la carpeta frontend:

```bash
cd frontend
npm install
npm run dev
```

La aplicación web correrá en: http://localhost:5173

## 📂 Estructura del Proyecto

Este proyecto sigue una arquitectura **Monorepo** (Frontend y Backend en el mismo repositorio) organizada de la siguiente manera:

```text
DashAI/
├── backend/                # 🧠 Lógica del Servidor y Machine Learning
│   ├── app/
│   │   ├── ml/             # Motor de Inteligencia Artificial
│   │   │   ├── engine.py   # Modelo de Predicción (Scikit-learn)
│   │   │   └── insights.py # Generador de Consejos de Negocio
│   │   ├── database.py     # Configuración de conexión a PostgreSQL
│   │   ├── models.py       # Modelos de Base de Datos (Tablas)
│   │   └── main.py         # API Gateway (FastAPI Endpoints)
│   ├── venv/               # Entorno Virtual de Python (Ignorado por Git)
│   └── requirements.txt    # Dependencias del Backend
│
├── frontend/               # 🎨 Interfaz de Usuario (React + Vite)
│   ├── src/
│   │   ├── App.jsx         # Dashboard Principal (Gráficos + Lógica de Upload)
│   │   ├── index.css       # Estilos Globales con Tailwind CSS
│   │   └── main.jsx        # Punto de entrada de React
│   ├── tailwind.config.js  # Configuración de diseño
│   └── package.json        # Dependencias del Frontend
│
├── docker-compose.yml      # 🐳 Configuración de Base de Datos Dockerizada
├── .gitignore              # Archivos excluidos del control de versiones
└── README.md               # Documentación del proyecto