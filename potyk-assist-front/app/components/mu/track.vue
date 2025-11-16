<script setup lang="ts">
const props = defineProps<{
  title: string
  artist: string
  src: string
  cover: string
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
    @click.stop.prevent="onToggleClick"
  >
    <template #prepend>
      <div class="track-cover-wrapper">
        <v-avatar >
          <v-img :src="props.cover" cover />
        </v-avatar>

        <v-btn
          class="track-play-btn"
          icon
          variant="text"
          size="small"
          @click.stop="onToggleClick"
        >
          <v-icon
            :icon="props.playing ? 'mdi-pause' : 'mdi-play'"
            color="white"
          />
        </v-btn>
      </div>
    </template>

    <v-list-item-title>{{ props.title }}</v-list-item-title>
    <v-list-item-subtitle>{{ props.artist }}</v-list-item-subtitle>
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