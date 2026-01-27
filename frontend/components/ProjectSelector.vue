<script setup>
import axios from 'axios'
import { reactive, onMounted, defineEmits } from 'vue'
import Select from 'primevue/select'

const emit = defineEmits(['project-selected'])

const state = reactive({
    projects: [],
    selectedProject: null,
    loading: true,
    error: null
})

onMounted(async () => {
    try {
        const response = await axios.get('/api/projects/')
        state.projects = response.data.data
        state.loading = false
    } catch (error) {
        state.error = 'Failed to load projects'
        state.loading = false
        console.error(error)
    }
})

function onProjectChange(event) {
    emit('project-selected', state.selectedProject)
}
</script>

<template>
    <div class="project-selector">
        <label for="project-select">Select Project</label>
        <Select
            id="project-select"
            v-model="state.selectedProject"
            :options="state.projects"
            optionLabel="name"
            placeholder="Choose a project"
            :loading="state.loading"
            @change="onProjectChange"
            class="w-full md:w-80"
            showClear
        />
        <small v-if="state.error" class="p-error">{{ state.error }}</small>
    </div>
</template>

<style scoped>
.project-selector {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.project-selector label {
    font-weight: 600;
    white-space: nowrap;
}
</style>
