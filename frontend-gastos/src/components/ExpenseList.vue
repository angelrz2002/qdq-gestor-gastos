<template>
  <div class="list-container">
    <!-- Filters Header Section -->
    <div class="filters-panel">
      <div class="filters-header">
        <h3 class="panel-title">Filtros & Búsqueda</h3>
        <button 
          v-if="tieneFiltrosActivos" 
          @click="limpiarFiltros" 
          class="btn-clear"
        >
          Limpiar filtros
        </button>
      </div>

      <div class="filters-grid">
        <!-- Search Field (Client-side) -->
        <div class="filter-group col-span-3">
          <label for="search" class="filter-label">Buscar por descripción</label>
          <div class="search-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="search-icon"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input 
              type="text" 
              id="search" 
              v-model="filtroLocal.busqueda" 
              placeholder="Buscar gasto..." 
              class="form-input search-padding"
            />
          </div>
        </div>

        <!-- Category Filter Customizado (Backend) -->
        <div class="filter-group custom-select-container" ref="selectContainer">
          <label class="filter-label">Categoría</label>
          <div class="custom-select-trigger" @click="toggleDropdown" :class="{ 'is-active': dropdownOpen }">
            <span v-if="filtroLocal.categoria" class="selected-text">{{ filtroLocal.categoria }}</span>
            <span v-else class="placeholder-text">Todas las categorías</span>
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
              class="custom-select-option" 
              :class="{ 'is-selected': !filtroLocal.categoria }"
              @click="selectCategory('')"
            >
              Todas las categorías
            </div>
            <div 
              v-for="cat in categoriasFiltradasSelect" 
              :key="cat" 
              class="custom-select-option" 
              :class="{ 'is-selected': filtroLocal.categoria === cat }"
              @click="selectCategory(cat)"
            >
              {{ cat }}
            </div>
            <div v-if="categoriasFiltradasSelect.length === 0" class="no-options-text">
              Sin coincidencias
            </div>
          </div>
        </div>

        <!-- Date Start Filter (Backend) -->
        <div class="filter-group">
          <label class="filter-label">Desde</label>
          <CustomDatePicker 
            v-model="filtroLocal.fecha_inicio" 
            placeholder="dd/mm/aaaa"
            @update:modelValue="emitirFiltros" 
          />
        </div>

        <!-- Date End Filter (Backend) -->
        <div class="filter-group">
          <label class="filter-label">Hasta</label>
          <CustomDatePicker 
            v-model="filtroLocal.fecha_fin" 
            placeholder="dd/mm/aaaa"
            @update:modelValue="emitirFiltros" 
          />
        </div>
      </div>
    </div>

    <!-- Expenses Table / Card List Section -->
    <div class="list-content">
      <div v-if="cargando" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando información financiera...</p>
      </div>

      <div v-else-if="gastosFiltrados.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="empty-icon"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        <p class="empty-title">Sin registros encontrados</p>
        <p class="empty-desc">Prueba a cambiar los filtros o añade un nuevo gasto para comenzar.</p>
      </div>

      <div v-else class="table-responsive">
        <!-- Vista de tabla para pantallas grandes -->
        <table class="expenses-table desktop-only">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Descripción</th>
              <th>Categoría</th>
              <th class="text-right">Importe</th>
              <th class="text-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="gasto in gastosPaginados" 
              :key="gasto.id" 
              class="expense-row"
            >
              <td class="cell-date">{{ formatearFecha(gasto.fecha) }}</td>
              <td class="cell-description">
                <div class="desc-text" :title="gasto.descripcion">{{ gasto.descripcion }}</div>
              </td>
              <td class="cell-category">
                <span 
                  class="badge-category"
                  :style="{ 
                    '--bg-badge': obtenerColorCategoria(gasto.categoria) + '33',
                    '--color-badge': obtenerColorCategoria(gasto.categoria)
                  }"
                >
                  {{ gasto.categoria }}
                </span>
              </td>
              <td class="cell-amount text-right">{{ formatearMoneda(gasto.importe) }}</td>
              <td class="cell-actions text-center">
                <div class="actions-wrapper">
                  <button 
                    @click="$emit('edit', gasto)" 
                    class="btn-action edit" 
                    title="Editar registro"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="action-icon"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                  </button>
                  <button 
                    @click="$emit('delete', gasto.id)" 
                    class="btn-action delete" 
                    title="Eliminar registro"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="action-icon"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Vista de tarjetas para móviles -->
        <div class="mobile-card-list mobile-only">
          <div 
            v-for="gasto in gastosPaginados" 
            :key="gasto.id" 
            class="expense-mobile-card"
          >
            <div class="mobile-card-header">
              <span class="mobile-card-date">{{ formatearFecha(gasto.fecha) }}</span>
              <span 
                class="badge-category"
                :style="{ 
                  '--bg-badge': obtenerColorCategoria(gasto.categoria) + '33',
                  '--color-badge': obtenerColorCategoria(gasto.categoria)
                }"
              >
                {{ gasto.categoria }}
              </span>
            </div>
            <div class="mobile-card-body">
              <p class="mobile-card-description">{{ gasto.descripcion }}</p>
              <h4 class="mobile-card-amount">{{ formatearMoneda(gasto.importe) }}</h4>
            </div>
            <div class="mobile-card-actions">
              <button 
                @click="$emit('edit', gasto)" 
                class="btn-action-mobile edit" 
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="action-icon"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                <span>Editar</span>
              </button>
              <button 
                @click="$emit('delete', gasto.id)" 
                class="btn-action-mobile delete" 
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="action-icon"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                <span>Eliminar</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Paginador -->
      <div v-if="totalRegistros > 0" class="pagination-bar">
        <div class="pagination-info">
          Mostrando <span class="highlight">{{ indiceInicio }}-{{ indiceFin }}</span> de <span class="highlight">{{ totalRegistros }}</span> gastos
        </div>
        
        <div class="pagination-controls">
          <button 
            type="button" 
            class="pag-btn" 
            :disabled="paginaActual === 1" 
            @click="cambiarPagina(1)"
            title="Primera página"
          >
            &laquo;
          </button>
          <button 
            type="button" 
            class="pag-btn" 
            :disabled="paginaActual === 1" 
            @click="cambiarPagina(paginaActual - 1)"
            title="Anterior"
          >
            &lsaquo;
          </button>
          
          <button 
            v-for="pag in totalPaginas" 
            :key="pag" 
            type="button" 
            class="pag-btn page-num" 
            :class="{ 'is-active': paginaActual === pag }"
            @click="cambiarPagina(pag)"
          >
            {{ pag }}
          </button>
          
          <button 
            type="button" 
            class="pag-btn" 
            :disabled="paginaActual === totalPaginas" 
            @click="cambiarPagina(paginaActual + 1)"
            title="Siguiente"
          >
            &rsaquo;
          </button>
          <button 
            type="button" 
            class="pag-btn" 
            :disabled="paginaActual === totalPaginas" 
            @click="cambiarPagina(totalPaginas)"
            title="Última página"
          >
            &raquo;
          </button>
        </div>

        <div class="pagination-size" ref="pageSizeContainer">
          <span class="size-label">Por página:</span>
          <div class="custom-select-container mini-select">
            <div class="custom-select-trigger" @click="togglePageSizeDropdown" :class="{ 'is-active': pageSizeDropdownOpen }">
              <span class="selected-text">{{ elementosPorPagina }}</span>
              <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" class="chevron-icon"><path d="m6 8 4 4 4-4" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
            <div v-if="pageSizeDropdownOpen" class="custom-select-dropdown">
              <div 
                v-for="size in [5, 10, 20, 50]" 
                :key="size"
                class="custom-select-option"
                :class="{ 'is-selected': elementosPorPagina === size }"
                @click="selectPageSize(size)"
              >
                {{ size }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import CustomDatePicker from './CustomDatePicker.vue'

const props = defineProps({
  gastos: {
    type: Array,
    required: true
  },
  cargando: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['edit', 'delete', 'filtrar'])

// Local Filter States
const filtroLocal = ref({
  busqueda: '',
  categoria: '',
  fecha_inicio: '',
  fecha_fin: ''
})

// Pagination
const paginaActual = ref(1)
const elementosPorPagina = ref(10)

// Reset page to 1 when filters or search terms change
watch(
  () => [filtroLocal.value.busqueda, filtroLocal.value.categoria, filtroLocal.value.fecha_inicio, filtroLocal.value.fecha_fin],
  () => {
    paginaActual.value = 1
  }
)

const totalRegistros = computed(() => gastosFiltrados.value.length)
const totalPaginas = computed(() => Math.ceil(totalRegistros.value / elementosPorPagina.value) || 1)

const gastosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * elementosPorPagina.value
  const fin = inicio + elementosPorPagina.value
  return gastosFiltrados.value.slice(inicio, fin)
})

