<script setup lang="ts">
const props = defineProps<{
  title: string
  artist: string
  year: string | number
  cover: string
  trackTitle: string
  trackArtist: string
  trackSrc: string
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
  <v-card>
    <v-img :src="props.cover" />

    <v-card-item>
      <v-card-title>{{ props.title }}</v-card-title>
      <v-card-subtitle>{{ props.artist }} • {{ props.year }}</v-card-subtitle>

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
        :title="props.trackTitle"
        :artist="props.trackArtist"
        :src="props.trackSrc"
        :cover="props.cover"
        :playing="props.playing"
        @toggle="onToggle"
      />
    </v-card-text>
  </v-card>
</template>


