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

const showCreateDialog = ref(false)
const formData = ref({
  title: '',
  artist: '',
  year: '',
  cover: '',
  link: '',
})
const form = ref<any>(null)

const requiredRule = (value: string) => {
  return !!value || "Поле обязательно для заполнения"
}

const openCreateDialog = () => {
  showCreateDialog.value = true
  formData.value = {
    title: '',
    artist: '',
    year: '',
    cover: '',
    link: '',
  }
}

const closeDialog = () => {
  showCreateDialog.value = false
  formData.value = {
    title: '',
    artist: '',
    year: '',
    cover: '',
    link: '',
  }
  form.value?.resetValidation()
}

const saveAlbum = async () => {
  const { valid } = await form.value.validate()
  if (!valid) {
    return
  }

  const album = {
    title: formData.value.title,
    artist: formData.value.artist,
    year: parseInt(formData.value.year),
    cover: formData.value.cover,
    link: formData.value.link || '',
  }

  console.log(album)
  closeDialog()
}
</script>

<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>mu</h1>
        <div class="d-flex align-center justify-space-between mb-4">
          <h2 class="mr-4">Featured</h2>
          <v-btn
            icon="mdi-plus"
            color="primary"
            @click="openCreateDialog"
            variant="outlined"
          ></v-btn>
        </div>
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

    <v-dialog v-model="showCreateDialog" max-width="600">
      <v-card>
        <v-card-title>Добавить альбом</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="formData.title"
              label="Название альбома"
              variant="outlined"
              class="mb-3"
              :rules="[requiredRule]"
            ></v-text-field>
            <v-text-field
              v-model="formData.artist"
              label="Исполнитель"
              variant="outlined"
              class="mb-3"
              :rules="[requiredRule]"
            ></v-text-field>
            <v-text-field
              v-model="formData.year"
              label="Год"
              variant="outlined"
              class="mb-3"
              type="number"
              :rules="[requiredRule]"
            ></v-text-field>
            <v-text-field
              v-model="formData.cover"
              label="Ссылка на обложку"
              variant="outlined"
              class="mb-3"
              :rules="[requiredRule]"
            ></v-text-field>
            <v-text-field
              v-model="formData.link"
              label="Ссылка на прослушивание"
              variant="outlined"
              hint="Опционально"
              persistent-hint
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveAlbum">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<style scoped lang="sass">

</style>