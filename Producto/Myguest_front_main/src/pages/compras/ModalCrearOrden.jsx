import { useState, useEffect } from 'react';
import useAuthStore from '../../store/authStore';
import useThemeStore from '../../store/themeStore';
import { getProveedores, crearOrdenCompra } from '../../services/comprasService';
import styles from './ComprasPage.module.css';

export default function ModalCrearOrden({ onClose, onCreado }) {
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

  const [proveedores, setProveedores] = useState([]);
  const [loading, setLoading]         = useState(false);
  const [error, setError]             = useState('');
  const [form, setForm]               = useState({
    id_proveedor:  '',
    fecha_entrega: '',
    notas:         '',
  });

  useEffect(() => {
    getProveedores(token)
      .then(data => setProveedores(data))
      .catch(() => setError('Error al cargar proveedores'));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    if (!form.id_proveedor) {
      setError('Debes seleccionar un proveedor');
      return;
    }
    if (!form.fecha_entrega) {
      setError('La fecha de entrega es obligatoria');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const hoy = new Date().toISOString().slice(0, 10);
      await crearOrdenCompra(token, {
        id_proveedor:      parseInt(form.id_proveedor),
        fecha_emision:     hoy,
        fecha_entrega_est: form.fecha_entrega,
        id_usuario:        getIdUsuario(),
        obs:               form.notas || '',
        detalles:          [],
      });
      onCreado();
      onClose();
    } catch {
      setError('Error al crear la orden. Intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={`${styles.modalBox} ${t}`} onClick={e => e.stopPropagation()}>

        <div className={styles.modalHeader}>
          <h2 className={styles.modalTitulo}>Crear Orden de Compra</h2>
          <button className={styles.modalClose} onClick={onClose}>✕</button>
        </div>
        <p className={styles.modalSubtitulo}>
          Ingresa los datos para crear una nueva orden de compra.
        </p>

        {error && <div className={styles.errorMsg}>{error}</div>}

        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Proveedor</label>
          <select
            name="id_proveedor"
            className={`${styles.formSelect} ${t}`}
            value={form.id_proveedor}
            onChange={handleChange}
          >
            <option value="">Seleccionar proveedor</option>
            {proveedores.map(p => (
              <option key={p.id_proveedor} value={p.id_proveedor}>
                {p.nom_proveedor}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Fecha de Entrega</label>
          <input
            type="date"
            name="fecha_entrega"
            className={`${styles.formInput} ${t}`}
            value={form.fecha_entrega}
            onChange={handleChange}
          />
        </div>

        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Notas (opcional)</label>
          <textarea
            name="notas"
            className={`${styles.formTextarea} ${t}`}
            placeholder="Instrucciones especiales..."
            value={form.notas}
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
            {loading ? 'Creando...' : 'Crear Orden'}
          </button>
        </div>

      </div>
    </div>
  );
}