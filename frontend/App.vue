<script setup>
import { reactive } from 'vue'
import store from './store'
import Toast from 'primevue/toast'
import ProjectSelector from './components/ProjectSelector.vue'
import StructureList from './components/StructureList.vue'
import ScheduleModal from './components/ScheduleModal.vue'
import ShipAction from './components/ShipAction.vue'

const props = defineProps({
  token: String,
  user: String
})

if (props.token) {
  store.setToken(props.token)
}

const state = reactive({
  selectedProject: null,
  scheduleModalPart: null,
  showScheduleModal: false,
  selectedForShipping: []
})

function onProjectSelected(project) {
  state.selectedProject = project
  state.selectedForShipping = []
}

function onSchedulePart(partDetail) {
  state.scheduleModalPart = partDetail
  state.showScheduleModal = true
}

function onScheduleModalClose() {
  state.showScheduleModal = false
  state.scheduleModalPart = null
}

function onScheduled(event) {
  console.log('Scheduled:', event)
}

function onUpdateShipSelection(parts) {
  state.selectedForShipping = parts
}

function onShipped(event) {
  console.log('Shipped:', event)
}

function onClearSelection() {
  state.selectedForShipping = []
}
</script>

<template>
  <Toast position="top-right" />

  <div class="app-container">
    <header>
      <h1>
        <i class="pi pi-building"></i>
        Project Parts Manager
      </h1>
      <p class="subtitle">Manage structures, schedule pours, and ship parts</p>
    </header>

    <main>
      <ProjectSelector @project-selected="onProjectSelected" />

      <div v-if="state.selectedProject" class="helper-text">
        <i class="pi pi-info-circle"></i>
        Select parts using the <i class="pi pi-truck"></i> checkbox column to ship, or click "Schedule Pour" for production scheduling.
      </div>

      <StructureList
        :project="state.selectedProject"
        @schedule-part="onSchedulePart"
        @update-ship-selection="onUpdateShipSelection"
      />

      <ScheduleModal
        :part-detail="state.scheduleModalPart"
        :show="state.showScheduleModal"
        @close="onScheduleModalClose"
        @scheduled="onScheduled"
      />

      <!-- Floating ship button -->
      <ShipAction
        :selected-parts="state.selectedForShipping"
        @shipped="onShipped"
        @clear-selection="onClearSelection"
      />
    </main>

    <footer>
      <p>Built with Django + Vue + PrimeVue</p>
    </footer>
  </div>
</template>

<style>
/* Global styles */
body {
  margin: 0;
  background: #f1f5f9;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}

* {
  box-sizing: border-box;
}
</style>

<style scoped>
.app-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  margin-bottom: 2rem;
}

header h1 {
  margin: 0;
  color: #1e293b;
  font-size: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

header h1 i {
  color: #3b82f6;
}

.subtitle {
  margin: 0.5rem 0 0 0;
  color: #64748b;
  font-size: 1rem;
}

main {
  flex: 1;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
}

footer {
  margin-top: 2rem;
  text-align: center;
  color: #94a3b8;
  font-size: 0.875rem;
}

footer p {
  margin: 0;
}

.helper-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  color: #1e40af;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.helper-text i {
  color: #3b82f6;
}
</style>
