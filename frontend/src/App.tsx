import React from "react";
import "./App.css";
import AppNav from "./AppNav";
import AppHeader from "./AppHeader";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <div className="App">
      <AppNav />
      <AppHeader text="Dashboard" />
      <main>
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
