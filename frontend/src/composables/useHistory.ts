import { ref } from 'vue';
import { useQuasar } from 'quasar';
import type { IncidentPlan } from 'src/services/IncidentService';

export interface HistoryItem {
  id: string;
  date: number;
  role: string;
  description: string;
  form: { description: string; logs: string; context: string };
  plan: IncidentPlan;
  checkedSteps: boolean[];
}

const HISTORY_KEY = 'incident_history';

const history = ref<HistoryItem[]>([]);
const activeItem = ref<HistoryItem | null>(null);

export function useHistory() {
  const $q = useQuasar();

  const load = () => {
    const saved = $q.localStorage.getItem(HISTORY_KEY);
    if (saved) {
      history.value = saved as HistoryItem[];
    }
  };

  const save = (
    role: string,
    form: { description: string; logs: string; context: string },
    plan: IncidentPlan
  ): string => {
    const id = crypto.randomUUID();

    const newItem: HistoryItem = {
      id,
      date: Date.now(),
      role,
      description: form.description.substring(0, 50) + (form.description.length > 50 ? '...' : ''),
      form: { ...form },
      plan,
      checkedSteps: new Array(plan.steps.length).fill(false)
    };

    history.value = [newItem, ...history.value].slice(0, 20);
    $q.localStorage.set(HISTORY_KEY, history.value);

    return id;
  };

  const updateProgress = (id: string, checks: boolean[]) => {
    const item = history.value.find(h => h.id === id);

    if (item) {
      item.checkedSteps = checks;
      $q.localStorage.set(HISTORY_KEY, history.value);
    }
  };

  const restore = (item: HistoryItem) => {
    activeItem.value = item;
  };

  const clear = () => {
    history.value = [];
    $q.localStorage.remove(HISTORY_KEY);
  };

  return {
    history,
    activeItem,
    load,
    save,
    updateProgress,
    restore,
    clear
  };
}