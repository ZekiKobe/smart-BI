import React,{ useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { 
  Box, 
  Button, 
  TextField, 
  Typography, 
  CircularProgress,
  Snackbar,
  Alert,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Paper
} from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import { generateSql } from '../services/api';

export default function QueryInterface() {
  const [query, setQuery] = useState('');
  const [sqlResult, setSqlResult] = useState('');
  const [notification, setNotification] = useState(null);
  const [selectedModel, setSelectedModel] = useState('gemini');
  
  const models = [
    { id: 'gemini', name: 'Google Gemini' },
    { id: 'deepseek', name: 'DeepSeek' }
  ];

  const { mutate, isLoading } = useMutation({
    mutationFn: (variables) => generateSql(variables),
    onSuccess: (data) => {
      setSqlResult(data.sql);
    },
    onError: (error) => {
      setNotification({
        message: error.response?.data?.error || 'Failed to generate SQL',
        severity: 'error'
      });
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    mutate({ prompt: query, model: selectedModel });
  };

  const handleCopy = () => {
    setNotification({
      message: 'SQL copied to clipboard!',
      severity: 'success'
    });
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        Natural Language to SQL
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
          label="Ask your data question"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., Show me the monthly sales trend for our top 10 products in Addis Ababa last year"
          sx={{ mb: 2 }}
        />
        
        <Button
          type="submit"
          variant="contained"
          disabled={isLoading}
          startIcon={isLoading ? <CircularProgress size={20} /> : null}
        >
          {isLoading ? 'Generating...' : 'Generate SQL'}
        </Button>
      </form>
      
      {sqlResult && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Generated SQL:
          </Typography>
          <Box
            sx={{
              p: 2,
              bgcolor: 'background.paper',
              borderRadius: 1,
              border: '1px solid',
              borderColor: 'divider',
              position: 'relative',
              overflowX: 'auto'
            }}
          >
            <pre style={{ margin: 0 }}>{sqlResult}</pre>
            <CopyToClipboard text={sqlResult} onCopy={handleCopy}>
              <Button
                size="small"
                startIcon={<ContentCopyIcon />}
                sx={{ position: 'absolute', top: 8, right: 8 }}
              >
                Copy
              </Button>
            </CopyToClipboard>
          </Box>
        </Box>
      )}
      
      <Snackbar
        open={!!notification}
        autoHideDuration={6000}
        onClose={() => setNotification(null)}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert
          onClose={() => setNotification(null)}
          severity={notification?.severity}
          sx={{ width: '100%' }}
        >
          {notification?.message}
        </Alert>
      </Snackbar>
    </Paper>
  );
}