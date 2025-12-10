<script setup lang="ts">
interface Movie {
  image: string
  title: string
  why: string
  kinopoiskUrl: string
  downloadUrl: string
}

const movies = ref<Movie[]>([
  {
    image: 'https://avatars.mds.yandex.net/get-kinopoisk-image/1946459/2b9b671e-4558-4d08-b114-4d6ac79f26dd/3840x',
    title: 'Красивая работа',
    why: 'сигма-муви по мнению <a href="https://t.me/rzhavuykholodez/95">ржавого холодца</a>',
    kinopoiskUrl: 'https://www.kinopoisk.ru/film/119363/',
    downloadUrl: 'https://rutracker.org/forum/viewtopic.php?t=3010430/'
  }
])

const dialog = ref(false)
const editingIndex = ref<number | null>(null)
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
  formData.value = {
    image: '',
    title: '',
    why: '',
    kinopoiskUrl: '',
    downloadUrl: ''
  }
}

const saveMovie = () => {
  if (editingIndex.value !== null) {
    movies.value[editingIndex.value] = { ...formData.value }
  }
  closeDialog()
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