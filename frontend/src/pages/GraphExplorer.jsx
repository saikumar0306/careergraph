import { useEffect, useState } from 'react';
import { getSkillConnections, getSkills } from '../services/api';

export default function GraphExplorer() {
  const [skills, setSkills] = useState([]);
  const [skillId, setSkillId] = useState('');
  const [connections, setConnections] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadSkills() {
      try {
        setLoading(true);
        setError('');
        const response = await getSkills();
        const availableSkills = response.skills || [];
        setSkills(availableSkills);
        if (availableSkills.length > 0) {
          setSkillId(availableSkills[0].id);
        }
      } catch (err) {
        setError(err.message || 'Unable to load skills.');
      } finally {
        setLoading(false);
      }
    }

    loadSkills();
  }, []);

  useEffect(() => {
    if (!skillId) return;

    async function loadConnections() {
      try {
        setLoading(true);
        setError('');
        const data = await getSkillConnections(skillId);
        setConnections(data);
      } catch (err) {
        setError(err.message || 'Unable to load skill connections.');
      } finally {
        setLoading(false);
      }
    }

    loadConnections();
  }, [skillId]);

  return (
    <div className="grid gap-6 lg:grid-cols-[0.85fr_1.15fr]">
      <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
        <h2 className="text-2xl font-semibold text-white">Graph Explorer</h2>
        <p className="mt-1 text-sm text-slate-400">Choose a skill to inspect the roles and technologies connected to it.</p>

        <label className="mt-6 block text-sm font-medium text-slate-200">
          Skill
          <select value={skillId} onChange={(event) => setSkillId(event.target.value)} className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none focus:border-cyan-500">
            {skills.length === 0 ? (
              <option value="">Loading skill list...</option>
            ) : (
              skills.map((skill) => (
                <option key={skill.id} value={skill.id}>
                  {skill.name}
                </option>
              ))
            )}
          </select>
        </label>
      </section>

      <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
        {loading ? (
          <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6 text-slate-300">Exploring connections…</div>
        ) : error ? (
          <div className="rounded-2xl border border-rose-700/40 bg-rose-950/40 p-6 text-rose-200">{error}</div>
        ) : (
          <div className="space-y-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
              <p className="text-sm text-slate-400">Selected Skill</p>
              <h3 className="mt-1 text-xl font-semibold text-white">{connections?.skill}</h3>
              <p className="mt-2 text-sm text-slate-300">This view highlights the job roles and technologies that connect through the chosen skill.</p>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
                <h4 className="font-semibold text-white">Connected Job Roles</h4>
                <div className="mt-3 space-y-2">
                  {connections?.job_roles?.length ? (
                    connections.job_roles.map((job) => (
                      <div key={job.id} className="rounded-xl border border-slate-800 bg-slate-900/70 px-3 py-2 text-sm text-slate-200">
                        {job.name}
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-slate-400">No connected roles returned.</p>
                  )}
                </div>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
                <h4 className="font-semibold text-white">Connected Technologies</h4>
                <div className="mt-3 space-y-2">
                  {connections?.technologies?.length ? (
                    connections.technologies.map((tech) => (
                      <div key={tech.id} className="rounded-xl border border-slate-800 bg-slate-900/70 px-3 py-2 text-sm text-slate-200">
                        {tech.name}
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-slate-400">No connected technologies returned.</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
