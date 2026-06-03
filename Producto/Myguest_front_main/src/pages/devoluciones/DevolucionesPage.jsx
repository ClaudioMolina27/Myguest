import { useState, useEffect } from 'react';
import useAuthStore from '../../store/authStore';
import useThemeStore from '../../store/themeStore';
import { getDevoluciones, eliminarDevolucion, getProductos } from '../../services/devolucionesService';
import MainLayout from '../../layouts/MainLayout';
import ModalCrearDevolucion from './ModalCrearDevolucion';
import styles from './DevolucionesPage.module.css';

export default function DevolucionesPage() {
  const { token } = useAuthStore();
  const { isDark } = useThemeStore();
  const t = isDark ? styles.dark : styles.light;

  const [devoluciones, setDevoluciones] = useState([]);
  const [productos, setProductos]       = useState([]);
  const [loading, setLoading]           = useState(true);
  const [error, setError]               = useState('');
  const [busqueda, setBusqueda]         = useState('');
  const [modalCrear, setModalCrear]     = useState(false);
  const [confirmEliminar, setConfirmEliminar] = useState(null);

  const cargarDatos = async () => {
    setLoading(true);
    setError('');
    try {
      const [dataDev, dataProd] = await Promise.all([
        getDevoluciones(token),
        getProductos(token),
      ]);
      setDevoluciones(dataDev);
      setProductos(dataProd);
    } catch {
      setError('Error al cargar las devoluciones. Verifica que el backend esté corriendo.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  const getNombreProducto = (id) => {
    const p = productos.find(p => p.id_producto === id);
    return p ? p.nom_producto : `Producto #${id}`;
  };

  // Stats
  const totalDevoluciones  = devoluciones.length;
  const totalProductos     = devoluciones.reduce((acc, d) => acc + (d.detalles?.length || 0), 0);
  const totalUnidades      = devoluciones.reduce((acc, d) => {
    return acc + (d.detalles?.reduce((s, det) => s + det.cantidad, 0) || 0);
  }, 0);

  // Filtros
  const devolucionesFiltradas = devoluciones.filter(d => {
    const texto = busqueda.toLowerCase();
    return (
      d.sigla?.toLowerCase().includes(texto) ||
      String(d.ano_academ).includes(texto) ||
      d.motivo_sobrante?.toLowerCase().includes(texto)
    );
  });

  const handleEliminar = async (id) => {
    try {
      await eliminarDevolucion(token, id);
      setConfirmEliminar(null);
      cargarDatos();
    } catch {
      setError('Error al eliminar la devolución');
    }
  };

  return (
    <MainLayout>
      <div className={styles.container}>

        <div className={styles.header}>
          <div>
            <h1 className={`${styles.titulo} ${t}`}>Devoluciones</h1>
            <p className={styles.subtitulo}>Registro de insumos sobrantes por taller</p>
          </div>
          <button className={styles.btnNueva} onClick={() => setModalCrear(true)}>
            + Registrar Devolución
          </button>
        </div>

        {/* Stats */}
        <div className={styles.statsGrid}>
          <div className={`${styles.statCard} ${t}`}>
            <div className={`${styles.statIcon} ${styles.statIconVerde}`}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.51"/>
              </svg>
            </div>
            <div>
              <p className={styles.statNumero}>{totalDevoluciones}</p>
              <p className={styles.statLabel}>Total Devoluciones</p>
            </div>
          </div>

          <div className={`${styles.statCard} ${t}`}>
            <div className={`${styles.statIcon} ${styles.statIconAzul}`}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
              </svg>
            </div>
            <div>
              <p className={styles.statNumero}>{totalProductos}</p>
              <p className={styles.statLabel}>Productos Distintos</p>
            </div>
          </div>

          <div className={`${styles.statCard} ${t}`}>
            <div className={`${styles.statIcon} ${styles.statIconAmarillo}`}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
              </svg>
            </div>
            <div>
              <p className={styles.statNumero}>{totalUnidades.toFixed(1)}</p>
              <p className={styles.statLabel}>Unidades Devueltas</p>
            </div>
          </div>
        </div>

        {/* Toolbar */}
        <div className={styles.toolbar}>
          <div className={styles.toolbarIzq}>
            <div className={styles.buscadorWrap}>
              <svg className={styles.buscadorIcon} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
              <input
                type="text"
                className={`${styles.buscador} ${t}`}
                placeholder="Buscar por asignatura, año o motivo..."
                value={busqueda}
                onChange={e => setBusqueda(e.target.value)}
              />
            </div>
          </div>
        </div>

        {error && <div className={styles.errorMsg}>{error}</div>}

        {/* Tabla */}
        <div className={`${styles.tablaWrap} ${t}`}>
          <table className={styles.tabla}>
            <thead>
              <tr className={t}>
                <th>Asignatura</th>
                <th>Año / Período</th>
                <th>Sección</th>
                <th>Fecha</th>
                <th>Productos</th>
                <th>Motivo</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="7" className={styles.estadoTabla}>Cargando devoluciones...</td></tr>
              ) : devolucionesFiltradas.length === 0 ? (
                <tr><td colSpan="7" className={styles.estadoTabla}>No hay devoluciones registradas</td></tr>
              ) : (
                devolucionesFiltradas.map(d => (
                  <tr key={d.id_devolucion} className={t}>
                    <td className={styles.tdAsignatura}>{d.sigla}</td>
                    <td>
                      <span className={styles.badge}>
                        {d.ano_academ} — {d.cod_periodo_academ === 1 ? '1SEM' : d.cod_periodo_academ === 2 ? '2SEM' : 'TAV'}
                      </span>
                    </td>
                    <td className={styles.tdSeccion}>Sección {d.seccion}</td>
                    <td>{d.fecha}</td>
                    <td>{d.detalles?.length || 0} ítem(s)</td>
                    <td style={{ maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {d.motivo_sobrante}
                    </td>
                    <td>
                      {confirmEliminar === d.id_devolucion ? (
                        <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                          <span style={{ fontSize: '0.75rem', color: '#ef4444' }}>¿Eliminar?</span>
                          <button
                            className={styles.btnConfirmar}
                            style={{ padding: '4px 10px', fontSize: '0.75rem' }}
                            onClick={() => handleEliminar(d.id_devolucion)}
                          >
                            Sí
                          </button>
                          <button
                            className={styles.btnCancelar}
                            style={{ padding: '4px 10px', fontSize: '0.75rem' }}
                            onClick={() => setConfirmEliminar(null)}
                          >
                            No
                          </button>
                        </div>
                      ) : (
                        <button
                          className={styles.btnEliminar}
                          onClick={() => setConfirmEliminar(d.id_devolucion)}
                          title="Eliminar"
                        >
                          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6m4-6v6"/><path d="M9 6V4h6v2"/>
                          </svg>
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {modalCrear && (
          <ModalCrearDevolucion
            onClose={() => setModalCrear(false)}
            onCreado={cargarDatos}
          />
        )}

      </div>
    </MainLayout>
  );
}