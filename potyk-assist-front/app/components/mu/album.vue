<script setup lang="ts">
import type {Album} from './mu-data'

const props = defineProps<{
  album: Album
  playing: boolean
  editable?: boolean
}>()

const emit = defineEmits<{
  (e: 'toggle', src: string): void
  (e: 'edit', albumId: number): void
}>()

const onToggle = (src: string) => {
  emit('toggle', src)
}

const onEdit = () => {
  if (props.album.id && typeof props.album.id === 'string') {
    const albumId = Number(props.album.id)
    if (!isNaN(albumId)) {
      emit('edit', albumId)
    }
  }
}
</script>

<template>
  <v-card>
    <v-img :src="props.album.cover" class="album-image">
      <v-toolbar v-if="editable" color="transparent" class="edit-toolbar">
        <template v-slot:append>
          <v-btn
            icon="mdi-pencil"
            @click="onEdit"
            variant="flat"
            color="white"
          ></v-btn>
        </template>
      </v-toolbar>
    </v-img>

    <v-card-item>
      <v-card-title class="text-subtitle-1	font-weight-semibold">{{ props.album.title }}</v-card-title>
      <v-card-subtitle>{{ props.album.artist }} • {{ props.album.year }}</v-card-subtitle>

      <template #append>
        <v-btn
            icon
            variant="text"
            size="small"
            :href="props.album.link"
            target="_blank"
            @click.stop
        >
          <v-icon icon="mdi-open-in-new"/>
        </v-btn>
      </template>
    </v-card-item>

    <template v-if="props.album.track">
      <v-divider/>

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

    </template>
  </v-card>
</template>

<style scoped lang="sass">
.album-image
  position: relative

  .edit-toolbar
    opacity: 0
    transition: opacity 0.2s ease-in-out

.album-image:hover .edit-toolbar
  opacity: 1
</style>

