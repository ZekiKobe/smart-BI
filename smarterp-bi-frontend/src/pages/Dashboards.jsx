import React, { useState } from 'react';
import DashboardList from '../components/DashboardList';
import DashboardEmbed from '../components/DashboardEmbed';

function Dashboards() {
  const [selectedDashboard, setSelectedDashboard] = useState(null);

  return (
    <div style={{ padding: 24 }}>
      <DashboardList onSelect={setSelectedDashboard} />
      {selectedDashboard && <DashboardEmbed dashboardId={selectedDashboard} />}
    </div>
  );
}

export default Dashboards; 