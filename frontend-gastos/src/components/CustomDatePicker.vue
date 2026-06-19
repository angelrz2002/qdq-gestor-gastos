<template>
  <div class="custom-date-container" ref="dateContainer">
    <div class="custom-date-trigger" @click="toggleCalendar" :class="{ 'is-active': calendarOpen }">
      <span v-if="modelValue" class="selected-text">{{ formatearFechaDisplay(modelValue) }}</span>
      <span v-else class="placeholder-text">{{ placeholder }}</span>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="date-calendar-icon"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
    </div>
    
    <div v-if="calendarOpen" class="custom-calendar-popup">
      <div class="calendar-header">
        <button type="button" @click.stop="prevMonth" class="cal-btn">&lt;</button>
        <span class="calendar-month-year">{{ nombreMesActual }} {{ añoActual }}</span>
        <button type="button" @click.stop="nextMonth" class="cal-btn">&gt;</button>
      </div>
      <div class="calendar-weekdays">
        <span v-for="d in ['L', 'M', 'X', 'J', 'V', 'S', 'D']" :key="d" class="weekday">{{ d }}</span>
      </div>
      <div class="calendar-days">
        <div v-for="(pad, idx) in vaciosInicio" :key="'pad-' + idx" class="calendar-day empty"></div>
        <div 
          v-for="dia in diasDelMes" 
          :key="dia" 
          class="calendar-day"
          :class="{ 
            'is-today': esHoy(dia), 
            'is-selected': esSeleccionado(dia) 
          }"
          @click.stop="seleccionarDia(dia)"
        >
          {{ dia }}
        </div>
      </div>
      <div class="calendar-footer">
        <button type="button" @click.stop="establecerHoy" class="footer-btn">Hoy</button>
        <button type="button" @click.stop="limpiarFecha" class="footer-btn text-danger">Borrar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Selecciona una fecha...'
  }
})

const emit = defineEmits(['update:modelValue'])

const calendarOpen = ref(false)
const dateContainer = ref(null)
const fechaReferencia = ref(new Date())

const añoActual = computed(() => fechaReferencia.value.getFullYear())
const mesActual = computed(() => fechaReferencia.value.getMonth())

const nombreMesActual = computed(() => {
  const nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  return nombres[mesActual.value]
})

const vaciosInicio = computed(() => {
  const primerDia = new Date(añoActual.value, mesActual.value, 1).getDay()
  return primerDia === 0 ? 6 : primerDia - 1
})

const diasDelMes = computed(() => {
  const total = new Date(añoActual.value, mesActual.value + 1, 0).getDate()
  return Array.from({ length: total }, (_, i) => i + 1)
})

const toggleCalendar = () => {
  calendarOpen.value = !calendarOpen.value
  if (calendarOpen.value && props.modelValue) {
    fechaReferencia.value = new Date(props.modelValue + 'T00:00:00')
  } else if (calendarOpen.value) {
    fechaReferencia.value = new Date()
  }
}

const prevMonth = () => {
  fechaReferencia.value = new Date(añoActual.value, mesActual.value - 1, 1)
}

const nextMonth = () => {
  fechaReferencia.value = new Date(añoActual.value, mesActual.value + 1, 1)
}

const seleccionarDia = (dia) => {
  const mesStr = String(mesActual.value + 1).padStart(2, '0')
  const diaStr = String(dia).padStart(2, '0')
  emit('update:modelValue', `${añoActual.value}-${mesStr}-${diaStr}`)
  calendarOpen.value = false
}

const esHoy = (dia) => {
  const hoy = new Date()
  return hoy.getDate() === dia && hoy.getMonth() === mesActual.value && hoy.getFullYear() === añoActual.value
}

const esSeleccionado = (dia) => {
  if (!props.modelValue) return false
  const [y, m, d] = props.modelValue.split('-').map(Number)
  return d === dia && m === (mesActual.value + 1) && y === añoActual.value
}

const establecerHoy = () => {
  const hoy = new Date()
  const y = hoy.getFullYear()
  const m = String(hoy.getMonth() + 1).padStart(2, '0')
  const d = String(hoy.getDate()).padStart(2, '0')
  emit('update:modelValue', `${y}-${m}-${d}`)
  calendarOpen.value = false
}

const limpiarFecha = () => {
  emit('update:modelValue', '')
  calendarOpen.value = false
}

const formatearFechaDisplay = (fechaStr) => {
  if (!fechaStr) return ''
  const partes = fechaStr.split('-')
  if (partes.length !== 3) return fechaStr
  return `${partes[2]}/${partes[1]}/${partes[0]}`
}

const clickOutsideCalendar = (event) => {
  if (dateContainer.value && !dateContainer.value.contains(event.target)) {
    calendarOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', clickOutsideCalendar)
})

onUnmounted(() => {
  document.removeEventListener('click', clickOutsideCalendar)
})
</script>

<style scoped>
.custom-date-container {
  position: relative;
  width: 100%;
}

.custom-date-trigger {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0.65rem 0.85rem;
  font-size: 0.85rem;
  color: var(--text-primary);
  background-color: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition);
  user-select: none;
}

.custom-date-trigger:focus,
.custom-date-trigger.is-active {
  background-color: var(--bg-input-focus);
  border-color: var(--border-color-focus);
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.15);
}

.placeholder-text {
  color: var(--text-secondary);
}

.date-calendar-icon {
  width: 1.1rem;
  height: 1.1rem;
  color: var(--text-secondary);
  transition: var(--transition);
}

.custom-date-trigger.is-active .date-calendar-icon {
  color: var(--accent);
}

/* Simulated Calendar Popup */
.custom-calendar-popup {
  position: absolute;
  top: 100%;
  left: 0;
  width: 280px;
  margin-top: 0.35rem;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  z-index: 70;
  padding: 1rem;
  user-select: none;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.calendar-month-year {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-primary);
}

.cal-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  transition: var(--transition);
}

.cal-btn:hover {
  background-color: var(--bg-input-focus);
  color: var(--text-primary);
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  margin-bottom: 0.35rem;
}

.weekday {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text-secondary);
  padding: 0.25rem 0;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  text-align: center;
}

.calendar-day {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-primary);
  padding: 0.4rem 0;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: var(--transition);
}

.calendar-day:hover:not(.empty) {
  background-color: var(--bg-input-focus);
  color: var(--accent);
}

.calendar-day.empty {
  cursor: default;
}

.calendar-day.is-today {
  border: 1px solid var(--accent);
  color: var(--accent);
}

.calendar-day.is-selected {
  background-color: var(--accent) !important;
  color: white !important;
  font-weight: 700;
}

.calendar-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 0.75rem;
  padding-top: 0.5rem;
  border-top: 1px solid var(--border-color);
}

.footer-btn {
  background: none;
  border: none;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--accent);
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  transition: var(--transition);
}

.footer-btn:hover {
  background-color: var(--bg-input-focus);
}

.footer-btn.text-danger {
  color: var(--danger);
}

.footer-btn.text-danger:hover {
  background-color: var(--danger-light);
}
</style>
