import { useEffect, useState } from 'react';
import { getJob, getJobSkills, getJobs } from '../services/api';

export default function JobExplorer() {
  const [jobs, setJobs] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState('');
  const [jobDetails, setJobDetails] = useState(null);
  const [jobSkills, setJobSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadJobs() {
      try {
        setLoading(true);
        const response = await getJobs();
        const loadedJobs = response.jobs || [];
        setJobs(loadedJobs);
        if (loadedJobs.length > 0) {
          setSelectedJobId(loadedJobs[0].id);
        }
      } catch (err) {
        setError(err.message || 'Unable to load jobs.');
      } finally {
        setLoading(false);
      }
    }
    loadJobs();
  }, []);

  useEffect(() => {
    if (!selectedJobId) return;

    async function loadJobDetails() {
      try {
        setError('');
        const [details, skillsResponse] = await Promise.all([getJob(selectedJobId), getJobSkills(selectedJobId)]);
        setJobDetails(details);
        setJobSkills(skillsResponse.skills || []);
      } catch (err) {
        setError(err.message || 'Unable to load the selected job.');
        setJobDetails(null);
        setJobSkills([]);
      }
    }

    loadJobDetails();
  }, [selectedJobId]);

  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
      <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-white">Job Explorer</h2>
            <p className="mt-1 text-sm text-slate-400">Browse roles and inspect the skills each one requires.</p>
          </div>
        </div>

        {loading ? (
          <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6 text-slate-300">Loading roles…</div>
        ) : error && jobs.length === 0 ? (
          <div className="rounded-2xl border border-rose-700/40 bg-rose-950/40 p-6 text-rose-200">{error}</div>
        ) : (
          <div className="space-y-3">
            {jobs.map((job) => {
              const active = selectedJobId === job.id;
              return (
                <button
                  key={job.id}
                  onClick={() => setSelectedJobId(job.id)}
                  className={`w-full rounded-2xl border p-4 text-left transition ${
                    active ? 'border-cyan-500 bg-cyan-500/10' : 'border-slate-800 bg-slate-950/70 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-semibold text-white">{job.name}</p>
                      <p className="mt-1 text-sm text-slate-400">{job.description}</p>
                    </div>
                    <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">View</span>
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </section>

      <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
        {!selectedJobId ? (
          <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-950/70 p-6 text-slate-400">Select a role to inspect its requirements.</div>
        ) : error ? (
          <div className="rounded-2xl border border-rose-700/40 bg-rose-950/40 p-6 text-rose-200">{error}</div>
        ) : jobDetails ? (
          <div className="space-y-6">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-300">Selected role</p>
              <h3 className="mt-2 text-2xl font-semibold text-white">{jobDetails.name}</h3>
              <p className="mt-3 text-slate-300">{jobDetails.description}</p>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-white">Required skills</h4>
              {jobSkills.length === 0 ? (
                <p className="mt-2 rounded-2xl border border-dashed border-slate-700 bg-slate-950/70 p-4 text-slate-400">No required skills were returned for this role.</p>
              ) : (
                <div className="mt-3 flex flex-wrap gap-2">
                  {jobSkills.map((skill) => (
                    <span key={skill.id} className="rounded-full border border-cyan-500/40 bg-cyan-500/10 px-3 py-2 text-sm text-cyan-200">
                      {skill.name}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-950/70 p-6 text-slate-400">Loading role details…</div>
        )}
      </section>
    </div>
  );
}
