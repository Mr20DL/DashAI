import { useState } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Registrar componentes de gráficos
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [file, setFile] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Por favor selecciona un archivo CSV primero.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Conectamos con tu Backend Python
      const response = await axios.post('http://127.0.0.1:8000/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setDashboardData(response.data);
    } catch (err) {
      console.error(err);
      setError("Error al conectar con el servidor. ¿Está corriendo el backend?");
    } finally {
      setLoading(false);
    }
  };

  // Preparar datos para el gráfico
  const getChartData = () => {
    if (!dashboardData) return null;

    const historico = dashboardData.data.historico;
    const prediccion = dashboardData.data.prediccion;

    // Unimos fechas para el eje X
    const labels = [
      ...historico.map(d => d.fecha),
      ...prediccion.map(d => d.fecha)
    ];

    // Datos históricos (rellenamos con null la parte futura)
    const dataHistorica = [
      ...historico.map(d => d.ventas),
      ...new Array(prediccion.length).fill(null)
    ];

    // Datos predicción (rellenamos con null la parte pasada)
    // Truco: el primer punto de predicción debería conectar con el último histórico
    const lastHistoryVal = historico[historico.length - 1].ventas;
    const dataPrediccion = [
      ...new Array(historico.length - 1).fill(null),
      lastHistoryVal, // Punto de conexión
      ...prediccion.map(d => d.ventas_predichas)
    ];

    return {
      labels,
      datasets: [
        {
          label: 'Ventas Históricas',
          data: dataHistorica,
          borderColor: 'rgb(59, 130, 246)', // Azul Tailwind
          backgroundColor: 'rgba(59, 130, 246, 0.5)',
          tension: 0.3,
        },
        {
          label: 'Predicción IA',
          data: dataPrediccion,
          borderColor: 'rgb(244, 63, 94)', // Rojo/Rosa Tailwind
          backgroundColor: 'rgba(244, 63, 94, 0.5)',
          borderDash: [5, 5], // Línea punteada
          tension: 0.3,
        },
      ],
    };
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8 font-sans text-gray-800">
      <div className="max-w-5xl mx-auto">

        {/* Header */}
        <header className="mb-10 text-center">
          <h1 className="text-4xl font-bold text-indigo-700 mb-2">DashAI 🚀</h1>
          <p className="text-gray-500">Sube tu historial de ventas y deja que la IA prediga el futuro.</p>
        </header>

        {/* Zona de Carga */}
        {!dashboardData && (
          <div className="bg-white p-10 rounded-2xl shadow-lg text-center max-w-lg mx-auto border-2 border-dashed border-indigo-200 hover:border-indigo-400 transition-colors">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 mb-4"
            />
            <button
              onClick={handleUpload}
              disabled={loading}
              className="w-full bg-indigo-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
            >
              {loading ? "Analizando datos..." : "Generar Predicción 🔮"}
            </button>
            {error && <p className="mt-4 text-red-500 text-sm">{error}</p>}
          </div>
        )}

        {/* Dashboard de Resultados */}
        {dashboardData && (
          <div className="space-y-8 animate-fade-in">

            {/* Tarjetas de Resumen */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-blue-500">
                <h3 className="text-gray-500 text-sm uppercase font-bold">Ventas Históricas Total</h3>
                <p className="text-3xl font-bold text-gray-800">
                  ${dashboardData.data.resumen.total_ventas_historicas.toLocaleString()}
                </p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-pink-500">
                <h3 className="text-gray-500 text-sm uppercase font-bold">Predicción Mes Siguiente</h3>
                <p className="text-3xl font-bold text-indigo-600">
                  ${dashboardData.data.resumen.prediccion_mes_siguiente.toLocaleString()}
                </p>
              </div>
            </div>

            {/* Tarjeta de Insight (IA) */}
            <div className={`bg-white p-6 rounded-xl shadow-md border border-l-8 ${dashboardData.insight.tone === 'positive' ? 'border-l-green-500' : 'border-l-yellow-500'}`}>
              <h3 className="text-lg font-bold mb-2 flex items-center gap-2">
                🤖 Consejo de Estrategia IA
              </h3>
              <p className="text-gray-700 leading-relaxed">
                {dashboardData.insight.text}
              </p>
            </div>

            {/* Gráfico */}
            <div className="bg-white p-6 rounded-xl shadow-md">
              <Line data={getChartData()} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />
            </div>

            <button
              onClick={() => { setDashboardData(null); setFile(null); }}
              className="block mx-auto text-indigo-600 hover:underline mt-8"
            >
              ← Subir otro archivo
            </button>

          </div>
        )}

      </div>
    </div>
  );
}

export default App;