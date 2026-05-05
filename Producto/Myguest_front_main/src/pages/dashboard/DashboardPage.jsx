import MainLayout from '../../layouts/MainLayout'
import useThemeStore from '../../store/themeStore'
import styles from './DashboardPage.module.css'

const DashboardPage = () => {
  const { isDark } = useThemeStore()

  return (
    <MainLayout>
      <div className={styles.container}>
        <div className={styles.header}>
          <h1 className={`${styles.title} ${isDark ? styles.dark : styles.light}`}>Dashboard</h1>
          <p className={styles.subtitle}>Vista general del sistema</p>
        </div>
      </div>
    </MainLayout>
  )
}

export default DashboardPage