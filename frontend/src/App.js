import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AuthPage from "../src/Pages/Auth";
import PhotoUploadPage from "../src/Pages/Home";

function App() {
  const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            isAuthenticated ? (
              <Navigate to="/upload" replace />
            ) : (
              <Navigate to="/auth" replace />
            )
          }
        />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/upload" element={<PhotoUploadPage />} />
      </Routes>
    </Router>
  );
}

export default App;
