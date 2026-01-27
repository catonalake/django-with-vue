<script setup>
import axios from 'axios'
import { reactive, watch, computed, defineProps, defineEmits } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Checkbox from 'primevue/checkbox'
import InputNumber from 'primevue/inputnumber'
import Panel from 'primevue/panel'
import ProgressSpinner from 'primevue/progressspinner'
import Message from 'primevue/message'

const props = defineProps({
    project: Object
})

const emit = defineEmits(['schedule-part', 'update-ship-selection'])

const state = reactive({
    structures: [],
    loading: false,
    error: null,
    expandedRows: {},
    selectedForShipping: {}
})

watch(() => props.project, async (newProject) => {
    if (newProject) {
        await loadStructures(newProject.id)
    } else {
        state.structures = []
    }
}, { immediate: true })

async function loadStructures(projectId) {
    state.loading = true
    state.error = null
    state.selectedForShipping = {}
    state.expandedRows = {}
    try {
        const response = await axios.get(`/api/projects/${projectId}/structures/`)
        state.structures = response.data.data
        state.loading = false
    } catch (error) {
        state.error = 'Failed to load structures'
        state.loading = false
        console.error(error)
    }
}

function onScheduleClick(partDetail) {
    emit('schedule-part', partDetail)
}

function isSelected(partId) {
    return !!state.selectedForShipping[partId]
}

function onSelectionChange(partDetail, checked) {
    if (checked) {
        state.selectedForShipping[partDetail.id] = {
            ...partDetail,
            shipQuantity: partDetail.quantity
        }
    } else {
        delete state.selectedForShipping[partDetail.id]
    }
    emit('update-ship-selection', Object.values(state.selectedForShipping))
}

function updateShipQuantity(partDetail, quantity) {
    if (state.selectedForShipping[partDetail.id]) {
        state.selectedForShipping[partDetail.id].shipQuantity = quantity
        emit('update-ship-selection', Object.values(state.selectedForShipping))
    }
}

function getShipQuantity(partId) {
    return state.selectedForShipping[partId]?.shipQuantity || 1
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
}

function formatWeight(value) {
    return `${parseFloat(value).toLocaleString()} lbs`
}
</script>

<template>
    <div class="structure-list">
        <div v-if="state.loading" class="loading-container">
            <ProgressSpinner />
        </div>

        <Message v-else-if="state.error" severity="error" :closable="false">
            {{ state.error }}
        </Message>

        <Message v-else-if="!props.project" severity="info" :closable="false">
            Select a project to view structures
        </Message>

        <Message v-else-if="state.structures.length === 0" severity="warn" :closable="false">
            No structures found for this project
        </Message>

        <div v-else class="structures-container">
            <Panel
                v-for="structure in state.structures"
                :key="structure.id"
                :header="structure.name"
                toggleable
                class="structure-panel"
            >
                <template #header>
                    <div class="panel-header">
                        <span class="structure-name">{{ structure.name }}</span>
                        <Tag :value="`${structure.part_details.length} parts`" severity="info" />
                    </div>
                </template>

                <p v-if="structure.description" class="structure-description">
                    {{ structure.description }}
                </p>

                <DataTable
                    :value="structure.part_details"
                    stripedRows
                    size="small"
                    class="parts-table"
                >
                    <Column style="width: 120px">
                        <template #header>
                            <span class="select-header">
                                <i class="pi pi-truck"></i> Ship
                            </span>
                        </template>
                        <template #body="{ data }">
                            <div class="ship-cell">
                                <Checkbox
                                    :modelValue="isSelected(data.id)"
                                    @update:modelValue="onSelectionChange(data, $event)"
                                    :disabled="!data.is_released"
                                    binary
                                />
                                <InputNumber
                                    v-if="isSelected(data.id)"
                                    :modelValue="getShipQuantity(data.id)"
                                    @update:modelValue="updateShipQuantity(data, $event)"
                                    :min="1"
                                    :max="data.quantity"
                                    showButtons
                                    buttonLayout="horizontal"
                                    :inputStyle="{ width: '50px' }"
                                    decrementButtonClass="p-button-secondary"
                                    incrementButtonClass="p-button-secondary"
                                    size="small"
                                />
                            </div>
                        </template>
                    </Column>

                    <Column field="name" header="Name" sortable />

                    <Column field="price" header="Price" sortable style="width: 120px">
                        <template #body="{ data }">
                            {{ formatCurrency(data.price) }}
                        </template>
                    </Column>

                    <Column field="quantity" header="Qty" sortable style="width: 80px" />

                    <Column field="weight" header="Weight" sortable style="width: 120px">
                        <template #body="{ data }">
                            {{ formatWeight(data.weight) }}
                        </template>
                    </Column>

                    <Column header="Status" style="width: 100px">
                        <template #body="{ data }">
                            <Tag
                                :value="data.is_released ? 'Released' : 'Pending'"
                                :severity="data.is_released ? 'success' : 'warn'"
                            />
                        </template>
                    </Column>

                    <Column header="Takeoff" style="width: 100px">
                        <template #body="{ data }">
                            <a
                                v-if="data.takeoff_url"
                                :href="data.takeoff_url"
                                target="_blank"
                                class="takeoff-link"
                            >
                                <i class="pi pi-external-link"></i> View
                            </a>
                            <span v-else class="no-takeoff">—</span>
                        </template>
                    </Column>

                    <Column header="Actions" style="width: 140px">
                        <template #body="{ data }">
                            <Button
                                label="Schedule Pour"
                                icon="pi pi-calendar"
                                size="small"
                                outlined
                                @click="onScheduleClick(data)"
                                :disabled="!data.is_released"
                            />
                        </template>
                    </Column>
                </DataTable>
            </Panel>
        </div>
    </div>
</template>

<style scoped>
.structure-list {
    margin-top: 1rem;
}

.loading-container {
    display: flex;
    justify-content: center;
    padding: 2rem;
}

.structures-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.structure-panel {
    border-radius: 8px;
}

.panel-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    width: 100%;
}

.structure-name {
    font-weight: 600;
    font-size: 1.1rem;
}

.structure-description {
    color: #666;
    margin-bottom: 1rem;
    font-style: italic;
}

.ship-cell {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.takeoff-link {
    color: var(--p-primary-color);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.takeoff-link:hover {
    text-decoration: underline;
}

.no-takeoff {
    color: #999;
}

:deep(.parts-table) {
    font-size: 0.9rem;
}

.select-header {
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.select-header i {
    color: #3b82f6;
}
</style>
