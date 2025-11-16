<script setup lang="ts">
const props = defineProps<{
  title: string
  artist: string
  year: string | number
  cover: string
  track: {
    title: string
    artist: string
    src: string
    cover?: string
  }
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
        :track="props.track"
        :playing="props.playing"
        @toggle="onToggle"
      ></mu-track>
    </v-card-text>
  </v-card>
</template>


