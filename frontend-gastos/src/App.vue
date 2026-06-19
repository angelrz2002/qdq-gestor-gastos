<template>
  <div class="app-container">
    <!-- Toast Notification for Feedback -->
    <Transition name="toast">
      <div v-if="notificacion.mensaje" :class="['toast-alert', notificacion.tipo]">
        <div class="toast-icon">
          <svg v-if="notificacion.tipo === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        </div>
        <span class="toast-text">{{ notificacion.mensaje }}</span>
      </div>
    </Transition>

    <!-- Header Section -->
    <header class="app-header">
      <div class="header-content">
        <div class="brand">
          <div class="brand-container" style="display: flex; align-items: center; gap: 12px;">
            <img :src="brandLogo" alt="qdq" class="brand-logo" style="height: 40px; width: auto; display: block; filter: invert(1); mix-blend-mode: screen;" />
            <span style="font-weight: 400; font-size: 1.1rem; color: #F8FAFC; letter-spacing: 0.5px;">| Control de Gastos</span>
          </div>
        </div>

        <!-- Premium Add Expense Button in Header -->
        <button class="btn-header-add" @click="abrirFormularioNuevo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="header-add-icon"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          <span>Añadir Gasto</span>
        </button>
      </div>
    </header>

    <!-- Main Content Grid -->
    <main class="app-main">
      <!-- Error State Banner -->
      <div v-if="error" class="error-banner">
        <div class="error-banner-content">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-banner-icon"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          <span>Error de conexión: {{ error }}. Por favor, verifica el backend.</span>
          <button @click="obtenerGastos()" class="btn-retry">Reintentar</button>
        </div>
      </div>

      <div class="dashboard-grid">
        <!-- Sidebar: Summary -->
        <div class="dashboard-sidebar">
          <ExpenseSummary :gastos="gastos" />
        </div>

        <!-- Main Column: List and Filters -->
        <div class="dashboard-content">
          <ExpenseList 
            :gastos="gastos" 
            :cargando="cargando"
            @edit="cargarGastoParaEdicion" 
            @delete="solicitarConfirmacionEliminar"
            @filtrar="obtenerGastos"
          />
        </div>
      </div>

      <!-- Modal Form Container -->
      <Transition name="modal-fade">
        <div v-if="mostrarFormularioModal || gastoParaEditar" class="modal-backdrop" @click.self="cancelarEdicionYModal">
          <div class="modal-content-wrapper">
            <button class="modal-close-btn" @click="cancelarEdicionYModal" title="Cerrar ventana">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
            <ExpenseForm 
              :gastoAEditar="gastoParaEditar" 
              @submit="guardarGastoYModal" 
              @cancelEdit="cancelarEdicionYModal" 
            />
          </div>
        </div>
      </Transition>

      <!-- Modal Confirm Delete -->
      <Transition name="modal-fade">
        <div v-if="confirmModal.isOpen" class="modal-backdrop" @click.self="cancelarEliminacion">
          <div class="confirm-modal-wrapper">
            <div class="confirm-modal-header">
              <div class="confirm-icon-circle">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
              </div>
              <h3>Confirmar Eliminación</h3>
            </div>
            <p class="confirm-modal-message">{{ confirmModal.message }}</p>
            <div class="confirm-modal-actions">
              <button type="button" class="btn btn-secondary" @click="cancelarEliminacion">Cancelar</button>
              <button type="button" class="btn btn-danger" @click="confirmarEliminacion">Eliminar</button>
            </div>
          </div>
        </div>
      </Transition>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import brandLogo from './assets/brand-logo.png'
import ExpenseSummary from './components/ExpenseSummary.vue'
import ExpenseForm from './components/ExpenseForm.vue'
import ExpenseList from './components/ExpenseList.vue'

const API_URL = 'http://localhost:8000/api/gastos'

// Reactive States
const gastos = ref([])
const cargando = ref(false)
const error = ref(null)
const gastoParaEditar = ref(null)

const confirmModal = ref({
  isOpen: false,
  id: null,
  message: '¿Estás seguro de que deseas eliminar este gasto de forma permanente?'
})

const notificacion = ref({
  mensaje: '',
  tipo: 'success'
})

// Trigger Toast Notifications
const mostrarNotificacion = (mensaje, tipo = 'success') => {
  notificacion.value.mensaje = mensaje
  notificacion.value.tipo = tipo
  setTimeout(() => {
    notificacion.value.mensaje = ''
  }, 4000)
}

