<template>
  <div class="form-container">
    <div class="form-header">
      <div class="form-title-badge">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="title-icon">
          <path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
        </svg>
        <h3 class="form-title">{{ esEdicion ? 'Editar Registro' : 'Nuevo Gasto' }}</h3>
      </div>
      <p class="form-subtitle">
        {{ esEdicion ? 'Actualiza los detalles del gasto seleccionado' : 'Añade un nuevo desembolso a tu cuenta' }}
      </p>
    </div>

    <form @submit.prevent="enviarFormulario" class="gasto-form" novalidate>
      <!-- Big Premium Amount Input -->
      <div class="form-group amount-group">
        <label for="importe" class="form-label">Importe del Gasto <span class="required">*</span></label>
        <div class="input-wrapper amount-wrapper">
          <span class="amount-currency">€</span>
          <input 
            type="number" 
            id="importe" 
            v-model.number="form.importe" 
            step="0.01" 
            min="0.01" 
            placeholder="0.00" 
            required 
            class="amount-input"
          />
        </div>
        <p v-if="errores.importe" class="input-error">{{ errores.importe }}</p>
      </div>

      <!-- Description Field -->
      <div class="form-group">
        <label for="descripcion" class="form-label">Concepto / Descripción <span class="required">*</span></label>
        <div class="input-wrapper">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="field-icon">
            <path d="M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>
          </svg>
          <input 
            type="text" 
            id="descripcion" 
            v-model.trim="form.descripcion" 
            placeholder="Ej. Grapadora, comida..." 
            required 
            maxlength="40"
            class="form-input prefix-padding"
          />
        </div>
        <p v-if="errores.descripcion" class="input-error">{{ errores.descripcion }}</p>
      </div>

      <!-- Grid 2 Columns for Category and Date -->
      <div class="form-grid-2">
        <!-- Categoría Selector Customizado -->
        <div class="form-group custom-select-container" ref="selectContainer">
          <label class="form-label">Categoría <span class="required">*</span></label>
          <div class="custom-select-trigger" @click="toggleDropdown" :class="{ 'is-active': dropdownOpen }">
            <span v-if="form.categoria" class="selected-text">{{ form.categoria }}</span>
            <span v-else class="placeholder-text">Categoría...</span>
            <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" class="chevron-icon"><path d="m6 8 4 4 4-4" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <div v-if="dropdownOpen" class="custom-select-dropdown">
            <div class="select-search-wrapper" @click.stop>
              <input 
                type="text" 
                v-model="filtroBusquedaSelect" 
                placeholder="Buscar categoría..." 
                class="select-search-input"
              />
            </div>
            <div 
              v-for="cat in categoriasFiltradasSelect" 
              :key="cat" 
              class="custom-select-option" 
              :class="{ 'is-selected': form.categoria === cat }"
              @click="selectCategory(cat)"
            >
              {{ cat }}
            </div>
            <div v-if="categoriasFiltradasSelect.length === 0" class="no-options-text">
              Sin coincidencias
            </div>
          </div>
          <p v-if="errores.categoria" class="input-error">{{ errores.categoria }}</p>
        </div>

        <!-- Fecha Selector Customizado -->
        <div class="form-group">
          <label class="form-label">Fecha <span class="required">*</span></label>
          <CustomDatePicker v-model="form.fecha" placeholder="dd/mm/aaaa" />
          <p v-if="errores.fecha" class="input-error">{{ errores.fecha }}</p>
        </div>
      </div>

      <!-- Actions Buttons -->
      <div class="form-actions">
        <button type="submit" class="btn btn-primary">
          <svg v-if="!esEdicion" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="btn-icon"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="btn-icon"><polyline points="20 6 9 17 4 12"></polyline></svg>
          {{ esEdicion ? 'Actualizar' : 'Guardar Gasto' }}
        </button>
        
        <button 
          v-if="esEdicion" 
          type="button" 
          @click="cancelarEdicion" 
          class="btn btn-secondary"
        >
          Cancelar
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import CustomDatePicker from './CustomDatePicker.vue'

