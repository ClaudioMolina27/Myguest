import styles from './TopBar.module.css'
import useThemeStore from '../store/themeStore'

const TopBar = () => {
  const { isDark } = useThemeStore()

  return (
    <div className={`${styles.topbar} ${isDark ? styles.dark : styles.light}`}>
      <div className={styles.left}>
        <div className={styles.duocLogo}>
          <span className={styles.duocText}>Duoc</span>
          <span className={styles.ucText}>UC</span>
        </div>
        <span className={styles.separator}>|</span>
        <span className={styles.carrera}>Carrera de Gastronomía</span>
      </div>
    </div>
  )
}

export default TopBar