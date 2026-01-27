<script setup>
import axios from 'axios'
import { reactive, watch, defineProps, defineEmits } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import DatePicker from 'primevue/datepicker'
import Message from 'primevue/message'
import FloatLabel from 'primevue/floatlabel'

const props = defineProps({
    partDetail: Object,
    show: Boolean
})

const emit = defineEmits(['close', 'scheduled'])

const state = reactive({
    scheduledDate: null,
    scheduledTime: null,
    quantity: 1,
    partIdentifier: '',
    price: 0,
    submitting: false,
    error: null
})

watch(() => props.partDetail, (newPart) => {
    if (newPart) {
        state.partIdentifier = newPart.name
        state.price = parseFloat(newPart.price)
        state.quantity = 1
        state.scheduledDate = null
        state.scheduledTime = null
        state.error = null
    }
}, { immediate: true })

function formatDate(date) {
    if (!date) return null
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
}

function formatTime(date) {
    if (!date) return null
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${hours}:${minutes}`
}

async function submitSchedule() {
    if (!state.scheduledDate || !state.scheduledTime) {
        state.error = 'Date and time are required'
        return
    }

    state.submitting = true
    state.error = null

    try {
        const response = await axios.post('/api/schedule-events/', {
            part_detail_id: props.partDetail.id,
            scheduled_date: formatDate(state.scheduledDate),
            scheduled_time: formatTime(state.scheduledTime),
            quantity: state.quantity,
            part_identifier: state.partIdentifier,
            price: state.price
        })
        emit('scheduled', response.data)
        emit('close')
    } catch (error) {
        state.error = error.response?.data?.error || 'Failed to schedule'
        console.error(error)
    } finally {
        state.submitting = false
    }
}

function close() {
    emit('close')
}
</script>

<template>
    <Dialog
        :visible="props.show"
        @update:visible="close"
        header="Schedule Pour"
        :modal="true"
        :closable="true"
        :style="{ width: '450px' }"
    >
        <Message v-if="state.error" severity="error" :closable="false" class="mb-4">
            {{ state.error }}
        </Message>

        <div class="form-container">
            <div class="form-row">
                <label>Original Part:</label>
                <span class="original-part">{{ props.partDetail?.name }}</span>
            </div>

            <div class="form-row">
                <FloatLabel>
                    <InputText
                        id="part-identifier"
                        v-model="state.partIdentifier"
                        class="w-full"
                    />
                    <label for="part-identifier">Part Identifier</label>
                </FloatLabel>
            </div>

            <div class="form-row-split">
                <FloatLabel class="flex-1">
                    <InputNumber
                        id="price"
                        v-model="state.price"
                        mode="currency"
                        currency="USD"
                        locale="en-US"
                        class="w-full"
                    />
                    <label for="price">Price</label>
                </FloatLabel>

                <FloatLabel class="flex-1">
                    <InputNumber
                        id="quantity"
                        v-model="state.quantity"
                        :min="1"
                        showButtons
                        class="w-full"
                    />
                    <label for="quantity">Quantity</label>
                </FloatLabel>
            </div>

            <div class="form-row-split">
                <FloatLabel class="flex-1">
                    <DatePicker
                        id="scheduled-date"
                        v-model="state.scheduledDate"
                        dateFormat="mm/dd/yy"
                        showIcon
                        class="w-full"
                    />
                    <label for="scheduled-date">Date</label>
                </FloatLabel>

                <FloatLabel class="flex-1">
                    <DatePicker
                        id="scheduled-time"
                        v-model="state.scheduledTime"
                        timeOnly
                        showIcon
                        class="w-full"
                    >
                        <template #inputicon="{ clickCallback }">
                            <i class="pi pi-clock" @click="clickCallback" />
                        </template>
                    </DatePicker>
                    <label for="scheduled-time">Time</label>
                </FloatLabel>
            </div>
        </div>

        <template #footer>
            <Button
                label="Cancel"
                severity="secondary"
                outlined
                @click="close"
                :disabled="state.submitting"
            />
            <Button
                :label="state.submitting ? 'Scheduling...' : 'Schedule'"
                icon="pi pi-calendar-plus"
                @click="submitSchedule"
                :loading="state.submitting"
            />
        </template>
    </Dialog>
</template>

<style scoped>
.form-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1rem 0;
}

.form-row {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-row label {
    font-weight: 600;
    color: #666;
}

.original-part {
    font-size: 1.1rem;
    color: #333;
}

.form-row-split {
    display: flex;
    gap: 1rem;
}

.flex-1 {
    flex: 1;
}

.mb-4 {
    margin-bottom: 1rem;
}

.w-full {
    width: 100%;
}
</style>