const props = defineProps({
  gastoAEditar: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancelEdit'])

// Default initial state
const obtenerFechaHoy = () => {
  const hoy = new Date()
  const yyyy = hoy.getFullYear()
  const mm = String(hoy.getMonth() + 1).padStart(2, '0')
  const dd = String(hoy.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

const estadoInicial = () => ({
  id: null,
  importe: null,
  categoria: '',
  descripcion: '',
  fecha: obtenerFechaHoy()
})

const form = ref(estadoInicial())
const errores = ref({})

// Predefined categories
const categoriasEstaticas = ref([
  'Comida',
  'Transporte',
  'Ocio',
  'Oficina',
  'Otros'
])

// Dynamically include any custom category from editing gasto
const listaCategorias = computed(() => {
  const copia = [...categoriasEstaticas.value]
  if (props.gastoAEditar && props.gastoAEditar.categoria) {
    if (!copia.includes(props.gastoAEditar.categoria)) {
      copia.unshift(props.gastoAEditar.categoria)
    }
  }
  return copia
})

// Custom Select Dropdown State & Methods
const dropdownOpen = ref(false)
const selectContainer = ref(null)
const filtroBusquedaSelect = ref('')

const categoriasFiltradasSelect = computed(() => {
  const query = filtroBusquedaSelect.value.toLowerCase().trim()
  if (!query) return listaCategorias.value
  return listaCategorias.value.filter(cat => cat.toLowerCase().includes(query))
})

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
  if (dropdownOpen.value) {
    filtroBusquedaSelect.value = ''
  }
}

const selectCategory = (cat) => {
  form.value.categoria = cat
  dropdownOpen.value = false
}

const clickOutsideHandler = (event) => {
  if (selectContainer.value && !selectContainer.value.contains(event.target)) {
    dropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', clickOutsideHandler)
})

onUnmounted(() => {
  document.removeEventListener('click', clickOutsideHandler)
})



const esEdicion = computed(() => !!props.gastoAEditar)

// React to editing changes
watch(
  () => props.gastoAEditar,
  (nuevoGasto) => {
    if (nuevoGasto) {
      form.value = { ...nuevoGasto }
    } else {
      form.value = estadoInicial()
    }
    errores.value = {}
  },
  { immediate: true }
)

// Validate inputs client-side
const validarFormulario = () => {
  const err = {}
  if (!form.value.importe || form.value.importe <= 0) {
    err.importe = 'El importe ingresado debe ser superior a 0 €.'
  }
  if (!form.value.categoria) {
    err.categoria = 'Por favor, selecciona una categoría para el gasto.'
  }
  if (!form.value.descripcion || form.value.descripcion.trim().length === 0) {
    err.descripcion = 'La descripción o concepto es obligatoria.'
  } else if (form.value.descripcion.length > 40) {
    err.descripcion = 'La descripción no puede superar los 40 caracteres.'
  }
  if (!form.value.fecha) {
    err.fecha = 'Por favor, selecciona una fecha válida.'
  }
  errores.value = err
  return Object.keys(err).length === 0
}

const enviarFormulario = () => {
  if (validarFormulario()) {
    emit('submit', { ...form.value })
    if (!esEdicion.value) {
      form.value = estadoInicial()
    }
  }
}

const cancelarEdicion = () => {
  emit('cancelEdit')
}
</script>

<style scoped>
.form-container {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.75rem;
  box-shadow: var(--shadow-md);
  position: relative;
}

.form-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: var(--primary);
  border-top-left-radius: var(--radius-md);
  border-top-right-radius: var(--radius-md);
}

.form-header {
  margin-bottom: 1.5rem;
}

.form-title-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.title-icon {
  width: 1.1rem;
  height: 1.1rem;
  color: var(--primary);
}

.form-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.form-subtitle {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.gasto-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 480px) {
  .form-grid-2 {
    grid-template-columns: 1fr;
  }
}

/* Amount Input Specific Styling */
.amount-group {
  background-color: rgba(18, 19, 22, 0.4);
  padding: 1rem;
  border-radius: var(--radius-md);
  border: 1px dashed var(--border-color);
  transition: var(--transition);
}

.amount-group:focus-within {
  border-color: var(--primary);
  background-color: rgba(18, 19, 22, 0.6);
}

.amount-wrapper {
  display: flex;
  align-items: baseline;
  position: relative;
}

.amount-currency {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--primary);
  margin-right: 0.5rem;
  user-select: none;
}

.amount-input {
  width: 100%;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 2rem;
  font-weight: 700;
  outline: none;
  font-family: var(--font-sans);
  padding: 0;
  -moz-appearance: textfield;
}

.amount-input::placeholder {
  color: var(--border-color);
}

.amount-input::-webkit-outer-spin-button,
.amount-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Input Fields & Icons styling */
.field-icon {
  position: absolute;
  left: 0.85rem;
  width: 1rem;
  height: 1rem;
  color: var(--text-secondary);
  pointer-events: none;
  transition: var(--transition);
}

.prefix-padding {
  padding-left: 2.2rem;
}

.input-wrapper:focus-within .field-icon {
  color: var(--primary);
}

/* Buttons style */
.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.btn-primary {
  flex: 1;
}

.btn-icon {
  width: 0.95rem;
  height: 0.95rem;
}
</style>
