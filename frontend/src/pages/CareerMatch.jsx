import { useEffect, useMemo, useState } from 'react';
import { getJobs, getMissingSkills, getPeople, getPersonMatches } from '../services/api';

export default function CareerMatch() {
  const [people, setPeople] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [personId, setPersonId] = useState('');
  const [jobId, setJobId] = useState('');
  const [matches, setMatches] = useState([]);
  const [missingSkills, setMissingSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [matchSummary, setMatchSummary] = useState(null);

  useEffect(() => {
    async function loadPeopleAndJobs() {
      try {
        setLoading(true);
        setError('');
        const [peopleResponse, jobsResponse] = await Promise.all([getPeople(), getJobs()]);
        const loadedPeople = peopleResponse.people || [];
        const loadedJobs = jobsResponse.jobs || [];

        setPeople(loadedPeople);
        setJobs(loadedJobs);

        if (!personId && loadedPeople.length > 0) {
          setPersonId(loadedPeople[0].id);
        }

        if (!jobId && loadedJobs.length > 0) {
          setJobId(loadedJobs[0].id);
        }
      } catch (err) {
        setError(err.message || 'Unable to load people and jobs.');
      } finally {
        setLoading(false);
      }
    }

    loadPeopleAndJobs();
  }, []);

  useEffect(() => {
    if (!personId || !jobId) return;

    async function loadMatchData() {
      try {
        setLoading(true);
        setError('');
        const [matchesResponse, missingResponse] = await Promise.all([
          getPersonMatches(personId),
          getMissingSkills(personId, jobId),
        ]);
        const matchItems = matchesResponse.matches || [];
        const selectedMatch = matchItems.find((item) => item.id === jobId) || matchItems[0] || null;

        setMatches(matchItems);
        setMatchSummary(selectedMatch);
        setMissingSkills(missingResponse.missing_skills || []);
      } catch (err) {
        setError(err.message || 'Unable to load match results.');
      } finally {
        setLoading(false);
      }
    }

    loadMatchData();
  }, [personId, jobId]);

  const activePerson = useMemo(() => people.find((person) => person.id === personId) || null, [people, personId]);
  const activeJob = useMemo(() => jobs.find((job) => job.id === jobId) || null, [jobs, jobId]);

  return (
    <div className="grid gap-6 lg:grid-cols-[0.85fr_1.15fr]">
      <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
        <h2 className="text-2xl font-semibold text-white">Career Match</h2>
        <p className="mt-1 text-sm text-slate-400">Choose a person and a target role to compare their current skills against required ones.</p>

        <div className="mt-6 space-y-4">
          <label className="block text-sm font-medium text-slate-200">
            Person
            <select
              value={personId}
              onChange={(event) => setPersonId(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none focus:border-cyan-500"
            >
              {people.map((person) => (
                <option key={person.id} value={person.id}>
                  {person.name} ({person.title})
                </option>
              ))}
            </select>
          </label>

          <label className="block text-sm font-medium text-slate-200">
            Job Role
            <select
              value={jobId}
              onChange={(event) => setJobId(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none focus:border-cyan-500"
            >
              {jobs.map((job) => (
                <option key={job.id} value={job.id}>
                  {job.name}
                </option>
              ))}
            </select>
          </label>
        </div>
      </section>

      <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
        {loading ? (
          <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6 text-slate-300">Loading match analysis…</div>
        ) : error ? (
          <div className="rounded-2xl border border-rose-700/40 bg-rose-950/40 p-6 text-rose-200">{error}</div>
        ) : (
          <div className="space-y-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
              <p className="text-sm text-slate-400">Selected Profile</p>
              <h3 className="mt-1 text-xl font-semibold text-white">{activePerson?.name || personId}</h3>
              <p className="mt-2 text-sm text-slate-300">Target role: {activeJob?.name || jobId}</p>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
              <p className="text-sm text-slate-400">Match Score</p>
              <p className="mt-2 text-4xl font-semibold text-cyan-300">{matchSummary?.match_percentage ?? 0}%</p>
              <p className="mt-2 text-sm text-slate-400">{matchSummary?.matching_skills ?? 0} matching skills identified</p>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
                <h4 className="font-semibold text-white">Top matching roles</h4>
                <div className="mt-3 space-y-2">
                  {matches.length > 0 ? (
                    matches.slice(0, 4).map((match) => (
                      <div key={match.id} className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-200">
                        {match.name} — {match.match_percentage?.toFixed(0)}%
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-slate-400">No related roles returned.</p>
                  )}
                </div>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
                <h4 className="font-semibold text-white">Skills to Develop</h4>
                <div className="mt-3 flex flex-wrap gap-2">
                  {missingSkills.length > 0 ? (
                    missingSkills.map((skill) => (
                      <span key={skill} className="rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-sm text-amber-300">
                        ○ {skill}
                      </span>
                    ))
                  ) : (
                    <p className="text-sm text-slate-400">No missing skills returned.</p>
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
