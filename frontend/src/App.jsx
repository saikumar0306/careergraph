import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import JobExplorer from './pages/JobExplorer';
import CareerMatch from './pages/CareerMatch';
import GraphExplorer from './pages/GraphExplorer';

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/jobs" element={<JobExplorer />} />
          <Route path="/match" element={<CareerMatch />} />
          <Route path="/graph" element={<GraphExplorer />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
