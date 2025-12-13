<script setup lang="ts">
interface Movie {
  id?: number;
  image: string;
  title: string;
  why: string;
  kinopoiskUrl: string;
  downloadUrl: string;
  watchUrl?: string;
}

interface MovieServer {
  id?: number;
  image: string;
  title: string;
  why: string;
  kinopoisk_url: string;
  download_url: string;
  watch_url?: string;
}

const apiBaseUrl = import.meta.dev
  ? "http://127.0.0.1:5000"
  : "http://84.201.131.244:5000";

const snakeToCamel = (serverMovie: MovieServer): Movie => ({
  id: serverMovie.id,
  image: serverMovie.image,
  title: serverMovie.title,
  why: serverMovie.why,
  kinopoiskUrl: serverMovie.kinopoisk_url,
  downloadUrl: serverMovie.download_url,
  watchUrl: serverMovie.watch_url,
});

const camelToSnake = (movie: Movie): MovieServer => ({
  id: movie.id,
  image: movie.image,
  title: movie.title,
  why: movie.why,
  kinopoisk_url: movie.kinopoiskUrl,
  download_url: movie.downloadUrl,
  watch_url: movie.watchUrl,
});

const { data: moviesData, refresh: refreshMovies } = await useFetch<
  MovieServer[]
>(`${apiBaseUrl}/movies`, {
  default: () => [],
});

const movies = ref<Movie[]>((moviesData.value || []).map(snakeToCamel));

watch(
  moviesData,
  (newData) => {
    if (newData) {
      movies.value = newData.map(snakeToCamel);
    }
  },
  { immediate: true },
);

const dialog = ref(false);
const isCreating = ref(false);
const editingIndex = ref<number | null>(null);
const editingMovieId = ref<number | null>(null);
const formData = ref<Movie>({
  image: "",
  title: "",
  why: "",
  kinopoiskUrl: "",
  downloadUrl: "",
  watchUrl: "",
});
const form = ref<any>(null);

const requiredRule = (value: string) => {
  return !!value || "Поле обязательно для заполнения";
};

const urlRule = (value: string) => {
  const downloadUrl = formData.value.downloadUrl?.trim() || "";
  const watchUrl = formData.value.watchUrl?.trim() || "";
  if (!downloadUrl && !watchUrl) {
    return "Должен быть заполнен хотя бы один URL (скачивания или просмотра)";
  }
  return true;
};

const openCreateDialog = () => {
  isCreating.value = true;
  editingIndex.value = null;
  editingMovieId.value = null;
  formData.value = {
    image: "",
    title: "",
    why: "",
    kinopoiskUrl: "",
    downloadUrl: "",
    watchUrl: "",
  };
  dialog.value = true;
};

const openEditDialog = (index: number) => {
  isCreating.value = false;
  editingIndex.value = index;
  const movie = movies.value[index];
  if (movie) {
    editingMovieId.value = movie.id ?? null;
    formData.value = {
      image: movie.image,
      title: movie.title,
      why: movie.why,
      kinopoiskUrl: movie.kinopoiskUrl,
      downloadUrl: movie.downloadUrl,
      watchUrl: movie.watchUrl ?? "",
    };
  }
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  isCreating.value = false;
  editingIndex.value = null;
  editingMovieId.value = null;
  formData.value = {
    image: "",
    title: "",
    why: "",
    kinopoiskUrl: "",
    downloadUrl: "",
    watchUrl: "",
  };
  form.value?.resetValidation();
};

const saveMovie = async () => {
  const { valid } = await form.value.validate();
  if (!valid) {
    return;
  }

  try {
    const serverData = camelToSnake(formData.value);

    if (isCreating.value) {
      await $fetch(`${apiBaseUrl}/movies`, {
        method: "POST",
        body: serverData,
      });
      await refreshMovies();
    } else {
      if (editingMovieId.value === null) {
        closeDialog();
        return;
      }

      await $fetch(`${apiBaseUrl}/movies/${editingMovieId.value}`, {
        method: "PUT",
        body: serverData,
      });

      if (editingIndex.value !== null) {
        movies.value[editingIndex.value] = {
          ...formData.value,
          id: editingMovieId.value,
        };
      }
    }
    closeDialog();
  } catch (error) {
    console.error("Ошибка при сохранении фильма:", error);
  }
};
</script>

