import { useState, useEffect } from 'react';
import useAuthStore from '../../store/authStore';
import useThemeStore from '../../store/themeStore';
import { getOrdenesCompra, getProveedores } from '../../services/comprasService';
import MainLayout from '../../layouts/MainLayout';
import styles from './ComprasPage.module.css';
import ModalCrearOrden from './ModalCrearOrden';
import ModalDetalleOrden from './ModalDetalleOrden';

const ESTADO_CONFIG = {
  borrador: { label: 'Borrador', clase: styles.badgePendiente },
  enviada: { label: 'Enviada', clase: styles.badgeEnviada },
  recibida: { label: 'Recibida', clase: styles.badgeRecibida },
  anulada: { label: 'Anulada', clase: styles.badgeAnulada },
};

export default function ComprasPage() {
  const { token } = useAuthStore();
  const { isDark } = useThemeStore();
  const t = isDark ? styles.dark : styles.light;

  const [ordenes, setOrdenes] = useState([]);
  const [proveedores, setProveedores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busqueda, setBusqueda] = useState('');
  const [filtroEstado, setFiltroEstado] = useState('todos');
  const [modalCrear, setModalCrear] = useState(false);
  const [ordenDetalle, setOrdenDetalle] = useState(null);

  const cargarOrdenes = async () => {
    setLoading(true);
    setError('');
    try {
      const [dataOrdenes, dataProveedores] = await Promise.all([
        getOrdenesCompra(token),
        getProveedores(token),
      ]);
      setProveedores(dataProveedores);
      setOrdenes(dataOrdenes);
    } catch {
      setError('Error al cargar las órdenes de compra. Verifica que el backend esté corriendo.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarOrdenes();
  }, []);

  const getNombreProveedor = (id_proveedor) => {
    const p = proveedores.find(p => p.id_proveedor === id_proveedor);
    return p ? p.nom_proveedor : '-';
  };

  const getRutProveedor = (id_proveedor) => {
    const p = proveedores.find(p => p.id_proveedor === id_proveedor);
    return p ? p.rut : '-';
  };

  const totalOrdenes = ordenes.length;
  const pendientes = ordenes.filter(o => o.estado === 'borrador' || o.estado === 'enviada').length;
  const recibidas = ordenes.filter(o => o.estado === 'recibida').length;
  const totalMes = ordenes.reduce((acc, o) => {
    const subtotal = o.detalles?.reduce((s, d) => s + (d.cantidad * d.precio_unitario), 0) || 0;
    return acc + subtotal;
  }, 0);

  const ordenesFiltradas = ordenes.filter(o => {
    const texto = busqueda.toLowerCase();
    const nombreProv = getNombreProveedor(o.id_proveedor).toLowerCase();
    const coincideTexto =
      `OC-${o.id_orden_compra}`.toLowerCase().includes(texto) ||
      nombreProv.includes(texto);
    const coincideEstado = filtroEstado === 'todos' || o.estado === filtroEstado;
    return coincideTexto && coincideEstado;
  });

  return (
    <MainLayout>
      <div className={styles.container}>

        <h1 className={styles.titulo}>Gestión de Compras</h1>
        <p className={styles.subtitulo}>Administra órdenes de compra y proveedores</p>

        <div className={styles.statsGrid}>
          <div className={`${styles.statCard} ${t}`}>
            <div className={`${styles.statIcon} ${styles.statIconVerde}`}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div>
              <p className={styles.statNumero}>{totalOrdenes}</p>
              <p className={styles.statLabel}>Total Órdenes</p>
            </div>
          </div>

          <div className={`${styles.statCard} ${t}`}>
            <div className={`${styles.statIcon} ${styles.statIconAmarillo}`}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" />
              </svg>
            </div>
            <div>
              <p className={styles.statNumero}>{pendientes}</p>
              <p className={styles.statLabel}>Pendientes</p>
            </div>
          </div>

          <div className={`${styles.statCard} ${t}`}>
            <div className={`${styles.statIcon} ${styles.statIconCian}`}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
            <div>
              <p className={styles.statNumero}>{recibidas}</p>
              <p className={styles.statLabel}>Recibidas</p>
            </div>
          </div>

          <div className={`${styles.statCard} ${t}`}>
            <div className={`${styles.statIcon} ${styles.statIconVerde}`}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="1" x2="12" y2="23" /><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" />
              </svg>
            </div>
            <div>
              <p className={styles.statNumero}>${totalMes.toLocaleString('es-CL')}</p>
              <p className={styles.statLabel}>Total Mes</p>
            </div>
          </div>
        </div>

        <div className={styles.toolbar}>
          <div className={styles.toolbarIzq}>
            <div className={styles.buscadorWrap}>
              <svg className={styles.buscadorIcon} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              <input
                type="text"
                className={`${styles.buscador} ${t}`}
                placeholder="Buscar por N° orden o proveedor..."
                value={busqueda}
                onChange={e => setBusqueda(e.target.value)}
              />
            </div>
            <select
              className={`${styles.filtroSelect} ${t}`}
              value={filtroEstado}
              onChange={e => setFiltroEstado(e.target.value)}
            >
              <option value="todos">Todos</option>
              <option value="borrador">Borrador</option>
              <option value="enviada">Enviada</option>
              <option value="recibida">Recibida</option>
              <option value="anulada">Anulada</option>
            </select>
          </div>
          <button className={styles.btnNueva} onClick={() => setModalCrear(true)}>
            + Nueva Orden
          </button>
        </div>

        {error && <div className={styles.errorMsg}>{error}</div>}

        <div className={`${styles.tablaWrap} ${t}`}>
          <table className={styles.tabla}>
            <thead>
              <tr className={t}>
                <th>N° Orden</th>
                <th>Proveedor</th>
                <th>RUT</th>
                <th>Fecha</th>
                <th>Entrega</th>
                <th>Ítems</th>
                <th>Total</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="9" className={styles.estadoTabla}>Cargando órdenes...</td></tr>
              ) : ordenesFiltradas.length === 0 ? (
                <tr><td colSpan="9" className={styles.estadoTabla}>No hay órdenes que mostrar</td></tr>
              ) : (
                ordenesFiltradas.map(o => {
                  const total = o.detalles?.reduce((s, d) => s + (d.cantidad * d.precio_unitario), 0) || 0;
                  const items = o.detalles?.length || 0;
                  const config = ESTADO_CONFIG[o.estado] || { label: o.estado, clase: '' };
                  return (
                    <tr key={o.id_orden_compra} className={t}>
                      <td className={styles.tdOrden}>OC-{String(o.id_orden_compra).padStart(3, '0')}</td>
                      <td>
                        <div className={styles.proveedorCell}>
                          🏢 {getNombreProveedor(o.id_proveedor)}
                        </div>
                      </td>
                      <td className={styles.tdRut}>{getRutProveedor(o.id_proveedor)}</td>
                      <td>{o.fecha_emision?.slice(0, 10) || '-'}</td>
                      <td>
                        <div className={styles.fechaCell}>
                          📅 {o.fecha_entrega_est || '-'}
                        </div>
                      </td>
                      <td>
                        <div className={styles.itemsCell}>
                          🔹 {items}
                        </div>
                      </td>
                      <td className={styles.tdTotal}>${total.toLocaleString('es-CL')}</td>
                      <td>
                        <span className={`${styles.badge} ${config.clase}`}>
                          {config.label}
                        </span>
                      </td>
                      <td>
                        <button
                          className={styles.btnVer}
                          onClick={() => setOrdenDetalle(o.id_orden_compra)}
                          title="Ver detalle"
                        >
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" />
                          </svg>
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {modalCrear && (
          <ModalCrearOrden
            onClose={() => setModalCrear(false)}
            onCreado={cargarOrdenes}
          />
        )}

        {ordenDetalle && (
          <ModalDetalleOrden
            idOrden={ordenDetalle}
            onClose={() => setOrdenDetalle(null)}
            onActualizado={cargarOrdenes}
          />
        )}

      </div>
    </MainLayout>
  );
}