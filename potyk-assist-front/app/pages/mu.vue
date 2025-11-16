<script setup lang="ts">
import { ref } from 'vue'

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

    <v-row>
      <v-col cols="3">
        <div>
          <v-img src="https://avatars.yandex.net/get-music-content/49876/cbf41616.a.89962-1/600x600"></v-img>
          <div class="font-weight-bold text-h6">Londinium</div>
          <div class="text-subtitle-2">Archive • 1996</div>

          <div class="text-subtitle-2 font-italic">
            Highlighted track:
          </div>

          <audio
            ref="audioRef"
          ></audio>

          <mu-track
            title="So Few Words"
            artist="Londinium"
            src="/Archive%20-%20So%20Few%20Words.mp3"
            cover="https://avatars.yandex.net/get-music-content/49876/cbf41616.a.89962-1/600x600"
            :playing="playingSrc === '/Archive%20-%20So%20Few%20Words.mp3'"
            @toggle="toggleTrack"
          ></mu-track>
        </div>
      </v-col>
    </v-row>

  </v-container>

</template>

<style scoped lang="sass">

</style>