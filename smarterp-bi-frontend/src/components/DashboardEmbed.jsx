import React, { useEffect, useState } from 'react';
import { fetchDashboardDetail } from '../services/superset';

function DashboardEmbed({ dashboardId }) {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardDetail(dashboardId)
      .then(data => setDashboard(data.result))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [dashboardId]);

  if (loading) return <div>Loading dashboard...</div>;
  if (!dashboard) return <div>Dashboard not found.</div>;

  // You can customize the embed URL as needed
  const supersetUrl = `http://localhost:8088/superset/dashboard/${dashboardId}/`;

  return (
    <div>
      <h3>{dashboard.dashboard_title}</h3>
      <iframe
        src={supersetUrl}
        width="100%"
        height="800"
        title="Superset Dashboard"
        frameBorder="0"
      />
    </div>
  );
}

export default DashboardEmbed; 