// Fetch Expenses from API
const obtenerGastos = async (filtros = {}) => {
  cargando.value = true
  error.value = null
  try {
    const params = new URLSearchParams()
    if (filtros.categoria) params.append('categoria', filtros.categoria)
    if (filtros.fecha_inicio) params.append('fecha_inicio', filtros.fecha_inicio)
    if (filtros.fecha_fin) params.append('fecha_fin', filtros.fecha_fin)

    const url = params.toString() ? `${API_URL}?${params.toString()}` : API_URL
    const response = await fetch(url)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Error al obtener los gastos')
    }
    
    gastos.value = await response.json()
  } catch (err) {
    error.value = err.message
    mostrarNotificacion('Error al cargar la información de gastos', 'error')
  } finally {
    cargando.value = false
  }
}

// Save Gasto (Create or Update)
const guardarGasto = async (gastoData) => {
  cargando.value = true
  error.value = null
  const esEdicion = !!gastoData.id
  const url = esEdicion ? `${API_URL}/${gastoData.id}` : API_URL
  const method = esEdicion ? 'PUT' : 'POST'

  try {
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(gastoData)
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Error al procesar la solicitud')
    }

    const gastoProcesado = await response.json()

    if (esEdicion) {
      const index = gastos.value.findIndex(g => g.id === gastoProcesado.id)
      if (index !== -1) {
        gastos.value[index] = gastoProcesado
      }
      mostrarNotificacion('Gasto actualizado correctamente', 'success')
      gastoParaEditar.value = null
    } else {
      gastos.value.unshift(gastoProcesado)
      mostrarNotificacion('Gasto guardado correctamente', 'success')
    }
  } catch (err) {
    error.value = err.message
    mostrarNotificacion(`No se pudo guardar el gasto: ${err.message}`, 'error')
  } finally {
    cargando.value = false
  }
}

// Delete Gasto
const solicitarConfirmacionEliminar = (id) => {
  confirmModal.value.id = id
  confirmModal.value.isOpen = true
}

const confirmarEliminacion = async () => {
  const id = confirmModal.value.id
  confirmModal.value.isOpen = false
  if (!id) return

  cargando.value = true
  error.value = null
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'DELETE'
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Error al eliminar el gasto')
    }

    // Update state immediately
    gastos.value = gastos.value.filter(g => g.id !== id)
    mostrarNotificacion('Gasto eliminado correctamente', 'success')
    
    // Reset edit state if deleted expense was being edited
    if (gastoParaEditar.value && gastoParaEditar.value.id === id) {
      gastoParaEditar.value = null
    }
  } catch (err) {
    error.value = err.message
    mostrarNotificacion('Error al intentar borrar el gasto', 'error')
  } finally {
    cargando.value = false
    confirmModal.value.id = null
  }
}

const cancelarEliminacion = () => {
  confirmModal.value.isOpen = false
  confirmModal.value.id = null
}

// Edit Management
const mostrarFormularioModal = ref(false)

const abrirFormularioNuevo = () => {
  gastoParaEditar.value = null
  mostrarFormularioModal.value = true
}

const cargarGastoParaEdicion = (gasto) => {
  gastoParaEditar.value = { ...gasto }
  mostrarFormularioModal.value = true
}

const cancelarEdicionYModal = () => {
  gastoParaEditar.value = null
  mostrarFormularioModal.value = false
}

const guardarGastoYModal = async (gastoData) => {
  await guardarGasto(gastoData)
  mostrarFormularioModal.value = false
}

// Initial Load
onMounted(() => {
  obtenerGastos()
})
</script>

<style>


.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header Styling */
.app-header {
  background-color: var(--bg-card);
  border-bottom: 1px solid var(--border-color);
  padding: 1.25rem 2rem;
  position: sticky;
  top: 0;
  z-index: 50;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Main Layout Grid */
.app-main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
}

.error-banner {
  background-color: var(--danger-light);
  border: 1px solid #7F1D1D;
  color: #FCA5A5;
  border-radius: var(--radius-md);
  padding: 1rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.error-banner-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.error-banner-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

.btn-retry {
  margin-left: auto;
  background-color: var(--danger);
  color: white;
  border: none;
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.btn-retry:hover {
  background-color: #B91C1C;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 2rem;
  align-items: start;
}

@media (max-width: 968px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

/* Modal Backdrop with Glassmorphism Blur */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(10, 11, 14, 0.75);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content-wrapper {
  position: relative;
  width: 100%;
  max-width: 460px;
  animation: modalScaleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes modalScaleUp {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-close-btn {
  position: absolute;
  top: 1rem;
  right: 1.2rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
  z-index: 80;
}

.modal-close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
  transform: rotate(90deg);
}

.modal-close-btn svg {
  width: 1rem;
  height: 1rem;
}

/* Header Add Button */
.btn-header-add {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--primary);
  color: white;
  border: none;
  font-family: var(--font-sans);
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.55rem 1.1rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition);
  box-shadow: 0 4px 12px rgba(0, 168, 89, 0.2);
}

.btn-header-add:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 168, 89, 0.3);
}

.header-add-icon {
  width: 1rem;
  height: 1rem;
}

/* Transition Animations for Modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}


</style>
