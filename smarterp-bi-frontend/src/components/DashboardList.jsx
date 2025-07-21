import React, { useEffect, useState } from 'react';
import { fetchDashboards } from '../services/superset';

function DashboardList({ onSelect }) {
  const [dashboards, setDashboards] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboards()
      .then(data => setDashboards(data.result))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading dashboards...</div>;

  return (
    <div>
      <h2>Dashboards</h2>
      <ul>
        {dashboards.map(d => (
          <li key={d.id}>
            <button onClick={() => onSelect(d.id)}>{d.dashboard_title}</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DashboardList; 