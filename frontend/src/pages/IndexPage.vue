<template>
  <q-page class="flex flex-center column q-pt-xl">
    <div class="content-container q-pa-md q-mt-lg">
      <transition name="fade" mode="out-in">
        <RoleSelector v-if="!selectedRole" @select="selectRole" />

        <div v-else class="column full-width">
          <div
            class="row items-center q-mb-lg cursor-pointer text-muted hover-text-primary transition-generic"
            @click="reset"
          >
            <q-icon name="arrow_back" size="xs" class="q-mr-xs" />
            <span class="text-caption text-uppercase text-weight-medium">Back to Roles</span>
          </div>

          <IncidentForm
            v-model="form"
            :role="selectedRole"
            :loading="loading"
            @submit="generatePlan"
          />

          <div v-if="loading" class="q-mt-xl text-center text-muted">
            <q-spinner-dots size="3rem" class="text-main" />
            <div class="text-caption q-mt-sm">Analyzing incident context...</div>
          </div>

          <IncidentPlanComponent
            v-if="plan"
            :plan="plan"
            :role="selectedRole"
            :saved-checks="currentChecks"
            @update:progress="handleProgressUpdate"
          />
        </div>
      </transition>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useQuasar } from 'quasar';
import { IncidentService, type IncidentPlan } from 'src/services/IncidentService';
import { useHistory } from 'src/composables/useHistory';

import RoleSelector from 'components/RoleSelector.vue';
import IncidentForm from 'components/IncidentForm.vue';
import IncidentPlanComponent from 'components/IncidentPlan.vue';

const $q = useQuasar();
const { save, activeItem, updateProgress } = useHistory();

const selectedRole = ref<string | null>(null);
const loading = ref(false);
const plan = ref<IncidentPlan | null>(null);

const currentHistoryId = ref<string | null>(null);
const currentChecks = ref<boolean[]>([]);

const form = ref({ description: '', logs: '', context: '' });

watch(activeItem, (newItem) => {
  if (newItem) {
    selectedRole.value = newItem.role;
    form.value = { ...newItem.form };
    plan.value = newItem.plan;

    currentHistoryId.value = newItem.id;
    currentChecks.value = newItem.checkedSteps || [];
  }
});

const selectRole = (role: string) => {
  selectedRole.value = role;
};

const reset = () => {
  selectedRole.value = null;
  form.value = { description: '', logs: '', context: '' };
  plan.value = null;
  currentHistoryId.value = null;
  currentChecks.value = [];
};

const handleProgressUpdate = (checks: boolean[]) => {
  currentChecks.value = checks;

  if (currentHistoryId.value) {
    updateProgress(currentHistoryId.value, checks);
  }
};

const generatePlan = async () => {
  if (!form.value.description) return;

  loading.value = true;
  plan.value = null;

  try {
    const payload = { ...form.value, role: selectedRole.value };
    const data = await IncidentService.generatePlan(payload);

    plan.value = data;
    currentChecks.value = [];

    const newId = save(selectedRole.value!, form.value, data);
    currentHistoryId.value = newId;
  } catch (err) {
    console.error(err);
    $q.notify({ type: 'negative', message: 'Error generating plan' });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.content-container {
  max-width: 900px;
  width: 100%;
}
.hover-text-primary {
  transition: color 0.3s ease;
}
.hover-text-primary:hover {
  color: var(--q-primary);
}
</style>