const indiceInicio = computed(() => {
  if (totalRegistros.value === 0) return 0
  return (paginaActual.value - 1) * elementosPorPagina.value + 1
})

const indiceFin = computed(() => {
  const fin = paginaActual.value * elementosPorPagina.value
  return fin > totalRegistros.value ? totalRegistros.value : fin
})

const cambiarPagina = (pagina) => {
  if (pagina >= 1 && pagina <= totalPaginas.value) {
    paginaActual.value = pagina
  }
}

// Custom Select Dropdown State & Methods
const dropdownOpen = ref(false)
const selectContainer = ref(null)
const filtroBusquedaSelect = ref('')

const pageSizeDropdownOpen = ref(false)
const pageSizeContainer = ref(null)

const togglePageSizeDropdown = () => {
  pageSizeDropdownOpen.value = !pageSizeDropdownOpen.value
}

const selectPageSize = (size) => {
  elementosPorPagina.value = size
  pageSizeDropdownOpen.value = false
}

const categoriasFiltradasSelect = computed(() => {
  const query = filtroBusquedaSelect.value.toLowerCase().trim()
  if (!query) return categoriasUnicas.value
  return categoriasUnicas.value.filter(cat => cat.toLowerCase().includes(query))
})

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
  if (dropdownOpen.value) {
    filtroBusquedaSelect.value = ''
  }
}

