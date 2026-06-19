<template>
  <div class="summary-container">
    <!-- Main Total Card -->
    <div class="summary-total-card">
      <span class="total-label">Total Acumulado</span>
      <h2 class="total-amount">{{ formatearMoneda(totalAcumulado) }}</h2>
      <div class="total-footer">
        <span class="total-count">{{ gastos.length }} {{ gastos.length === 1 ? 'gasto registrado' : 'gastos registrados' }}</span>
      </div>
    </div>

    <!-- Category Breakdown Title -->
    <div class="category-header">
      <h3 class="category-title">Por Categorías</h3>
    </div>

    <!-- Category Cards List -->
    <div class="category-list">
      <div v-if="desgloseCategorias.length === 0" class="empty-categories">
        No hay datos para clasificar
      </div>
      
      <div 
        v-for="cat in desgloseCategorias" 
        :key="cat.nombre" 
        class="category-card"
        :style="{ '--accent-cat': obtenerColorCategoria(cat.nombre) }"
      >
        <div class="category-card-header">
          <span class="category-badge-dot"></span>
          <span class="category-name" :title="cat.nombre">{{ cat.nombre }}</span>
        </div>
        <div class="category-card-body">
          <span class="category-amount">{{ formatearMoneda(cat.total) }}</span>
          <span class="category-percentage">{{ cat.porcentaje }}%</span>
        </div>
        <!-- Progress bar for visual representation -->
        <div class="category-progress-bg">
          <div class="category-progress-bar" :style="{ width: cat.porcentaje + '%' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  gastos: {
    type: Array,
    required: true,
    default: () => []
  }
})

// Calculate Total Accumulated
const totalAcumulado = computed(() => {
  return props.gastos.reduce((acc, gasto) => acc + Number(gasto.importe || 0), 0)
})

// Calculate breakdown by categories
const desgloseCategorias = computed(() => {
  const grupos = {}
  
  props.gastos.forEach(gasto => {
    const cat = gasto.categoria || 'Otros'
    grupos[cat] = (grupos[cat] || 0) + Number(gasto.importe || 0)
  })

  const total = totalAcumulado.value || 1 // Avoid division by zero
  
  return Object.keys(grupos).map(nombre => {
    const subtotal = grupos[nombre]
    return {
      nombre,
      total: subtotal,
      porcentaje: Math.round((subtotal / total) * 100)
    }
  }).sort((a, b) => b.total - a.total)
})

// Format numeric values to Euros
const formatearMoneda = (valor) => {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'EUR'
  }).format(valor)
}

// Generate nice dynamic colors based on category names (adjusted for dark mode visibility)
const obtenerColorCategoria = (nombre) => {
  const lower = nombre.toLowerCase()
  if (lower.includes('comida')) return '#E5A93C'
  if (lower.includes('transporte')) return '#34D399'
  if (lower.includes('formacion') || lower.includes('formación')) return '#60A5FA'
  if (lower.includes('oficina') || lower.includes('obs')) return '#00A859'
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
.summary-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Total Card Styling */
.summary-total-card {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.summary-total-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background-color: var(--primary);
}

.summary-total-card:hover {
  border-color: var(--text-tertiary);
}

.total-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.total-amount {
  font-size: 2.1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-top: 0.25rem;
  letter-spacing: -0.02em;
}

.total-footer {
  margin-top: 0.75rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.total-count {
  font-weight: 500;
  color: var(--text-primary);
}

/* Category Section */
.category-header {
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
}

.category-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.empty-categories {
  background-color: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-md);
  padding: 2rem 1rem;
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

/* Individual Category Card */
.category-card {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  box-shadow: var(--shadow-sm);
  transition: var(--transition);
}

.category-card:hover {
  border-color: var(--text-secondary);
}

.category-card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.35rem;
}

.category-badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--accent-cat, var(--primary));
}

.category-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.category-card-body {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.5rem;
}

.category-amount {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
}

.category-percentage {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-secondary);
}

/* Category Progress Bar */
.category-progress-bg {
  height: 4px;
  background-color: var(--bg-app);
  border-radius: 2px;
  overflow: hidden;
}

.category-progress-bar {
  height: 100%;
  background-color: var(--accent-cat, var(--primary));
  border-radius: 2px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
