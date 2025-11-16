<script setup lang="ts">
import type { Album } from './mu-data'

const props = defineProps<{
  album: Album
  playing: boolean
}>()

const emit = defineEmits<{
  (e: 'toggle', src: string): void
}>()

const onToggle = (src: string) => {
  emit('toggle', src)
}
</script>

<template>
  <v-card >
    <v-img :src="props.album.cover" />

    <v-card-item>
      <v-card-title>{{ props.album.title }}</v-card-title>
      <v-card-subtitle>{{ props.album.artist }} • {{ props.album.year }}</v-card-subtitle>

      <template #append>
        <slot name="actions" />
      </template>
    </v-card-item>

    <v-divider />

    <v-card-text>
      <div class="font-italic">
        Highlighted track:
      </div>

      <mu-track
        :track="props.album.track"
        :playing="props.playing"
        @toggle="onToggle"
      />
    </v-card-text>
  </v-card>
</template>