const selectCategory = (cat) => {
  filtroLocal.value.categoria = cat
  dropdownOpen.value = false
  emitirFiltros()
}

const clickOutsideHandler = (event) => {
  if (selectContainer.value && !selectContainer.value.contains(event.target)) {
    dropdownOpen.value = false
  }
  if (pageSizeContainer.value && !pageSizeContainer.value.contains(event.target)) {
    pageSizeDropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', clickOutsideHandler)
})

onUnmounted(() => {
  document.removeEventListener('click', clickOutsideHandler)
})

// Calculate Unique Categories dynamically for the filter dropdown
const categoriasUnicas = computed(() => {
  const base = ['Comida', 'Transporte', 'Ocio', 'Oficina', 'Otros']
  const delServidor = props.gastos.map(g => g.categoria).filter(Boolean)
  const combinadas = new Set([...base, ...delServidor])
  return Array.from(combinadas)
})

// Client-side text search filter applied on the database-returned expenses
const gastosFiltrados = computed(() => {
  if (!filtroLocal.value.busqueda.trim()) {
    return props.gastos
  }
  const query = filtroLocal.value.busqueda.toLowerCase().trim()
  const queryDot = query.replace(',', '.')
  return props.gastos.filter(gasto => {
    const importeStr = gasto.importe !== undefined && gasto.importe !== null ? gasto.importe.toString() : ''
    const importeFixed = gasto.importe !== undefined && gasto.importe !== null ? gasto.importe.toFixed(2) : ''
    const importeComas = importeFixed.replace('.', ',')

    return (
      (gasto.descripcion && gasto.descripcion.toLowerCase().includes(query)) ||
      (gasto.categoria && gasto.categoria.toLowerCase().includes(query)) ||
      importeStr.includes(queryDot) ||
      importeFixed.includes(queryDot) ||
      importeComas.includes(query)
    );
  })
})

