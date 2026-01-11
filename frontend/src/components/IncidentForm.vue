<template>
  <q-card v-if="config" flat class="my-surface shadow-soft rounded-xl q-pa-lg animate-fade-up">
    <div class="row items-center q-mb-lg">
      <div class="col">
        <div class="text-overline text-weight-bold" :class="`text-${config?.color}`">
          {{ config?.title?.toUpperCase() }} MODE
        </div>
        <div class="text-h5 text-weight-bold text-main">{{ config?.inputs?.description }}</div>
      </div>

      <q-icon :name="config?.icon" size="lg" :color="config?.color" class="opacity-20" />
    </div>

    <div class="q-gutter-y-lg">
      <q-input
        outlined
        :dark="$q.dark.isActive"
        v-model="descriptionProxy"
        :label="config?.inputs?.description"
        :hint="config?.inputs?.descHint"
        type="textarea"
        rows="3"
        class="input-rounded"
        :color="config?.color"
      >
        <template v-slot:prepend><q-icon name="edit" /></template>
      </q-input>

      <div class="row q-col-gutter-md">
        <div class="col-12 col-md-6">
          <q-input
            outlined
            :dark="$q.dark.isActive"
            v-model="logsProxy"
            :label="config?.inputs?.logs"
            :placeholder="config?.inputs?.logsHint"
            type="textarea"
            rows="5"
            class="input-rounded font-mono text-caption"
            :color="config?.color"
          />
        </div>
        <div class="col-12 col-md-6">
          <q-input
            outlined
            :dark="$q.dark.isActive"
            v-model="contextProxy"
            :label="config?.inputs?.context"
            :placeholder="config?.inputs?.contextHint"
            type="textarea"
            rows="5"
            class="input-rounded"
            :color="config?.color"
          />
        </div>
      </div>
    </div>

    <div class="row justify-end q-mt-xl">
      <q-btn
        unelevated
        rounded
        size="lg"
        :color="config?.color"
        class="q-px-xl hover-lift shadow-dynamic"
        :loading="loading"
        @click="$emit('submit')"
        :disable="!descriptionProxy"
      >
        <div class="row items-center">
          <span>Generate Plan</span>
          <q-icon name="auto_fix_high" size="xs" class="q-ml-sm" />
        </div>
      </q-btn>
    </div>
  </q-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useQuasar } from 'quasar';
import { getRoleConfig } from 'src/config/roles';

const $q = useQuasar();
const props = defineProps<{
  modelValue: { description: string; logs: string; context: string };
  role: string | null;
  loading: boolean;
}>();
const emit = defineEmits(['submit', 'update:modelValue']);

const config = computed(() => getRoleConfig(props.role));

const descriptionProxy = computed({
  get: () => props.modelValue.description,
  set: (val) => emit('update:modelValue', { ...props.modelValue, description: val }),
});
const logsProxy = computed({
  get: () => props.modelValue.logs,
  set: (val) => emit('update:modelValue', { ...props.modelValue, logs: val }),
});
const contextProxy = computed({
  get: () => props.modelValue.context,
  set: (val) => emit('update:modelValue', { ...props.modelValue, context: val }),
});
</script>

<style scoped>
.shadow-soft {
  box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.08);
}
.rounded-xl {
  border-radius: 24px;
}
.input-rounded :deep(.q-field__control) {
  border-radius: 12px;
}
.font-mono :deep(textarea) {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85em;
}
.hover-lift {
  transition: transform 0.2s;
}
.hover-lift:hover {
  transform: translateY(-2px);
}
.opacity-20 {
  opacity: 0.2;
}
.animate-fade-up {
  animation: fadeUp 0.6s ease-out;
}
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.shadow-dynamic {
  box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.2);
}
</style>
