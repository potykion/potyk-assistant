<script setup lang="ts">
const props = defineProps<{
  title: string
  artist: string
  src: string
}>()

const emit = defineEmits<{
  (e: 'toggle', src: string): void
}>()

const onToggleClick = () => {
  emit('toggle', props.src)
}
</script>

<template>
  <v-list-item>
    <v-list-item-title>{{ props.title }}</v-list-item-title>
    <v-list-item-subtitle>{{ props.artist }}</v-list-item-subtitle>

    <template #append>
      <v-btn size="small" variant="text" @click.stop="onToggleClick">
        Play / Pause
      </v-btn>
    </template>
  </v-list-item>
</template>

<style scoped lang="sass">
</style>