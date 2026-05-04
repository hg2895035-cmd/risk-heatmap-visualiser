import RiskList from "./pages/RiskList";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-900 text-white p-4">
        <h1 className="text-xl font-bold">Risk Heatmap Visualiser</h1>
      </nav>

      <RiskList />
    </div>
  );
}

export default App;