<template>
  <v-container>
    <h1>vid</h1>
    <cite>Всякие видики, фильмеры, картинки со звуком</cite>

    <h2>Kino</h2>

    <div class="d-flex align-center justify-space-between mb-4">
      <h3 class="mr-4">Посмотреть позже</h3>
      <v-btn
        icon="mdi-plus"
        color="primary"
        @click="openCreateDialog"
        variant="outlined"
      ></v-btn>
    </div>
    <v-row>
      <v-col v-for="(movie, index) in movies" :key="movie.title" cols="3">
        <v-card class="movie-card">
          <v-img :src="movie.image" cover class="movie-image" height="400">
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

          <v-card-text class="movie-why">
            <div class="movie-why-content">
              <b>Почему?:</b> <span v-html="movie.why"></span>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn v-if="movie.kinopoiskUrl" :href="movie.kinopoiskUrl"
              >КП</v-btn
            >
            <v-btn v-if="movie.downloadUrl" :href="movie.downloadUrl"
              >Скачать</v-btn
            >
            <v-btn v-if="movie.watchUrl" :href="movie.watchUrl">Смотреть</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <h3>Где смотреть кино</h3>
        <ul>
          <li>
            <b>Kinopub</b> - пиратский онлайн кинотеатр
            <ul>
              <li><a href="https://kinopub.zerkalo.live">Зеркало</a></li>
              <li>
                <a href="https://t.me/c/1209124051/472">Телега</a> (как еще одно
                зеркало)
              </li>
            </ul>
          </li>
          <li>
            <b>Torrent streaming</b> - просмотр киношки с торрентов без ожидания
            скачивания
            <ul>
              <li>
                <a href="https://github.com/hotheadhacker/seedbox-lite"
                  >seedbox</a
                >
              </li>
              <li>
                <a href="https://github.com/webtorrent/webtorrent"
                  >webtorrent</a
                >
              </li>
            </ul>
          </li>
        </ul>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{
          isCreating ? "Добавить фильм" : "Редактировать фильм"
        }}</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="formData.title"
              label="Название"
              variant="outlined"
              class="mb-3"
              :rules="[requiredRule]"
            ></v-text-field>
            <v-text-field
              v-model="formData.image"
              label="URL изображения"
              variant="outlined"
              class="mb-3"
              :rules="[requiredRule]"
            ></v-text-field>

            <v-textarea
              v-model="formData.why"
              label="Почему?"
              variant="outlined"
              class="mb-3"
              :rules="[requiredRule]"
            ></v-textarea>
            <v-text-field
              v-model="formData.kinopoiskUrl"
              label="URL Кинопоиска"
              variant="outlined"
              class="mb-3"
              :rules="[requiredRule]"
            ></v-text-field>
            <v-text-field
              v-model="formData.downloadUrl"
              label="URL скачивания"
              variant="outlined"
              class="mb-3"
              :rules="[urlRule]"
            ></v-text-field>
            <v-text-field
              v-model="formData.watchUrl"
              label="URL просмотра"
              variant="outlined"
              :rules="[urlRule]"
            ></v-text-field>
          </v-form>
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
  display: flex
  flex-direction: column

  .edit-toolbar
    opacity: 0
    transition: opacity 0.2s ease-in-out

  .movie-why
    height: 4.5em
    overflow: hidden

  .movie-why-content
    line-height: 1.5em
    max-height: 3em
    overflow: hidden
    display: block

.movie-image:hover .edit-toolbar
  opacity: 1
</style>
