import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import {
  Box,
  Button,
  TextField,
  Typography,
  CircularProgress,
  Snackbar,
  Alert,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import { generateDashboard } from '../services/superset';

export default function DashboardGenerator() {
  const [prompt, setPrompt] = useState('');
  const [selectedModel, setSelectedModel] = useState('gemini');
  const [notification, setNotification] = useState(null);
  const [dashboardUrl, setDashboardUrl] = useState('');

  const models = [
    { id: 'gemini', name: 'Google Gemini' },
    { id: 'deepseek', name: 'DeepSeek' }
  ];

  const { mutate, isLoading } = useMutation({
    mutationFn: ({ prompt, model }) => generateDashboard(prompt, model),
    onSuccess: (data) => {
      setNotification({
        message: `Dashboard created successfully!`,
        severity: 'success'
      });
      setDashboardUrl(data.dashboard_url || '');
      setPrompt('');
    },
    onError: (error) => {
      setNotification({
        message: error.message || 'Failed to create dashboard',
        severity: 'error'
      });
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim()) {
      setNotification({
        message: 'Dashboard request is required',
        severity: 'warning'
      });
      return;
    }
    mutate({
      prompt,
      model: selectedModel
    });
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        Dashboard Generator
      </Typography>
      <form onSubmit={handleSubmit}>
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>LLM Model</InputLabel>
          <Select
            value={selectedModel}
            label="LLM Model"
            onChange={(e) => setSelectedModel(e.target.value)}
          >
            {models.map((model) => (
              <MenuItem key={model.id} value={model.id}>
                {model.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <TextField
          fullWidth
          multiline
          rows={4}
          variant="outlined"
          label="Describe your dashboard request"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g., Create a dashboard showing monthly sales trends, top 5 products by revenue, and regional sales distribution."
          sx={{ mb: 2 }}
        />
        <Button
          type="submit"
          variant="contained"
          disabled={isLoading}
          startIcon={isLoading ? <CircularProgress size={20} /> : null}
        >
          {isLoading ? 'Creating...' : 'Generate Dashboard'}
        </Button>
      </form>
      {dashboardUrl && (
        <Box sx={{ mt: 3 }}>
          <Alert severity="success">
            Dashboard created!{' '}
            <a href={dashboardUrl} target="_blank" rel="noopener noreferrer">View in Superset</a>
          </Alert>
        </Box>
      )}
      <Snackbar
        open={!!notification}
        autoHideDuration={6000}
        onClose={() => setNotification(null)}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        {notification && (
          <Alert onClose={() => setNotification(null)} severity={notification.severity} sx={{ width: '100%' }}>
            {notification.message}
          </Alert>
        )}
      </Snackbar>
    </Paper>
  );
}