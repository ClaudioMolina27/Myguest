import { useState, useEffect } from 'react';
import useAuthStore from '../../store/authStore';
import useThemeStore from '../../store/themeStore';
import { crearMerma, getMotivos, getProductos } from '../../services/mermasService';
import styles from './MermasPage.module.css';

export default function ModalCrearMerma({ onClose, onCreado }) {
  const { token } = useAuthStore();
  const { isDark } = useThemeStore();
  const t = isDark ? styles.dark : styles.light;

  const getIdUsuario = () => {
    try {
      return parseInt(JSON.parse(atob(token.split('.')[1])).sub);
    } catch {
      return null;
    }
  };

  const [motivos, setMotivos]     = useState([]);
  const [productos, setProductos] = useState([]);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState('');
  const [busquedaProd, setBusquedaProd] = useState('');
  const [form, setForm] = useState({
    fecha:            '',
    id_producto:      '',
    cantidad:         '',
    cod_motivo_merma: '',
    obs:              '',
  });

  useEffect(() => {
    Promise.all([getMotivos(token), getProductos(token)])
      .then(([dataMotivos, dataProductos]) => {
        setMotivos(dataMotivos);
        setProductos(dataProductos);
      })
      .catch(() => setError('Error al cargar datos'));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Productos filtrados por búsqueda
  const productosFiltrados = productos.filter(p =>
    p.nom_producto?.toLowerCase().includes(busquedaProd.toLowerCase())
  ).slice(0, 8);

  const handleSubmit = async () => {
    if (!form.id_producto) { setError('Debes seleccionar un producto'); return; }
    if (!form.cantidad || parseFloat(form.cantidad) <= 0) { setError('La cantidad debe ser mayor a 0'); return; }
    if (!form.cod_motivo_merma) { setError('Debes seleccionar un motivo'); return; }
    if (!form.fecha) { setError('La fecha es obligatoria'); return; }

    setLoading(true);
    setError('');
    try {
      await crearMerma(token, {
        fecha:            form.fecha,
        id_producto:      parseInt(form.id_producto),
        cantidad:         parseFloat(form.cantidad),
        cod_motivo_merma: parseInt(form.cod_motivo_merma),
        id_usuario:       getIdUsuario(),
        obs:              form.obs || null,
        url_foto:         null,
      });
      onCreado();
      onClose();
    } catch {
      setError('Error al registrar la merma. Intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={`${styles.modalBox} ${t}`} onClick={e => e.stopPropagation()}>

        <div className={styles.modalHeader}>
          <h2 className={styles.modalTitulo}>Registrar Merma</h2>
          <button className={styles.modalClose} onClick={onClose}>✕</button>
        </div>
        <p className={styles.modalSubtitulo}>
          Registra un producto dado de baja por pérdida o daño.
        </p>

        {error && <div className={styles.errorMsg}>{error}</div>}

        {/* Búsqueda de producto */}
        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Buscar Producto</label>
          <input
            type="text"
            className={`${styles.formInput} ${t}`}
            placeholder="Escribe el nombre del producto..."
            value={busquedaProd}
            onChange={e => {
              setBusquedaProd(e.target.value);
              setForm({ ...form, id_producto: '' });
            }}
          />
          {busquedaProd && !form.id_producto && (
            <div style={{
              border: '1px solid #374151',
              borderRadius: '8px',
              marginTop: '4px',
              overflow: 'hidden',
              maxHeight: '200px',
              overflowY: 'auto',
            }}>
              {productosFiltrados.length === 0 ? (
                <div style={{ padding: '10px 12px', color: '#6b7280', fontSize: '0.83rem' }}>
                  Sin resultados
                </div>
              ) : (
                productosFiltrados.map(p => (
                  <div
                    key={p.id_producto}
                    onClick={() => {
                      setForm({ ...form, id_producto: p.id_producto });
                      setBusquedaProd(p.nom_producto);
                    }}
                    style={{
                      padding: '10px 12px',
                      cursor: 'pointer',
                      fontSize: '0.85rem',
                      borderBottom: '1px solid #1f2937',
                      background: isDark ? '#111827' : '#ffffff',
                      color: isDark ? '#f9fafb' : '#111827',
                    }}
                    onMouseEnter={e => e.currentTarget.style.background = isDark ? '#1f2937' : '#f9fafb'}
                    onMouseLeave={e => e.currentTarget.style.background = isDark ? '#111827' : '#ffffff'}
                  >
                    {p.nom_producto}
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Cantidad</label>
          <input
            type="number"
            name="cantidad"
            className={`${styles.formInput} ${t}`}
            placeholder="Ej: 2.5"
            min="0"
            step="0.1"
            value={form.cantidad}
            onChange={handleChange}
          />
        </div>

        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Motivo</label>
          <select
            name="cod_motivo_merma"
            className={`${styles.formSelect} ${t}`}
            value={form.cod_motivo_merma}
            onChange={handleChange}
          >
            <option value="">Seleccionar motivo</option>
            {motivos.map(m => (
              <option key={m.cod_motivo_merma} value={m.cod_motivo_merma}>
                {m.nom_motivo_merma}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Fecha</label>
          <input
            type="date"
            name="fecha"
            className={`${styles.formInput} ${t}`}
            value={form.fecha}
            onChange={handleChange}
          />
        </div>

        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Observación (opcional)</label>
          <textarea
            name="obs"
            className={`${styles.formTextarea} ${t}`}
            placeholder="Detalle adicional..."
            value={form.obs}
            onChange={handleChange}
          />
        </div>

        <div className={styles.modalFooter}>
          <button className={styles.btnCancelar} onClick={onClose}>
            Cancelar
          </button>
          <button
            className={styles.btnConfirmar}
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? 'Registrando...' : 'Registrar Merma'}
          </button>
        </div>

      </div>
    </div>
  );
}