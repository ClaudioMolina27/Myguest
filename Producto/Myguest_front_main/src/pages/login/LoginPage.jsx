import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginRequest, getMeRequest } from '../../services/authService'
import useAuthStore from '../../store/authStore'
import useThemeStore from '../../store/themeStore'
import TopBar from '../../components/TopBar'
import styles from './LoginPage.module.css'

const LoginPage = () => {
  const [login, setLogin] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const dominiosValidos = ['@profesor.duoc.cl', '@duoc.cl']
  const dominioValido = dominiosValidos.some(dominio => login.endsWith(dominio))

  const { setToken, setUsuario } = useAuthStore()
  const { isDark, toggleTheme } = useThemeStore()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
  e.preventDefault()
  setError('')
  setLoading(true)

  const dominiosValidos = ['@profesor.duoc.cl', '@duoc.cl']
  const dominioValido = dominiosValidos.some(dominio => login.endsWith(dominio))

  if (!dominioValido) {
    setError('Error correo o contraseña invalida')
    setLoading(false)
    return
  }

  try {
    const data = await loginRequest(login, password)
    setToken(data.access_token)
    const usuario = await getMeRequest(data.access_token)
    setUsuario(usuario)
    navigate('/dashboard')
  } catch (err) {
    setError('Credenciales incorrectas. Intenta de nuevo.')
  } finally {
    setLoading(false)
  }
}

  return (
    <div className={`${styles.container} ${isDark ? styles.dark : styles.light}`}>

      <TopBar />

      <button className={styles.themeBtn} onClick={toggleTheme}>
        {isDark ? '☀️' : '🌙'}
      </button>

      <div className={styles.card}>

        <div className={styles.header}>
          <div className={styles.logo}>🍽️</div>
          <h1 className={styles.title}>My Guest</h1>
          <p className={styles.subtitle}>Sistema de Gestión Gastronómica</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className={styles.field}>
            <label className={styles.label}>Correo institucional</label>
            <input
              type="email"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              placeholder="usuario@duoc.cl"
              required
              className={`${styles.input} ${isDark ? styles.inputDark : styles.inputLight}`}
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label}>Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              className={`${styles.input} ${isDark ? styles.inputDark : styles.inputLight}`}
            />
          </div>

          {error && (
            <div className={styles.error}>{error}</div>
          )}

          <button
            type="submit"
            disabled={loading}
            className={`${styles.submitBtn} ${loading ? styles.submitBtnLoading : ''}`}
          >
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>

        <p className={styles.footer}>DuocUC — Carrera de Gastronomía v2.0</p>
      </div>
    </div>
  )
}

export default LoginPage