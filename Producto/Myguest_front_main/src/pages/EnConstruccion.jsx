import MainLayout from '../layouts/MainLayout'
import useThemeStore from '../store/themeStore'

const EnConstruccion = ({ titulo }) => {
  const { isDark } = useThemeStore()

  return (
    <MainLayout>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '60vh',
        gap: '16px'
      }}>
        <span style={{ fontSize: '64px' }}>🚧</span>
        <h2 style={{ color: isDark ? '#ffffff' : '#111827', margin: 0 }}>{titulo}</h2>
        <p style={{ color: '#6b7280', margin: 0 }}>Este módulo está en construcción</p>
      </div>
    </MainLayout>
  )
}

export default EnConstruccion