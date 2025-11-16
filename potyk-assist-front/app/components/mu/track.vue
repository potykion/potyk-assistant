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
    <template #prepend>
      <v-btn
        icon
        variant="text"
        size="small"
        @click.stop="onToggleClick"
      >
        <v-icon icon="mdi-play-pause" />
      </v-btn>
    </template>

    <v-list-item-title>{{ props.title }}</v-list-item-title>
    <v-list-item-subtitle>{{ props.artist }}</v-list-item-subtitle>
  </v-list-item>
</template>

<style scoped lang="sass">
</style>