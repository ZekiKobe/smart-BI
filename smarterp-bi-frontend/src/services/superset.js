export async function fetchDashboards() {
  const response = await fetch('http://localhost:8000/api/dashboards/');
  if (!response.ok) throw new Error('Failed to fetch dashboards');
  return response.json();
}

export async function fetchDashboardDetail(dashboardId) {
  const response = await fetch(`http://localhost:8000/api/dashboards/${dashboardId}/`);
  if (!response.ok) throw new Error('Failed to fetch dashboard detail');
  return response.json();
}

export async function generateDashboard(prompt, llm) {
  const response = await fetch('http://localhost:8000/api/generate_dashboard/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, llm })
  });
  if (!response.ok) throw new Error('Failed to generate dashboard');
  return response.json();
} 