import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import RunTest from './pages/RunTest';
import Sessions from './pages/Sessions';
import SessionDetail from './pages/SessionDetail';
import IssueDetail from './pages/IssueDetail';
import ActionTimeline from './pages/ActionTimeline';
import LLMReport from './pages/LLMReport';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Landing from './pages/Landing';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/*"
          element={
            <MainLayout>
              <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/run-test" element={<RunTest />} />
                <Route path="/sessions" element={<Sessions />} />
                <Route path="/session/:id" element={<SessionDetail />} />
                <Route path="/session/:id/actions" element={<ActionTimeline />} />
                <Route path="/session/:id/llm-report" element={<LLMReport />} />
                <Route path="/issue/:id" element={<IssueDetail />} />
              </Routes>
            </MainLayout>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
