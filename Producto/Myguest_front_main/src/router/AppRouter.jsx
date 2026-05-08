import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from '../pages/login/LoginPage'
import DashboardPage from '../pages/dashboard/DashboardPage'
import UsuariosPage from '../pages/usuarios/UsuariosPage'
import EnConstruccion from '../pages/EnConstruccion'
import useAuthStore from '../store/authStore'
import InventarioPage from '../pages/inventario/InventarioPage'
import ProveedoresPage from '../pages/proveedores/ProveedoresPage'

const PrivateRoute = ({ children }) => {
  const { token } = useAuthStore()
  return token ? children : <Navigate to="/login" />
}

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
        <Route path="/usuarios" element={<PrivateRoute><UsuariosPage /></PrivateRoute>} />
        <Route path="/inventario" element={<PrivateRoute><InventarioPage /></PrivateRoute>} />
        <Route path="/compras" element={<PrivateRoute><EnConstruccion titulo="Compras" /></PrivateRoute>} />
        <Route path="/proveedores" element={<PrivateRoute><ProveedoresPage /></PrivateRoute>} />
        <Route path="/facturacion" element={<PrivateRoute><EnConstruccion titulo="Facturación" /></PrivateRoute>} />
        <Route path="/mermas" element={<PrivateRoute><EnConstruccion titulo="Mermas" /></PrivateRoute>} />
        <Route path="/reportes" element={<PrivateRoute><EnConstruccion titulo="Reportes" /></PrivateRoute>} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRouter