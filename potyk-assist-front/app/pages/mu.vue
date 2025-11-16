<script setup lang="ts">
import {ref} from 'vue'

type FeaturedAlbum = {
  id: string
  title: string
  artist: string
  year: number
  cover: string
  link: string
  track: {
    title: string
    artist: string
    src: string
  }
}

const featuredAlbums: FeaturedAlbum[] = [
  {
    id: 'londinium',
    title: 'Londinium',
    artist: 'Archive',
    year: 1996,
    cover: 'https://avatars.yandex.net/get-music-content/49876/cbf41616.a.89962-1/600x600',
    link: 'https://music.yandex.ru/album/89962',
    track: {
      title: 'So Few Words',
      artist: 'Archive',
      src: '/Archive%20-%20So%20Few%20Words.mp3',
    },
  },
]

const audioRef = ref<HTMLAudioElement | null>(null)
const currentSrc = ref<string | null>(null)
const playingSrc = ref<string | null>(null)

const toggleTrack = (src: string) => {
  const audio = audioRef.value
  if (!audio) return

  // if another track selected – switch and play from start
  if (currentSrc.value !== src) {
    currentSrc.value = src
    audio.src = src
    audio.currentTime = 0
    void audio.play()
    playingSrc.value = src
    return
  }

  // same track – toggle play/pause
  if (audio.paused) {
    void audio.play()
    playingSrc.value = src
  } else {
    audio.pause()
    playingSrc.value = null
  }
}
</script>

<template>
  <v-container>
    <h1>mu</h1>
    <h2>Featured</h2>

    <!-- глобальный аудиоплеер, общий для всех альбомов на странице -->
    <audio ref="audioRef"></audio>

    <v-row>
      <v-col
        v-for="album in featuredAlbums"
        :key="album.id"
        cols="3"
      >
        <mu-album
          :title="album.title"
          :artist="album.artist"
          :year="album.year"
          :cover="album.cover"
          :track-title="album.track.title"
          :track-artist="album.track.artist"
          :track-src="album.track.src"
          :playing="playingSrc === album.track.src"
          @toggle="toggleTrack"
        >
          <template #actions>
            <v-btn
              icon
              variant="text"
              size="small"
              :href="album.link"
              target="_blank"
              @click.stop
            >
              <v-icon icon="mdi-open-in-new" />
            </v-btn>
          </template>
        </mu-album>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped lang="sass">

</style>