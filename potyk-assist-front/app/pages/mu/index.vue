<script setup lang="ts">
import {ref, computed} from 'vue'
import type {Album} from '../../components/mu/mu-data'
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

const apiBaseUrl = import.meta.dev
  ? "http://127.0.0.1:5000"
  : "http://84.201.131.244:5000"

interface AlbumApi {
  id: number
  title: string
  artist: string
  year: number
  cover: string
  link: string | null
}

interface TagApi {
  id: number
  title: string
  entity_type: string
}

const {data: albumsData, refresh: refreshAlbums} = await useFetch<AlbumApi[]>(
  `${apiBaseUrl}/albums`,
  {
    default: () => [],
  }
)

const {data: tagsData} = await useFetch<TagApi[]>(
  `${apiBaseUrl}/tags?entity_type=mu_album`,
  {
    default: () => [],
  }
)

const apiAlbums = computed<Album[]>(() => {
  return (albumsData.value || []).map((album) => ({
    id: String(album.id),
    title: album.title,
    artist: album.artist,
    year: album.year,
    cover: album.cover,
    link: album.link || '',
    track: null,
  }))
})

const allFeaturedAlbums = computed(() => {
  return [...featuredAlbums, ...apiAlbums.value]
})

const showCreateDialog = ref(false)
const isCreating = ref(true)
const editingAlbumId = ref<number | null>(null)
const formData = ref({
  title: '',
  artist: '',
  year: '',
  cover: '',
  link: '',
  tags: [] as TagApi[],
})
const form = ref<any>(null)

const requiredRule = (value: string) => {
  return !!value || "Поле обязательно для заполнения"
}

const openCreateDialog = () => {
  isCreating.value = true
  editingAlbumId.value = null
  showCreateDialog.value = true
  formData.value = {
    title: '',
    artist: '',
    year: '',
    cover: '',
    link: '',
    tags: [],
  }
}

const openEditDialog = (albumId: number) => {
  const album = apiAlbums.value.find(a => Number(a.id) === albumId)
  if (!album) return
  
  isCreating.value = false
  editingAlbumId.value = albumId
  showCreateDialog.value = true
  formData.value = {
    title: album.title,
    artist: album.artist,
    year: String(album.year),
    cover: album.cover,
    link: album.link || '',
  }
}

const closeDialog = () => {
  showCreateDialog.value = false
  isCreating.value = true
  editingAlbumId.value = null
  formData.value = {
    title: '',
    artist: '',
    year: '',
    cover: '',
    link: '',
    tags: [],
  }
  form.value?.resetValidation()
}

const saveAlbum = async () => {
  const { valid } = await form.value.validate()
  if (!valid) {
    return
  }

  try {
    const album = {
      title: formData.value.title,
      artist: formData.value.artist,
      year: parseInt(formData.value.year),
      cover: formData.value.cover,
      link: formData.value.link || null,
    }

    if (isCreating.value) {
      await $fetch(`${apiBaseUrl}/albums`, {
        method: "POST",
        body: album,
      })
    } else {
      if (editingAlbumId.value === null) {
        closeDialog()
        return
      }
      await $fetch(`${apiBaseUrl}/albums/${editingAlbumId.value}`, {
        method: "PUT",
        body: album,
      })
    }
    
    await refreshAlbums()
    closeDialog()
  } catch (error) {
    console.error("Ошибка при сохранении альбома:", error)
  }
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
          v-for="album in allFeaturedAlbums"
          :key="album.id"
          cols="3"
      >
        <mu-album
            :album="album"
            :playing="album.track && playingSrc === album.track.src"
            :editable="!!apiAlbums.find(a => a.id === album.id)"
            @toggle="toggleTrack"
            @edit="openEditDialog"
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
        <v-card-title>{{ isCreating ? "Добавить альбом" : "Редактировать альбом" }}</v-card-title>
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
              class="mb-3"
            ></v-text-field>
            <v-autocomplete
              v-model="formData.tags"
              :items="tagsData || []"
              item-title="title"
              item-value="id"
              label="Теги"
              variant="outlined"
              multiple
              chips
              closable-chips
              hint="Опционально"
              persistent-hint
            ></v-autocomplete>
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