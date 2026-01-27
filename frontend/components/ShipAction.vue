<script setup>
import axios from 'axios'
import { computed, reactive, ref, defineProps, defineEmits } from 'vue'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Textarea from 'primevue/textarea'
import Chip from 'primevue/chip'
import Message from 'primevue/message'
import Divider from 'primevue/divider'
import Badge from 'primevue/badge'
import { useToast } from 'primevue/usetoast'

const toast = useToast()

const props = defineProps({
    selectedParts: Array
})

const emit = defineEmits(['shipped', 'clear-selection'])

const state = reactive({
    notes: '',
    submitting: false,
    error: null,
    showDialog: false
})

const totalWeight = computed(() => {
    if (!props.selectedParts || props.selectedParts.length === 0) return 0
    return props.selectedParts.reduce((sum, part) => {
        return sum + (parseFloat(part.weight) * (part.shipQuantity || part.quantity))
    }, 0)
})

const formattedWeight = computed(() => {
    return totalWeight.value.toLocaleString(undefined, { maximumFractionDigits: 2 })
})

const hasSelection = computed(() => {
    return props.selectedParts && props.selectedParts.length > 0
})

const partCount = computed(() => {
    return props.selectedParts?.length || 0
})

function openDialog() {
    state.showDialog = true
    state.error = null
}

function closeDialog() {
    state.showDialog = false
}

async function submitShipment() {
    if (!hasSelection.value) return

    state.submitting = true
    state.error = null

    const now = new Date().toISOString()
    const parts = props.selectedParts.map(p => ({
        part_detail_id: p.id,
        quantity: p.shipQuantity || p.quantity,
        weight: parseFloat(p.weight)
    }))

    try {
        const response = await axios.post('/api/shipping-events/create/', {
            shipped_date: now,
            notes: state.notes,
            parts: parts
        })
        emit('shipped', response.data)
        emit('clear-selection')
        state.notes = ''
        state.showDialog = false

        toast.add({
            severity: 'success',
            summary: 'Shipment Created',
            detail: `Successfully shipped ${parts.length} part(s) - Total weight: ${formattedWeight.value} lbs`,
            life: 5000
        })
    } catch (error) {
        state.error = error.response?.data?.error || 'Failed to create shipment'
        console.error(error)
    } finally {
        state.submitting = false
    }
}

function getPartWeight(part) {
    const weight = parseFloat(part.weight) * (part.shipQuantity || part.quantity)
    return weight.toLocaleString(undefined, { maximumFractionDigits: 2 })
}
</script>

<template>
    <!-- Floating Action Button -->
    <transition name="fab-slide">
        <div v-if="hasSelection" class="fab-container">
            <Button
                @click="openDialog"
                class="fab-button"
                rounded
                size="large"
            >
                <i class="pi pi-truck"></i>
                <span class="fab-label">Ship Parts</span>
                <Badge :value="partCount" severity="contrast" />
            </Button>
            <div class="fab-weight">{{ formattedWeight }} lbs</div>
        </div>
    </transition>

    <!-- Ship Dialog -->
    <Dialog
        v-model:visible="state.showDialog"
        header="Create Shipment"
        :modal="true"
        :style="{ width: '500px' }"
    >
        <Message v-if="state.error" severity="error" :closable="false" class="mb-3">
            {{ state.error }}
        </Message>

        <div class="dialog-content">
            <div class="selected-parts">
                <label>Parts to Ship:</label>
                <div class="chips-container">
                    <Chip
                        v-for="part in props.selectedParts"
                        :key="part.id"
                        class="part-chip"
                    >
                        <span class="part-name">{{ part.name }}</span>
                        <span class="part-qty">×{{ part.shipQuantity || part.quantity }}</span>
                        <span class="part-weight">({{ getPartWeight(part) }} lbs)</span>
                    </Chip>
                </div>
            </div>

            <Divider />

            <div class="total-section">
                <div class="total-label">Total Weight:</div>
                <div class="total-value">{{ formattedWeight }} lbs</div>
            </div>

            <div class="notes-section">
                <label for="notes">Notes (optional)</label>
                <Textarea
                    id="notes"
                    v-model="state.notes"
                    rows="3"
                    placeholder="Add shipping notes, truck info, destination..."
                    class="w-full"
                />
            </div>
        </div>

        <template #footer>
            <Button
                label="Cancel"
                severity="secondary"
                outlined
                @click="closeDialog"
                :disabled="state.submitting"
            />
            <Button
                :label="state.submitting ? 'Creating...' : 'Create Shipment'"
                icon="pi pi-truck"
                @click="submitShipment"
                :loading="state.submitting"
            />
        </template>
    </Dialog>
</template>

<style scoped>
.fab-container {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
    z-index: 1000;
}

.fab-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 1.5rem;
    font-size: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.fab-button:hover {
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
    transform: translateY(-2px);
}

.fab-label {
    font-weight: 600;
}

.fab-weight {
    background: #1e293b;
    color: white;
    padding: 0.35rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.85rem;
    font-weight: 500;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Transition for FAB */
.fab-slide-enter-active,
.fab-slide-leave-active {
    transition: all 0.3s ease;
}

.fab-slide-enter-from,
.fab-slide-leave-to {
    opacity: 0;
    transform: translateY(20px);
}

/* Dialog styles */
.dialog-content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.selected-parts label {
    font-weight: 600;
    color: #475569;
    display: block;
    margin-bottom: 0.5rem;
}

.chips-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    max-height: 150px;
    overflow-y: auto;
    padding: 0.5rem;
    background: #f8fafc;
    border-radius: 8px;
}

.part-chip {
    background: white;
    border: 1px solid #e2e8f0;
}

.part-name {
    font-weight: 500;
}

.part-qty {
    color: #3b82f6;
    margin-left: 0.25rem;
}

.part-weight {
    color: #64748b;
    font-size: 0.85rem;
    margin-left: 0.25rem;
}

.total-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: #f0fdf4;
    border-radius: 8px;
    border: 1px solid #bbf7d0;
}

.total-label {
    font-weight: 600;
    color: #166534;
}

.total-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #166534;
}

.notes-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.notes-section label {
    font-weight: 600;
    color: #475569;
}

.w-full {
    width: 100%;
}

.mb-3 {
    margin-bottom: 0.75rem;
}
</style>
