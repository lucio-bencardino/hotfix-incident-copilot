<template>
  <div class="q-mt-xl animate-fade-up">
    <div class="text-h5 text-weight-bold q-mb-md flex items-center text-main">
      <q-icon name="checklist" :color="config.color" class="q-mr-sm" />
      {{ texts.titles.plan }}
    </div>

    <q-banner
      v-if="plan.warnings?.length"
      rounded
      class="q-mb-md border-amber"
      :class="$q.dark.isActive ? 'bg-amber-10 text-black' : 'bg-amber-1 text-amber-10'"
    >
      <template v-slot:avatar>
        <q-icon name="warning" :color="$q.dark.isActive ? 'black' : 'amber-9'" />
      </template>
      <div class="text-weight-medium">{{ texts.titles.warnings }}</div>
      <ul class="q-my-none q-pl-md">
        <li v-for="(w, i) in plan.warnings" :key="i" v-html="renderMarkdown(w)"></li>
      </ul>
    </q-banner>

    <div class="my-surface rounded-xl q-pa-sm">
      <q-list separator :dark="$q.dark.isActive">
        <q-item
          v-for="(step, i) in plan.steps"
          :key="i"
          tag="label"
          v-ripple
          class="q-py-md rounded-borders"
        >
          <q-item-section avatar top>
            <q-checkbox
              v-model="checkedSteps[i]"
              :color="config.color"
              size="md"
              :dark="$q.dark.isActive"
            />
          </q-item-section>

          <q-item-section>
            <q-item-label
              class="text-body1"
              :class="checkedSteps[i] ? 'text-strike text-muted' : 'text-main'"
            >
              <span class="markdown-content" v-html="renderMarkdown(step)"></span>
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </div>

    <div class="row justify-end q-mt-md">
      <q-btn
        flat
        icon="content_copy"
        :label="texts.actions.copy"
        class="text-muted hover-text-main"
        @click="copyToClipboard"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { useQuasar, copyToClipboard as qCopy } from 'quasar';
import MarkdownIt from 'markdown-it';
import { UI_TEXT } from 'src/constants/text';
import { getRoleConfig } from 'src/config/roles';
import type { IncidentPlan } from 'src/services/IncidentService';

const props = defineProps<{
  plan: IncidentPlan;
  role: string | null;
  savedChecks?: boolean[];
}>();

const emit = defineEmits(['update:progress']);

const texts = UI_TEXT;
const $q = useQuasar();
const checkedSteps = ref<boolean[]>([]);
const md = new MarkdownIt({ linkify: true, breaks: true });

const config = computed(() => getRoleConfig(props.role));

watch(
  () => props.plan,
  (newPlan) => {
    if (!newPlan?.steps) return;

    if (props.savedChecks && props.savedChecks.length === newPlan.steps.length) {
      checkedSteps.value = [...props.savedChecks];
    } else {
      checkedSteps.value = new Array(newPlan.steps.length).fill(false);
    }
  },
  { immediate: true },
);

watch(
  checkedSteps,
  (newVal) => {
    emit('update:progress', newVal);
  },
  { deep: true },
);

const renderMarkdown = (text: string) => md.renderInline(text);

const copyToClipboard = () => {
  const text = `**INCIDENT PLAN**\n\n` + props.plan.steps.map((s) => `[ ] ${s}`).join('\n');
  qCopy(text)
    .then(() => $q.notify({ type: 'positive', message: 'Copied!', icon: 'check' }))
    .catch(() => $q.notify({ type: 'negative', message: 'Failed to copy' }));
};
</script>

<style scoped>
.rounded-xl {
  border-radius: 24px;
}
.border-amber {
  border: 1px solid #fcd34d;
}
.text-strike {
  text-decoration: line-through;
  opacity: 0.6;
}
.hover-text-main {
  transition: color 0.3s;
}
.hover-text-main:hover {
  color: var(--text-main) !important;
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

:deep(.markdown-content code) {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9em;
  padding: 0.2em 0.4em;
  border-radius: 6px;
  background-color: rgba(0, 0, 0, 0.06);
  color: #d63384;
}
:global(body.body--dark) :deep(.markdown-content code) {
  background-color: rgba(255, 255, 255, 0.15);
  color: #ff79c6;
}
</style>
