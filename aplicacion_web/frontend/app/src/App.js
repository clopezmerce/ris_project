import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import GraphPage from './pages/GraphPage';
import StatusPage from './pages/StatusPage';
import eyeHorusLogo from './assets/eye_horus.png';

const App = () => {
  return (
    <Router>
      <div className="container">
        {/* Nav Menu */}
        <nav className="navbar navbar-expand mb-4">
          <div className="container-fluid">
            <NavLink to="/" className="navbar-brand d-flex align-items-center">
              <img src={eyeHorusLogo} alt="Eye Horus Logo" width="40" height="40" className="me-2" />
              Sensor Dashboard
            </NavLink>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <NavLink to="/" className="nav-link">Gráficas</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink to="/status" className="nav-link">Estados</NavLink>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        {/* Routes */}
        <div className="mt-4">
          <Routes>
            <Route path="/" element={<GraphPage />} />
            <Route path="/status" element={<StatusPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
