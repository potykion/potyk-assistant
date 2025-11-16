<script setup lang="ts">
const props = defineProps<{
  title: string
  artist: string
  src: string
  playing: boolean
}>()

const emit = defineEmits<{
  (e: 'toggle', src: string): void
}>()

const onToggleClick = () => {
  emit('toggle', props.src)
}
</script>

<template>
  <v-list-item
    class="track-item"
    clickable
    rounded="lg"
    density="compact"
    @click="onToggleClick"
  >
    <template #prepend>
      <v-btn
        icon
        variant="text"
        size="small"
        @click.stop="onToggleClick"
      >
        <v-icon :icon="props.playing ? 'mdi-pause' : 'mdi-play'" />
      </v-btn>
    </template>

    <v-list-item-title>{{ props.title }}</v-list-item-title>
    <v-list-item-subtitle>{{ props.artist }}</v-list-item-subtitle>
  </v-list-item>
</template>

<style scoped lang="sass">
.track-item
  padding-left: 0 !important
  padding-right: 0 !important
</style>