const tieneFiltrosActivos = computed(() => {
  return (
    filtroLocal.value.busqueda ||
    filtroLocal.value.categoria ||
    filtroLocal.value.fecha_inicio ||
    filtroLocal.value.fecha_fin
  )
})

// Emit values to the parent App.vue for fetching backend data
const emitirFiltros = () => {
  emit('filtrar', {
    categoria: filtroLocal.value.categoria,
    fecha_inicio: filtroLocal.value.fecha_inicio,
    fecha_fin: filtroLocal.value.fecha_fin
  })
}

const limpiarFiltros = () => {
  filtroLocal.value = {
    busqueda: '',
    categoria: '',
    fecha_inicio: '',
    fecha_fin: ''
  }
  emitirFiltros()
}

// Helpers
const formatearMoneda = (valor) => {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'EUR'
  }).format(valor)
}

const formatearFecha = (fechaStr) => {
  if (!fechaStr) return ''
  const partes = fechaStr.split('-')
  if (partes.length !== 3) return fechaStr
  return `${partes[2]}/${partes[1]}/${partes[0]}`
}

const obtenerColorCategoria = (nombre) => {
  const lower = nombre.toLowerCase()
  if (lower.includes('comida')) return '#E5A93C'
  if (lower.includes('transporte')) return '#34D399'
  if (lower.includes('formacion') || lower.includes('formación')) return '#60A5FA'
  if (lower.includes('oficina') || lower.includes('obs')) return '#4ADE80'
  if (lower.includes('servicios') || lower.includes('luz') || lower.includes('agua')) return '#10B981'
  
  let hash = 0
  for (let i = 0; i < nombre.length; i++) {
    hash = nombre.charCodeAt(i) + ((hash << 5) - hash)
  }
  const h = Math.abs(hash) % 360
  return `hsl(${h}, 70%, 65%)`
}
</script>

