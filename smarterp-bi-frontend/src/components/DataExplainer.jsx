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
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { explainData } from '../services/api';

export default function DataExplainer() {
  const [dataQuestion, setDataQuestion] = useState('');
  const [selectedModel, setSelectedModel] = useState('gemini');
  const [explanations, setExplanations] = useState([]);
  const [notification, setNotification] = useState(null);
  const [expanded, setExpanded] = useState(false);

  const models = [
    { id: 'gemini', name: 'Google Gemini' },
    { id: 'deepseek', name: 'DeepSeek' }
  ];

  const { mutate, isLoading } = useMutation({
    mutationFn: (variables) => explainData(variables),
    onSuccess: (data) => {
      setExplanations(prev => [
        {
          question: dataQuestion,
          answer: data.answer,
          insights: data.insights,
          timestamp: new Date().toLocaleString(),
          id: Date.now()
        },
        ...prev
      ]);
      setDataQuestion('');
    },
    onError: (error) => {
      setNotification({
        message: error.response?.data?.error || 'Failed to get explanation',
        severity: 'error'
      });
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!dataQuestion.trim()) {
      setNotification({
        message: 'Please enter a question',
        severity: 'warning'
      });
      return;
    }
    mutate({ question: dataQuestion, data: null, model: selectedModel });
  };

  const handleAccordionChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        Data Explainer
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
          rows={3}
          variant="outlined"
          label="Ask about your data"
          value={dataQuestion}
          onChange={(e) => setDataQuestion(e.target.value)}
          placeholder="e.g., Why did sales drop last quarter? What are the key trends?"
          sx={{ mb: 2 }}
        />
        <Button
          type="submit"
          variant="contained"
          disabled={isLoading}
          startIcon={isLoading ? <CircularProgress size={20} /> : null}
        >
          {isLoading ? 'Analyzing...' : 'Explain Data'}
        </Button>
      </form>

      {explanations.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Previous Explanations
          </Typography>
          {explanations.map((item) => (
            <Accordion 
              key={item.id} 
              expanded={expanded === item.id}
              onChange={handleAccordionChange(item.id)}
              sx={{ mb: 1 }}
            >
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography sx={{ width: '33%', flexShrink: 0 }}>
                  {item.question}
                </Typography>
                <Typography sx={{ color: 'text.secondary' }}>
                  {item.timestamp}
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography paragraph sx={{ whiteSpace: 'pre-wrap' }}>
                  {item.answer}
                </Typography>
                
                {item.insights?.length > 0 && (
                  <>
                    <Typography variant="subtitle2" gutterBottom>
                      Key Insights:
                    </Typography>
                    <List dense>
                      {item.insights.map((insight, i) => (
                        <React.Fragment key={i}>
                          <ListItem>
                            <ListItemText primary={`• ${insight}`} />
                          </ListItem>
                          {i < item.insights.length - 1 && <Divider component="li" />}
                        </React.Fragment>
                      ))}
                    </List>
                  </>
                )}
              </AccordionDetails>
            </Accordion>
          ))}
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