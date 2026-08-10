import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getHealth, getJobs, getPeople } from '../services/api';

export default function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [people, setPeople] = useState([]);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        const [jobsResponse, peopleResponse, healthResponse] = await Promise.all([getJobs(), getPeople(), getHealth()]);
        setJobs(jobsResponse.jobs || []);
        setPeople(peopleResponse.people || []);
        setHealth(healthResponse);
      } catch (err) {
        setError(err.message || 'Unable to load dashboard data.');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="space-y-8">
      <section className="overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-br from-cyan-600/20 via-slate-900 to-slate-900 p-8 shadow-2xl">
        <div className="max-w-2xl">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.3em] text-cyan-300">CareerGraph</p>
          <h1 className="text-4xl font-semibold text-white sm:text-5xl">Explore careers through a connected skill graph.</h1>
          <p className="mt-4 text-lg text-slate-300">
            Discover roles, compare your strengths to job requirements, and surface the skills you still need to grow.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link to="/jobs" className="rounded-full bg-cyan-500 px-5 py-3 font-medium text-slate-950 transition hover:bg-cyan-400">
              Explore Jobs
            </Link>
            <Link to="/match" className="rounded-full border border-slate-700 px-5 py-3 font-medium text-slate-100 transition hover:border-cyan-400 hover:text-cyan-300">
              Try Career Match
            </Link>
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
          <p className="text-sm text-slate-400">Backend</p>
          <p className="mt-2 text-2xl font-semibold text-white">{health?.database === 'connected' ? 'Connected' : 'Unavailable'}</p>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
          <p className="text-sm text-slate-400">Job Roles</p>
          <p className="mt-2 text-2xl font-semibold text-white">{jobs.length}</p>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
          <p className="text-sm text-slate-400">Profiles</p>
          <p className="mt-2 text-2xl font-semibold text-white">{people.length}</p>
        </div>
      </section>

      <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-white">Career Match</h2>
            <p className="mt-1 text-sm text-slate-400">Choose a person and a target role to compare skills and uncover gaps.</p>
          </div>
          <Link to="/match" className="text-sm font-medium text-cyan-300 hover:text-cyan-200">
            Open match view →
          </Link>
        </div>
        <div className="mt-6 rounded-2xl border border-dashed border-slate-700 bg-slate-950/70 p-6 text-sm text-slate-300">
          {loading ? <p>Loading insights…</p> : error ? <p className="text-rose-400">{error}</p> : <p>Use the Career Match page to compare Maya Singh against Data Scientist and see which skills you still need.</p>}
        </div>
      </section>
    </div>
  );
}
