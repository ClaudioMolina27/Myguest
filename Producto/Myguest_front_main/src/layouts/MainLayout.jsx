import { useState } from 'react'
import TopBar from '../components/TopBar'
import Sidebar from '../components/Sidebar'
import useThemeStore from '../store/themeStore'
import styles from './MainLayout.module.css'

const MainLayout = ({ children }) => {
  const { isDark } = useThemeStore()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className={`${styles.container} ${isDark ? styles.dark : styles.light}`}>
      <TopBar onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
      <div className={styles.body}>
        <Sidebar isOpen={sidebarOpen} />
        <main className={`${styles.main} ${sidebarOpen ? styles.mainShifted : ''}`}>
          {children}
        </main>
      </div>
    </div>
  )
}

export default MainLayout