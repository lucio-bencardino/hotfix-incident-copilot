<template>
  <q-layout view="hHh lpR fFf" class="my-bg-page">
    <div class="fixed-top z-max row justify-center q-pt-md pointer-events-none">
      <div
        class="glass-pill row items-center q-px-lg q-py-sm shadow-2 pointer-events-auto"
        :class="$q.dark.isActive ? 'glass-dark' : 'glass-light'"
      >
        <q-icon name="bolt" color="amber-5" size="sm" class="q-mr-sm" />
        <div class="text-subtitle1 text-weight-bold tracking-wide gt-xs">
          Incident<span class="text-primary">Copilot</span>
        </div>

        <div class="q-mx-md text-caption row items-center text-muted">
          <div class="status-dot q-mr-xs" :class="backendAlive ? 'bg-positive' : 'bg-grey-4'"></div>
          <span v-if="backendAlive" class="gt-xs">v{{ backendVersion }}</span>
        </div>

        <q-separator vertical class="q-mx-sm" />

        <div class="row q-gutter-x-sm">
          <q-btn
            flat
            round
            dense
            :icon="$q.dark.isActive ? 'light_mode' : 'dark_mode'"
            :color="$q.dark.isActive ? 'yellow' : 'grey-7'"
            @click="$q.dark.toggle()"
          >
            <q-tooltip>Theme</q-tooltip>
          </q-btn>

          <q-btn
            flat
            round
            dense
            icon="history"
            color="primary"
            @click="rightDrawerOpen = !rightDrawerOpen"
          >
            <q-badge v-if="history.length" color="red" floating rounded dot />
            <q-tooltip>History</q-tooltip>
          </q-btn>
        </div>
      </div>
    </div>

    <q-drawer
      v-model="rightDrawerOpen"
      side="right"
      overlay
      behavior="mobile"
      class="my-surface"
      :class="$q.dark.isActive ? 'bg-grey-10' : 'bg-white'"
      bordered
    >
      <div class="column full-height q-pa-md">
        <div class="text-h6 text-weight-bold q-mb-md text-main">Recent Plans</div>

        <div v-if="history.length === 0" class="text-center text-muted q-mt-xl">
          <q-icon name="history_toggle_off" size="xl" class="opacity-20 q-mb-sm" />
          <div>No history yet.</div>
        </div>

        <q-list separator class="scroll col">
          <q-item
            v-for="item in history"
            :key="item.id"
            clickable
            v-ripple
            class="rounded-borders q-my-sm"
            @click="restoreAndClose(item)"
          >
            <q-item-section avatar>
              <q-icon
                :name="item.role === 'dev' ? 'code' : 'dns'"
                :color="item.role === 'dev' ? 'accent' : 'secondary'"
              />
            </q-item-section>

            <q-item-section>
              <q-item-label class="text-weight-medium text-main text-body2 ellipsis-2-lines">
                {{ item.description || 'No description' }}
              </q-item-label>
              <q-item-label caption class="text-muted">
                {{ formatDate(item.date) }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>

        <q-btn
          v-if="history.length"
          outline
          color="negative"
          label="Clear History"
          class="q-mt-md"
          size="sm"
          @click="clear"
        />
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useQuasar, date } from 'quasar';
import { useHistory, type HistoryItem } from 'src/composables/useHistory';
import { IncidentService } from 'src/services/IncidentService';

const $q = useQuasar();
const backendVersion = ref('');
const backendAlive = ref(false);

const rightDrawerOpen = ref(false);
const { load, history, clear, restore } = useHistory();

const formatDate = (ts: number) => {
  return date.formatDate(ts, 'DD/MM HH:mm');
};

const restoreAndClose = (item: HistoryItem) => {
  restore(item);
  rightDrawerOpen.value = false;
  $q.notify({
    message: 'Plan restored from history',
    icon: 'restore',
    color: 'primary',
    position: 'bottom',
  });
};

const initTheme = () => {
  const savedTheme = $q.localStorage.getItem('isDark');

  if (savedTheme !== null) {
    $q.dark.set(!!savedTheme);
  } else {
    $q.dark.set('auto');
  }
};
watch(
  () => $q.dark.isActive,
  (val) => $q.localStorage.set('isDark', val),
);

onMounted(async () => {
  initTheme();
  load();

  try {
    const data = await IncidentService.checkHealth();
    backendVersion.value = data.version;
    backendAlive.value = true;
  } catch (e) {
    console.warn('Backend fail', e);
    backendAlive.value = false;
  }
});
</script>

<style scoped>
.ellipsis-2-lines {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.pointer-events-none {
  pointer-events: none;
}
.pointer-events-auto {
  pointer-events: auto;
}

.glass-pill {
  backdrop-filter: blur(12px);
  border-radius: 50px;
  transition: all 0.3s ease;
}
.glass-light {
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.6);
}
.glass-dark {
  background: rgba(30, 41, 59, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
}

.border-left {
  border-left: 1px solid var(--border-color);
}
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
</style>
