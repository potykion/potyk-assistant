<script setup lang="ts">
import type { Track } from './mu-data'

const props = defineProps<{
  track: Track
  playing: boolean
}>()

const emit = defineEmits<{
  (e: 'toggle', src: string): void
}>()

const onToggleClick = () => {
  emit('toggle', props.track.src)
}
</script>

<template>
  <v-list-item
    class="track-item"
    clickable
    rounded="lg"
    @click.stop.prevent="onToggleClick"
  >
    <template #prepend>
      <div class="track-cover-wrapper">
        <v-avatar>
          <v-img :src="props.track.cover" cover />
        </v-avatar>

        <v-btn
          class="track-play-btn"
          icon
          variant="text"
          size="small"
          @click.stop="onToggleClick"
        >
          <v-icon :icon="props.playing ? 'mdi-pause' : 'mdi-play'" color="white" />
        </v-btn>
      </div>
    </template>

    <v-list-item-title>{{ props.track.title }}</v-list-item-title>
    <v-list-item-subtitle>{{ props.track.artist }}</v-list-item-subtitle>
  </v-list-item>
</template>

<style scoped lang="sass">
.track-item :deep(.v-list-item__prepend)
  padding-right: 8px

.track-item
  padding-left: 4px
  padding-right: 4px

.track-cover-wrapper
  position: relative
  display: inline-flex

.track-play-btn
  position: absolute
  top: 50%
  left: 50%
  transform: translate(-50%, -50%)
  opacity: 0
  transition: opacity 0.15s ease

.track-item:hover .track-play-btn
  opacity: 1
</style>