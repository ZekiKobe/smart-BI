import { Container } from '@mui/material';
import QueryInterface from '../components/QueryInterface';
import DashboardGenerator from '../components/DashboardGenerator';
import DataExplainer from '../components/DataExplainer';

export default function Home() {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <QueryInterface />
      <DashboardGenerator />
      <DataExplainer />
    </Container>
  );
}