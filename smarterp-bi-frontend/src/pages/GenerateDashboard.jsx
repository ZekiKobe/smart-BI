import React, { useState } from 'react';
import { generateDashboard } from '../services/superset';

function GenerateDashboard() {
  const [prompt, setPrompt] = useState('');
  const [llm, setLlm] = useState('gemini');
  const [loading, setLoading] = useState(false);
  const [dashboardUrl, setDashboardUrl] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setDashboardUrl(null);
    try {
      const result = await generateDashboard(prompt, llm);
      setDashboardUrl(result.dashboard_url);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 24, maxWidth: 600, margin: '0 auto' }}>
      <h2>Generate Dashboard from Prompt</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: 24 }}>
        <div style={{ marginBottom: 12 }}>
          <label>Prompt:</label><br />
          <textarea
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            rows={3}
            style={{ width: '100%' }}
            required
          />
        </div>
        <div style={{ marginBottom: 12 }}>
          <label>LLM:</label><br />
          <select value={llm} onChange={e => setLlm(e.target.value)}>
            <option value="gemini">Gemini</option>
            <option value="deepseek">DeepSeek</option>
          </select>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Dashboard'}
        </button>
      </form>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {dashboardUrl && (
        <div>
          <h3>Generated Dashboard</h3>
          <iframe
            src={dashboardUrl}
            width="100%"
            height="800"
            title="Generated Superset Dashboard"
            frameBorder="0"
          />
        </div>
      )}
    </div>
  );
}

export default GenerateDashboard; 