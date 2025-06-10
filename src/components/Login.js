import React, { useState } from 'react';
import {useNavigate} from 'react-router-dom';
import {Container,Box,TextField,Button,Typography,Paper,Alert,FormControlLabel,Checkbox,Link,InputAdornment,IconButton} from '@mui/material';
import {Visibility as VisibilityIcon,VisibilityOff as VisibilityOffIcon} from '@mui/icons-material';
import axios from 'axios';

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  /**
   * Maneja los cambios en los campos del formulario
   * @param {Event} e - Evento del cambio
   */
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  /**
   * Maneja el envío del formulario
   * @param {Event} e - Evento del submit
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
      const response = await axios.post('http://localhost:8000/api/v1/login-json/', formData);
      
      // Almacenar tokens en localStorage
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.mensaje || 'Error al iniciar sesión');
    } finally {
      setIsLoading(false);
    }
  };

  const textFieldStyles = {
    '& .MuiOutlinedInput-root': {
      '&.Mui-error .MuiOutlinedInput-notchedOutline': {
        borderColor: 'red',
      },
      '&:hover fieldset': {
        borderColor: '#1976d2',
      },
    },
  };

  return (
    // Contenedor principal con imagen de fondo
    <Box sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundImage: 'url(/biblioteca.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <Container component="main" maxWidth="xs" sx={{ display: 'flex' }}>
        <Paper
          elevation={6}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            background: 'rgba(255, 255, 255, 0.7)',
            borderRadius: '20px',
            backdropFilter: 'blur(5px)',
            flex: 1,
            maxWidth: '400px',
            mx: 'auto',
          }}
        >
          {/* Título */}
          <Typography
            component="h1"
            variant="h4"
            sx={{
              mb: 3,
              color: '#000',
              fontWeight: 'normal',
              textAlign: 'center',
            }}
          >
            ¡Bienvenido!
          </Typography>
          
          {/* Mensaje de error */}
          {error && (
            <Alert 
              severity="error" 
              sx={{ 
                mb: 2,
                width: '100%',
                borderRadius: 1,
              }}
            >
              {error}
            </Alert>
          )}

          {/* Formulario */}
          <Box 
            component="form" 
            onSubmit={handleSubmit} 
            sx={{ 
              mt: 1,
              width: '100%',
            }}
          >
            {/* Campo de usuario */}
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Usuario"
              name="username"
              autoComplete="username"
              autoFocus
              value={formData.username}
              onChange={handleChange}
              error={!!error && formData.username === ''}
              helperText={!!error && formData.username === '' ? 'Usuario es requerido' : ''}
              sx={textFieldStyles}
            />

            {/* Campo de contraseña */}
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Contraseña"
              type={showPassword ? 'text' : 'password'}
              id="password"
              autoComplete="current-password"
              value={formData.password}
              onChange={handleChange}
              error={!!error && formData.password === ''}
              helperText={!!error && formData.password === '' ? 'Contraseña es requerida' : ''}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              sx={textFieldStyles}
            />

            {/* Botón de envío */}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={isLoading}
              sx={{
                mt: 3,
                mb: 2,
                py: 1.5,
                fontSize: '1.1rem',
                textTransform: 'uppercase',
                borderRadius: '0px',
                background: isLoading ? '#4caf50' : '#1976d2',
                '&:hover': {
                  background: '#1976d2',
                  transform: 'none',
                  transition: 'none',
                },
                '&:active': {
                  transform: 'none',
                },
              }}
            >
              {isLoading ? 'INICIANDO SESIÓN...' : 'INICIAR SESIÓN'}
            </Button>
           </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default Login;