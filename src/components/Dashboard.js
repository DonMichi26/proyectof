import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  AppBar,
  Toolbar,
} from '@mui/material';
import axios from 'axios';

const Dashboard = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/api/v1/dashboard/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUserData(response.data);
      } catch (err) {
        if (err.response?.status === 401) {
          // Token expirado o inválido
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          navigate('/login');
        } else {
          setError('Error al cargar los datos del dashboard');
        }
      }
    };

    fetchDashboardData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  if (!userData) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <Typography>Cargando...</Typography>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        backgroundImage: 'url(/biblioteca.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <AppBar position="static" sx={{ background: 'rgba(25, 118, 210, 0.8)', boxShadow: 'none' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: '#fff' }}>
            Dashboard
          </Typography>
          <Button 
            color="inherit" 
            onClick={handleLogout}
            sx={{
              color: '#fff',
              borderColor: '#fff',
              '&:hover': {
                background: 'rgba(255, 255, 255, 0.2)',
              },
            }}
          >
            Cerrar Sesión
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
        {error && (
          <Typography color="error" sx={{ mb: 2, bgcolor: 'rgba(255, 255, 255, 0.9)', p: 1, borderRadius: 1 }}>
            {error}
          </Typography>
        )}

        <Grid container spacing={3}>
          {/* Información del Usuario */}
          <Grid item xs={12} md={6}>
            <Paper 
              sx={{
                p: 3,
                background: 'rgba(255, 255, 255, 0.9)',
                borderRadius: 2,
                boxShadow: 3,
              }}
            >
              <Typography variant="h5" gutterBottom sx={{ color: '#1976d2', fontWeight: 'bold' }}>
                Información del Usuario
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Usuario:</strong> {userData.usuario.username}
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Email:</strong> {userData.usuario.email}
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Último acceso:</strong> {userData.usuario.last_login || 'N/A'}
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Fecha de registro:</strong> {userData.usuario.date_joined}
              </Typography>
            </Paper>
          </Grid>

          {/* Estadísticas */}
          <Grid item xs={12} md={6}>
            <Paper 
              sx={{
                p: 3,
                background: 'rgba(255, 255, 255, 0.9)',
                borderRadius: 2,
                boxShadow: 3,
              }}
            >
              <Typography variant="h5" gutterBottom sx={{ color: '#1976d2', fontWeight: 'bold' }}>
                Estadísticas
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <Card 
                    sx={{
                      background: 'rgba(240, 240, 240, 0.9)',
                      boxShadow: 1,
                      borderRadius: 2,
                    }}
                  >
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        Total Usuarios
                      </Typography>
                      <Typography variant="h4" sx={{ color: '#1976d2', fontWeight: 'bold' }}>
                        {userData.estadisticas.total_usuarios}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Card 
                    sx={{
                      background: 'rgba(240, 240, 240, 0.9)',
                      boxShadow: 1,
                      borderRadius: 2,
                    }}
                  >
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        Usuarios Activos
                      </Typography>
                      <Typography variant="h4" sx={{ color: '#28a745', fontWeight: 'bold' }}>
                        {userData.estadisticas.usuarios_activos}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Card 
                    sx={{
                      background: 'rgba(240, 240, 240, 0.9)',
                      boxShadow: 1,
                      borderRadius: 2,
                    }}
                  >
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        Usuarios Staff
                      </Typography>
                      <Typography variant="h4" sx={{ color: '#ffc107', fontWeight: 'bold' }}>
                        {userData.estadisticas.usuarios_staff}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Dashboard; 