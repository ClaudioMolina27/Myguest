import { useState, useEffect } from 'react';
import useAuthStore from '../../store/authStore';
import useThemeStore from '../../store/themeStore';
import { crearDevolucion, getRegistrosTaller, getProductos } from '../../services/devolucionesService';
import styles from './DevolucionesPage.module.css';

export default function ModalCrearDevolucion({ onClose, onCreado }) {
  const { token } = useAuthStore();
  const { isDark } = useThemeStore();
  const t = isDark ? styles.dark : styles.light;

  const getIdUsuario = () => {
    try {
      return parseInt(JSON.parse(atob(token.split('.')[1])).sub);
    } catch { return null; }
  };

  const [registros, setRegistros]   = useState([]);
  const [productos, setProductos]   = useState([]);
  const [loading, setLoading]       = useState(false);
  const [error, setError]           = useState('');
  const [busquedaProd, setBusquedaProd] = useState('');
  const [productosAgregados, setProductosAgregados] = useState([]);
  const [registroSeleccionado, setRegistroSeleccionado] = useState(null);
  const [motivo, setMotivo]         = useState('');

  useEffect(() => {
    Promise.all([getRegistrosTaller(token), getProductos(token)])
      .then(([dataReg, dataProd]) => {
        setRegistros(dataReg);
        setProductos(dataProd);
      })
      .catch(() => setError('Error al cargar datos'));
  }, []);

  // Etiqueta legible para cada registro
  const getRegistroLabel = (r) => {
    const periodo = r.cod_periodo_academ === 1 ? '1SEM' : r.cod_periodo_academ === 2 ? '2SEM' : 'TAV';
    return `${r.sigla} — Sección ${r.seccion} — ${r.ano_academ} ${periodo} — ${r.fecha}`;
  };

  const handleSeleccionarRegistro = (e) => {
    const idx = e.target.value;
    if (idx === '') { setRegistroSeleccionado(null); return; }
    setRegistroSeleccionado(registros[parseInt(idx)]);
  };

  // Productos filtrados para autocomplete
  const productosFiltrados = busquedaProd
    ? productos
        .filter(p => p.nom_producto?.toLowerCase().includes(busquedaProd.toLowerCase()))
        .filter(p => !productosAgregados.find(pa => pa.id_producto === p.id_producto))
        .slice(0, 8)
    : [];

  const agregarProducto = (p) => {
    setProductosAgregados(prev => [...prev, {
      id_producto: p.id_producto,
      nombre: p.nom_producto,
      cantidad: 1,
    }]);
    setBusquedaProd('');
  };

  const quitarProducto = (id) => {
    setProductosAgregados(prev => prev.filter(p => p.id_producto !== id));
  };

  const actualizarCantidad = (id, cantidad) => {
    setProductosAgregados(prev =>
      prev.map(p => p.id_producto === id ? { ...p, cantidad: parseFloat(cantidad) || 0 } : p)
    );
  };

  const handleSubmit = async () => {
    if (!registroSeleccionado)           { setError('Debes seleccionar un registro de taller'); return; }
    if (!motivo)                         { setError('El motivo del sobrante es obligatorio'); return; }
    if (productosAgregados.length === 0) { setError('Debes agregar al menos un producto'); return; }
    if (productosAgregados.some(p => p.cantidad <= 0)) { setError('Todas las cantidades deben ser mayores a 0'); return; }

    setLoading(true);
    setError('');
    try {
      await crearDevolucion(token, {
        fecha:              registroSeleccionado.fecha,
        ano_academ:         registroSeleccionado.ano_academ,
        cod_periodo_academ: registroSeleccionado.cod_periodo_academ,
        sigla:              registroSeleccionado.sigla,
        seccion:            registroSeleccionado.seccion,
        id_taller:          registroSeleccionado.id_taller,
        id_usuario:         getIdUsuario(),
        motivo_sobrante:    motivo,
        detalles:           productosAgregados.map(p => ({
          id_producto: p.id_producto,
          cantidad:    p.cantidad,
        })),
      });
      onCreado();
      onClose();
    } catch {
      setError('Error al registrar la devolución. Intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={`${styles.modalBox} ${t}`} onClick={e => e.stopPropagation()}>

        <div className={styles.modalHeader}>
          <h2 className={styles.modalTitulo}>Registrar Devolución</h2>
          <button className={styles.modalClose} onClick={onClose}>✕</button>
        </div>
        <p className={styles.modalSubtitulo}>
          Selecciona un taller ejecutado y registra los insumos sobrantes.
        </p>

        {error && <div className={styles.errorMsg}>{error}</div>}

        {/* Selector de registro */}
        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Taller Ejecutado</label>
          <select
            className={`${styles.formSelect} ${t}`}
            onChange={handleSeleccionarRegistro}
            defaultValue=""
          >
            <option value="">Seleccionar taller ejecutado</option>
            {registros.map((r, idx) => (
              <option key={idx} value={idx}>
                {getRegistroLabel(r)}
              </option>
            ))}
          </select>
        </div>

        {/* Info del registro seleccionado */}
        {registroSeleccionado && (
          <div style={{
            background: isDark ? '#0f172a' : '#f0fdf4',
            border: '1px solid #22c55e',
            borderRadius: '8px',
            padding: '12px 16px',
            marginBottom: '16px',
            fontSize: '0.83rem',
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '8px',
          }}>
            <div><span style={{ color: '#6b7280' }}>Asignatura:</span> {registroSeleccionado.sigla}</div>
            <div><span style={{ color: '#6b7280' }}>Sección:</span> {registroSeleccionado.seccion}</div>
            <div><span style={{ color: '#6b7280' }}>Fecha:</span> {registroSeleccionado.fecha}</div>
            <div><span style={{ color: '#6b7280' }}>Taller ID:</span> {registroSeleccionado.id_taller}</div>
          </div>
        )}

        {/* Motivo */}
        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Motivo del sobrante</label>
          <textarea
            className={`${styles.formTextarea} ${t}`}
            placeholder="Ej: Sobraron ingredientes por baja asistencia..."
            value={motivo}
            onChange={e => setMotivo(e.target.value)}
          />
        </div>

        {/* Productos */}
        <div className={styles.formGroup}>
          <p className={styles.seccionTitulo}>Productos devueltos</p>

          {productosAgregados.length > 0 && (
            <div className={styles.productosLista}>
              {productosAgregados.map(p => (
                <div key={p.id_producto} className={`${styles.productoItem} ${t}`}>
                  <span className={styles.productoNombre}>{p.nombre}</span>
                  <input
                    type="number"
                    className={`${styles.productoCantidad} ${t}`}
                    value={p.cantidad}
                    min="0.1"
                    step="0.1"
                    onChange={e => actualizarCantidad(p.id_producto, e.target.value)}
                  />
                  <button
                    className={styles.btnQuitarProducto}
                    onClick={() => quitarProducto(p.id_producto)}
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          )}

          <input
            type="text"
            className={`${styles.formInput} ${t}`}
            placeholder="Buscar producto para agregar..."
            value={busquedaProd}
            onChange={e => setBusquedaProd(e.target.value)}
          />

          {busquedaProd && (
            <div className={styles.sugerencias}>
              {productosFiltrados.length === 0 ? (
                <div className={styles.sinResultados}>Sin resultados</div>
              ) : (
                productosFiltrados.map(p => (
                  <div
                    key={p.id_producto}
                    className={`${styles.sugerenciaItem} ${t}`}
                    onClick={() => agregarProducto(p)}
                  >
                    {p.nom_producto}
                  </div>
                ))
              )}
            </div>
          )}
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
            {loading ? 'Registrando...' : 'Registrar Devolución'}
          </button>
        </div>

      </div>
    </div>
  );
}