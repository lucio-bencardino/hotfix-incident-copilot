<template>
  <div class="column items-center q-gutter-y-xl animate-fade-in">
    <div class="text-center">
      <h1 class="text-h3 text-weight-bold q-mb-sm text-main">Who is fixing this?</h1>
      <p class="text-subtitle1 text-muted">Select your expert persona to tune the AI model.</p>
    </div>

    <div class="row q-gutter-xl justify-center full-width">
      <div
        v-for="role in rolesList"
        :key="role.id"
        class="role-card cursor-pointer relative-position my-surface"
        @click="$emit('select', role.id)"
        v-ripple
      >
        <div class="icon-circle" :class="getBgClass(role)">
          <q-icon :name="role.icon" size="md" :color="role.color" />
        </div>

        <div class="text-h6 text-weight-bold q-mt-md text-main">{{ role.title }}</div>
        <p class="text-caption text-muted text-center q-mt-sm">{{ role.subtitle }}</p>

        <div class="card-indicator" :class="`bg-${role.color}`"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar';
import { getRolesList, type RoleDefinition } from 'src/config/roles';

const $q = useQuasar();
const rolesList = getRolesList();
defineEmits(['select']);

const getBgClass = (role: RoleDefinition) => {
  return $q.dark.isActive ? 'bg-grey-9' : role.bgClass;
};
</script>

<style scoped>
.role-card {
  width: 240px;
  height: 260px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition:
    transform 0.3s,
    box-shadow 0.3s;
  overflow: hidden;
}
.role-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}
.icon-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  transition: all 0.3s;
}
.card-indicator {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 6px;
  opacity: 0;
  transition: opacity 0.3s;
}
.role-card:hover .card-indicator {
  opacity: 1;
}
</style>
