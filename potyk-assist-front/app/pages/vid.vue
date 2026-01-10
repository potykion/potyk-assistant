<script setup lang="ts">
const showCreateDialog = ref(false);
const showArchiveDialog = ref(false);

const openCreateDialog = () => {
  showCreateDialog.value = true;
};

const openArchiveDialog = () => {
  showArchiveDialog.value = true;
};
</script>

<template>
  <v-container>
    <h1>vid</h1>
    <cite>Всякие видики, фильмеры, картинки со звуком</cite>

    <h2>Kino</h2>

    <div class="d-flex align-center justify-space-between mb-4">
      <h3 class="mr-4">Посмотреть позже</h3>
      <div class="d-flex gap-2">
        <v-btn
          icon="mdi-archive"
          color="secondary"
          @click="openArchiveDialog"
          variant="outlined"
        ></v-btn>
        <v-btn
          icon="mdi-plus"
          color="primary"
          @click="openCreateDialog"
          variant="outlined"
        ></v-btn>
      </div>
    </div>
    <vid-movie-list 
      :editable="true" 
      v-model:show-create-dialog="showCreateDialog"
      v-model:show-archive-dialog="showArchiveDialog"
    />

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

  </v-container>
</template>