<style scoped>
.list-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Filters Panel */
.filters-panel {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.panel-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.btn-clear {
  background: none;
  border: none;
  color: var(--accent);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  padding: 0.25rem;
  transition: var(--transition);
}

.btn-clear:hover {
  color: var(--text-primary);
  text-decoration: underline;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

@media (max-width: 768px) {
  .filters-grid {
    grid-template-columns: 1fr;
  }
  .col-span-3 {
    grid-column: span 1 !important;
  }
}

.col-span-3 {
  grid-column: span 3 / span 3;
}

.search-padding {
  padding-left: 2.2rem;
}

/* List Content & Table Layout */
.list-content {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid var(--border-color);
  border-top: 3px solid var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  width: 3rem;
  height: 3rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.empty-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.empty-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  max-width: 300px;
}

.table-responsive {
  width: 100%;
  overflow-x: auto;
}

.expenses-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.expenses-table th {
  background-color: rgba(11, 19, 26, 0.4);
  padding: 1rem 1.5rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border-color);
}

.expense-row {
  border-bottom: 1px solid var(--border-color);
  transition: var(--transition);
}

.expense-row:last-child {
  border-bottom: none;
}

.expense-row:hover {
  background-color: rgba(26, 43, 60, 0.2);
}

.expenses-table td {
  padding: 1rem 1.5rem;
  font-size: 0.85rem;
  color: var(--text-primary);
  vertical-align: middle;
}

.cell-date {
  color: var(--text-secondary);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.cell-description {
  max-width: 300px;
}

.desc-text {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.badge-category {
  display: inline-flex;
  align-items: center;
  padding: 0.3rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 50px;
  background-color: var(--bg-badge, rgba(255,255,255,0.05));
  color: var(--color-badge, var(--text-primary));
  white-space: nowrap;
}

.cell-amount {
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.text-right {
  text-align: right;
}

.text-center {
  text-align: center;
}

.actions-wrapper {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  cursor: pointer;
  transition: var(--transition);
}

.action-icon {
  width: 0.9rem;
  height: 0.9rem;
}

.btn-action.edit {
  color: var(--text-secondary);
}

.btn-action.edit:hover {
  background-color: var(--bg-input-focus);
  color: var(--accent);
}

.btn-action.delete {
  color: var(--text-secondary);
}

.btn-action.delete:hover {
  background-color: var(--danger-light);
  color: var(--danger);
}



/* Pagination Bar Styling */
.pagination-bar {
  display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem;
  background-color: rgba(11, 19, 26, 0.4); border-top: 1px solid var(--border-color); flex-wrap: wrap; gap: 1rem;
}
@media (max-width: 640px) {
  .pagination-bar { flex-direction: column; align-items: center; text-align: center; }
}
.pagination-info { font-size: 0.8rem; color: var(--text-secondary); }
.pagination-info .highlight { color: var(--text-primary); font-weight: 600; }
.pagination-controls { display: flex; align-items: center; gap: 0.35rem; }
.pag-btn {
  display: inline-flex; align-items: center; justify-content: center; min-width: 2rem; height: 2rem; padding: 0 0.5rem;
  font-family: var(--font-sans); font-size: 0.8rem; font-weight: 600; color: var(--text-secondary);
  background-color: var(--bg-input); border: 1px solid var(--border-color); border-radius: var(--radius-sm);
  cursor: pointer; transition: var(--transition); user-select: none;
}
.pag-btn:hover:not(:disabled) { background-color: var(--bg-input-focus); color: var(--accent); border-color: var(--border-color-focus); }
.pag-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.pag-btn.page-num.is-active { background-color: var(--accent); color: white; border-color: var(--accent); }
.pagination-size { display: flex; align-items: center; gap: 0.5rem; }
.size-label { font-size: 0.8rem; color: var(--text-secondary); }
.size-select {
  padding: 0.3rem 0.5rem; font-family: var(--font-sans); font-size: 0.8rem; color: var(--text-primary);
  background-color: var(--bg-input); border: 1px solid var(--border-color); border-radius: var(--radius-sm);
  outline: none; cursor: pointer; transition: var(--transition);
}
.size-select:focus { border-color: var(--border-color-focus); }

/* Responsive View Utilities */
.mobile-only {
  display: none !important;
}

@media (max-width: 768px) {
  .desktop-only {
    display: none !important;
  }
  .mobile-only {
    display: block !important;
  }
  .mobile-card-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }
  .expense-mobile-card {
    background-color: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    transition: var(--transition);
  }
  .expense-mobile-card:hover {
    border-color: var(--text-secondary);
    background-color: rgba(26, 43, 60, 0.15);
  }
  .mobile-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .mobile-card-date {
    font-size: 0.75rem;
    color: var(--text-secondary);
    font-variant-numeric: tabular-nums;
  }
  .mobile-card-body {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
  }
  .mobile-card-description {
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-primary);
    word-break: break-word;
    text-align: left;
  }
  .mobile-card-amount {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    white-space: nowrap;
  }
  .mobile-card-actions {
    display: flex;
    gap: 0.5rem;
    border-top: 1px solid var(--border-color);
    padding-top: 0.75rem;
    margin-top: 0.25rem;
  }
  .btn-action-mobile {
    flex: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    font-family: var(--font-sans);
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.5rem;
    border-radius: var(--radius-sm);
    background-color: var(--bg-input);
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    cursor: pointer;
    transition: var(--transition);
  }
  .btn-action-mobile:hover {
    background-color: var(--bg-input-focus);
    color: var(--text-primary);
  }
  .btn-action-mobile.edit:hover {
    color: var(--accent);
    border-color: var(--accent);
  }
  .btn-action-mobile.delete:hover {
    color: var(--danger);
    border-color: var(--danger);
    background-color: var(--danger-light);
  }
}
</style>
