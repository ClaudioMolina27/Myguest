import useAuthStore from '../../store/authStore'
import { useNavigate } from 'react-router-dom'

const DashboardPage = () => {
  const { usuario, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Bienvenido, {usuario?.nom} {usuario?.primer_apellido}</h1>
      <p>Perfil: {usuario?.cod_perfil === 0 ? 'Administrador TI' : usuario?.cod_perfil === 1 ? 'Administrador de carrera' : 'Docente'}</p>
      <button onClick={handleLogout}>Cerrar sesión</button>
    </div>
  )
}

export default DashboardPage