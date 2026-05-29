import { useState, useEffect } from 'react';
import useAuthStore from '../../store/authStore';
import useThemeStore from '../../store/themeStore';
import { getOrdenCompra, actualizarEstadoOrden, eliminarOrdenCompra } from '../../services/comprasService';
import styles from './ComprasPage.module.css';

const ESTADO_CONFIG = {
  borrador: { label: 'Borrador',  clase: styles.badgePendiente },
  enviada:  { label: 'Enviada',   clase: styles.badgeEnviada   },
  recibida: { label: 'Recibida',  clase: styles.badgeRecibida  },
  anulada:  { label: 'Anulada',   clase: styles.badgeAnulada   },
};

const ESTADOS = ['borrador', 'enviada', 'recibida', 'anulada'];

export default function ModalDetalleOrden({ idOrden, onClose, onActualizado }) {
  const { token } = useAuthStore();
  const { isDark } = useThemeStore();
  const t = isDark ? styles.dark : styles.light;

  const [orden, setOrden]               = useState(null);
  const [loading, setLoading]           = useState(true);
  const [error, setError]               = useState('');
  const [cambiandoEstado, setCambiando] = useState(false);
  const [confirmEliminar, setConfirmEliminar] = useState(false);
  const [eliminando, setEliminando]     = useState(false);

  useEffect(() => {
    getOrdenCompra(token, idOrden)
      .then(data => setOrden(data))
      .catch(() => setError('Error al cargar el detalle de la orden'))
      .finally(() => setLoading(false));
  }, [idOrden]);

  const handleCambiarEstado = async (nuevoEstado) => {
    setCambiando(true);
    try {
      await actualizarEstadoOrden(token, idOrden, { estado: nuevoEstado });
      setOrden({ ...orden, estado: nuevoEstado });
      onActualizado();
    } catch {
      setError('Error al cambiar el estado');
    } finally {
      setCambiando(false);
    }
  };

  const handleEliminar = async () => {
    setEliminando(true);
    try {
      await eliminarOrdenCompra(token, idOrden);
      onActualizado();
      onClose();
    } catch {
      setError('Error al eliminar la orden');
      setConfirmEliminar(false);
    } finally {
      setEliminando(false);
    }
  };

  const total = orden?.detalles?.reduce(
    (s, d) => s + (d.cantidad * d.precio_unitario), 0
  ) || 0;

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div
        className={`${styles.modalBox} ${t}`}
        style={{ maxWidth: '580px' }}
        onClick={e => e.stopPropagation()}
      >
        <div className={styles.modalHeader}>
          <h2 className={styles.modalTitulo}>Detalle de Orden</h2>
          <button className={styles.modalClose} onClick={onClose}>✕</button>
        </div>

        {loading && <p style={{ color: '#6b7280', fontSize: '0.85rem' }}>Cargando...</p>}
        {error   && <div className={styles.errorMsg}>{error}</div>}

        {orden && (
          <>
            <div className={styles.detalleGrid}>
              <div className={styles.detalleItem}>
                <span className={styles.detalleLabel}>N° Orden</span>
                <span className={styles.detalleValor}>
                  OC-{String(orden.id_orden_compra).padStart(3, '0')}
                </span>
              </div>
              <div className={styles.detalleItem}>
                <span className={styles.detalleLabel}>Estado</span>
                <span className={`${styles.badge} ${ESTADO_CONFIG[orden.estado]?.clase}`}>
                  {ESTADO_CONFIG[orden.estado]?.label}
                </span>
              </div>
              <div className={styles.detalleItem}>
                <span className={styles.detalleLabel}>Fecha Emisión</span>
                <span className={styles.detalleValor}>{orden.fecha_emision?.slice(0, 10) || '-'}</span>
              </div>
              <div className={styles.detalleItem}>
                <span className={styles.detalleLabel}>Fecha Entrega</span>
                <span className={styles.detalleValor}>{orden.fecha_entrega_est || '-'}</span>
              </div>
              {orden.obs && (
                <div className={styles.detalleItem} style={{ gridColumn: '1 / -1' }}>
                  <span className={styles.detalleLabel}>Notas</span>
                  <span className={styles.detalleValor}>{orden.obs}</span>
                </div>
              )}
            </div>

            {orden.detalles && orden.detalles.length > 0 && (
              <div className={styles.detalleTablaWrap}>
                <h3 className={styles.detalleSectionTitle}>Productos</h3>
                <table className={styles.tablaDetalle}>
                  <thead>
                    <tr>
                      <th>Producto</th>
                      <th>Cantidad</th>
                      <th>Precio Unit.</th>
                      <th>Subtotal</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orden.detalles.map((item, i) => (
                      <tr key={i}>
                        <td>{item.nombre_producto || item.id_producto}</td>
                        <td>{item.cantidad}</td>
                        <td>${item.precio_unitario?.toLocaleString('es-CL')}</td>
                        <td>${(item.cantidad * item.precio_unitario).toLocaleString('es-CL')}</td>
                      </tr>
                    ))}
                    <tr>
                      <td colSpan="3" style={{ textAlign: 'right', fontWeight: 600, paddingTop: '12px' }}>
                        Total
                      </td>
                      <td style={{ fontWeight: 700, color: '#22c55e', paddingTop: '12px' }}>
                        ${total.toLocaleString('es-CL')}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            )}

            <div className={styles.cambiarEstadoWrap}>
              <span className={styles.detalleLabel}>Cambiar estado:</span>
              <div className={styles.estadoBtns}>
                {ESTADOS.map(e => (
                  <button
                    key={e}
                    className={`${styles.btnEstado} ${orden.estado === e ? styles.btnEstadoActivo : ''}`}
                    onClick={() => handleCambiarEstado(e)}
                    disabled={cambiandoEstado || orden.estado === e}
                  >
                    {ESTADO_CONFIG[e].label}
                  </button>
                ))}
              </div>
            </div>
          </>
        )}

        <div className={styles.modalFooter}>
          {!confirmEliminar ? (
            <>
              <button className={styles.btnEliminar} onClick={() => setConfirmEliminar(true)}>
                🗑️ Eliminar
              </button>
              <button className={styles.btnCancelar} onClick={onClose}>Cerrar</button>
            </>
          ) : (
            <>
              <span style={{ fontSize: '0.83rem', color: '#ef4444', marginRight: 'auto' }}>
                ¿Confirmas eliminar esta orden?
              </span>
              <button className={styles.btnCancelar} onClick={() => setConfirmEliminar(false)}>
                No
              </button>
              <button className={styles.btnEliminarConfirm} onClick={handleEliminar} disabled={eliminando}>
                {eliminando ? 'Eliminando...' : 'Sí, eliminar'}
              </button>
            </>
          )}
        </div>

      </div>
    </div>
  );
}