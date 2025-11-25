<script setup lang="ts">
import {ref} from 'vue'
import {featuredAlbums, listenLaterAlbums} from '../../components/mu/mu-data'

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

const {data: genreArticles} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%genres%").order("date", "DESC").all()
)
</script>

<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>mu</h1>
        <h2>Featured</h2>

      </v-col>
    </v-row>
    <v-row>
      <v-col
          v-for="album in featuredAlbums"
          :key="album.id"
          cols="3"
      >
        <mu-album
            :album="album"
            :playing="album.track && playingSrc === album.track.src"
            @toggle="toggleTrack"
        >
        </mu-album>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <h2>Listen Later</h2>

      </v-col>
    </v-row>
    <v-row>
      <v-col
          v-for="album in listenLaterAlbums"
          :key="album.id"
          cols="3"
      >
        <mu-album
            :album="album"
            :playing="album.track &&  playingSrc === album.track.src"
            @toggle="toggleTrack"
        >
        </mu-album>
      </v-col>
    </v-row>

  <v-row>
      <v-col>
            <h2>Genres</h2>



        <blog-post-list :posts="genreArticles" :show-date="false"/>

      </v-col>
    </v-row>



    <audio ref="audioRef"></audio>

  </v-container>
</template>

<style scoped lang="sass">

</style>