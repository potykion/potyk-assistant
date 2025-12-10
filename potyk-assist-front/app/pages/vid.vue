<script setup lang="ts">
interface Movie {
  id?: number
  image: string
  title: string
  why: string
  kinopoiskUrl: string
  downloadUrl: string
}

interface MovieServer {
  id?: number
  image: string
  title: string
  why: string
  kinopoisk_url: string
  download_url: string
}

const apiBaseUrl = import.meta.dev 
  ? 'http://127.0.0.1:5000' 
  : 'http://84.201.131.244:5000'

const snakeToCamel = (serverMovie: MovieServer): Movie => ({
  id: serverMovie.id,
  image: serverMovie.image,
  title: serverMovie.title,
  why: serverMovie.why,
  kinopoiskUrl: serverMovie.kinopoisk_url,
  downloadUrl: serverMovie.download_url
})

const camelToSnake = (movie: Movie): MovieServer => ({
  id: movie.id,
  image: movie.image,
  title: movie.title,
  why: movie.why,
  kinopoisk_url: movie.kinopoiskUrl,
  download_url: movie.downloadUrl
})

const { data: moviesData } = await useFetch<MovieServer[]>(`${apiBaseUrl}/movies`, {
  default: () => []
})

const movies = ref<Movie[]>((moviesData.value || []).map(snakeToCamel))

watch(moviesData, (newData) => {
  if (newData) {
    movies.value = newData.map(snakeToCamel)
  }
}, { immediate: true })

const dialog = ref(false)
const editingIndex = ref<number | null>(null)
const editingMovieId = ref<number | null>(null)
const formData = ref<Movie>({
  image: '',
  title: '',
  why: '',
  kinopoiskUrl: '',
  downloadUrl: ''
})

const openEditDialog = (index: number) => {
  editingIndex.value = index
  const movie = movies.value[index]
  if (movie) {
    editingMovieId.value = movie.id ?? null
    formData.value = {
      image: movie.image,
      title: movie.title,
      why: movie.why,
      kinopoiskUrl: movie.kinopoiskUrl,
      downloadUrl: movie.downloadUrl
    }
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  editingIndex.value = null
  editingMovieId.value = null
  formData.value = {
    image: '',
    title: '',
    why: '',
    kinopoiskUrl: '',
    downloadUrl: ''
  }
}

const saveMovie = async () => {
  if (editingMovieId.value === null) {
    closeDialog()
    return
  }

  try {
    const serverData = camelToSnake(formData.value)
    await $fetch(`${apiBaseUrl}/movies/${editingMovieId.value}`, {
      method: 'PUT',
      body: serverData
    })

    if (editingIndex.value !== null) {
      movies.value[editingIndex.value] = { ...formData.value, id: editingMovieId.value }
    }
    closeDialog()
  } catch (error) {
    console.error('Ошибка при сохранении фильма:', error)
  }
}
</script>

<template>

  <v-container>
    <h1>vid</h1>
    <cite>Всякие видики, фильмеры, картинки со звуком</cite>

    <h2>Kino</h2>

    <h3>Посмотреть позже</h3>
    <v-row>
      <v-col v-for="(movie, index) in movies" :key="movie.title" cols="3">
        <v-card class="movie-card">
          <v-img :src="movie.image" cover class="movie-image">
            <v-toolbar color="transparent" class="edit-toolbar">
              <template v-slot:append>
                <v-btn
                  icon="mdi-pencil"
                  @click="openEditDialog(index)"
                  variant="flat"
                  color="white"
                ></v-btn>
              </template>
            </v-toolbar>
          </v-img>

          <v-card-item>
            <v-card-title>{{ movie.title }}</v-card-title>
          </v-card-item>

          <v-card-text>
            <b>Почему?:</b> <span v-html="movie.why"></span>
          </v-card-text>

          <v-card-actions>
            <v-btn :href="movie.kinopoiskUrl">КП</v-btn>
            <v-btn :href="movie.downloadUrl">Скачать</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <h3>Где смотреть кино</h3>
        <ul>
          <li><b>Kinopub</b> - пиратский онлайн кинотеатр
            <ul>
              <li><a href="https://kinopub.zerkalo.live">Зеркало</a></li>
              <li><a href="https://t.me/c/1209124051/472">Телега</a> (как еще одно зеркало)</li>
            </ul>
          </li>
          <li>
            <b>Torrent streaming</b> - просмотр киношки с торрентов без ожидания скачивания
            <ul>
              <li><a href="https://github.com/hotheadhacker/seedbox-lite">seedbox</a></li>
              <li><a href="https://github.com/webtorrent/webtorrent">webtorrent</a></li>
            </ul>

          </li>
        </ul>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>Редактировать фильм</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="formData.image"
            label="URL изображения"
            variant="outlined"
            class="mb-3"
          ></v-text-field>
          <v-text-field
            v-model="formData.title"
            label="Название"
            variant="outlined"
            class="mb-3"
          ></v-text-field>
          <v-textarea
            v-model="formData.why"
            label="Почему?"
            variant="outlined"
            class="mb-3"
          ></v-textarea>
          <v-text-field
            v-model="formData.kinopoiskUrl"
            label="URL Кинопоиска"
            variant="outlined"
            class="mb-3"
          ></v-text-field>
          <v-text-field
            v-model="formData.downloadUrl"
            label="URL скачивания"
            variant="outlined"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveMovie">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>

</template>

<style scoped lang="sass">
.movie-card
  position: relative

  .edit-toolbar
    opacity: 0
    transition: opacity 0.2s ease-in-out

.movie-image:hover .edit-toolbar
  opacity: 1
</style>