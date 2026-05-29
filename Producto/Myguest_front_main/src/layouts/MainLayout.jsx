import { useState, useEffect } from 'react'
import TopBar from '../components/TopBar'
import Sidebar from '../components/Sidebar'
import useThemeStore from '../store/themeStore'
import styles from './MainLayout.module.css'

const MainLayout = ({ children }) => {
  const { isDark } = useThemeStore()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  // En móvil/tablet el sidebar arranca cerrado
  useEffect(() => {
    if (window.innerWidth <= 1024) {
      setSidebarOpen(false)
    }
  }, [])

  const handleToggle = () => setSidebarOpen(!sidebarOpen)
  const handleClose  = () => setSidebarOpen(false)

  // En desktop el contenido se desplaza, en tablet/móvil no
  const isDesktop = window.innerWidth > 1024

  return (
    <div className={`${styles.container} ${isDark ? styles.dark : styles.light}`}>
      <TopBar onToggleSidebar={handleToggle} />
      <div className={styles.body}>
        <Sidebar isOpen={sidebarOpen} onClose={handleClose} />
        <main className={`${styles.main} ${sidebarOpen && isDesktop ? styles.mainShifted : ''}`}>
          {children}
        </main>
      </div>
    </div>
  )
}

export default MainLayout