import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { RegistrationPage } from './pages/RegistrationPage';
import { PersonsPage } from './pages/PersonsPage';
import { MonitoringPage } from './pages/MonitoringPage';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="register" element={<RegistrationPage />} />
        <Route path="persons" element={<PersonsPage />} />
        <Route path="monitoring" element={<MonitoringPage />} />
      </Route>
    </Routes>
  );
}

export default App;
