const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8010';

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || 'Request failed');
  }

  return response.json();
}

export async function getJobs() {
  return request('/api/jobs');
}

export async function getJob(jobId) {
  return request(`/api/jobs/${encodeURIComponent(jobId)}`);
}

export async function getJobSkills(jobId) {
  return request(`/api/jobs/${encodeURIComponent(jobId)}/skills`);
}

export async function getPeople() {
  return request('/api/people');
}

export async function getPersonMatches(personId) {
  return request(`/api/people/${encodeURIComponent(personId)}/matches`);
}

export async function getMissingSkills(personId, jobId) {
  return request(`/api/people/${encodeURIComponent(personId)}/missing-skills/${encodeURIComponent(jobId)}`);
}

export async function getSkillConnections(skillId) {
  return request(`/api/skills/${encodeURIComponent(skillId)}/connections`);
}

export async function getHealth() {
  return request('/health/db');
}
