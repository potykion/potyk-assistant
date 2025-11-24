<script setup lang="ts">

</script>

<template>

  <v-container>
    <h1>vid</h1>
    <cite>Всякие видики, фильмеры, картинки со звуком</cite>

    <h2>Kino</h2>

    <h3>Посмотреть позже</h3>
    <v-row>
      <v-col cols="3">
        <v-card>
          <v-img
              src="https://avatars.mds.yandex.net/get-kinopoisk-image/1946459/2b9b671e-4558-4d08-b114-4d6ac79f26dd/3840x"/>

          <v-card-item>
            <v-card-title>Красивая работа</v-card-title>


          </v-card-item>


          <v-card-text>
            <b>Почему?:</b> сигма-муви по мнению <a href="https://t.me/rzhavuykholodez/95">ржавого холодца</a>


          </v-card-text>

          <v-card-actions>
            <v-btn href="https://www.kinopoisk.ru/film/119363/">КП</v-btn>
            <v-btn href="https://rutracker.org/forum/viewtopic.php?t=3010430/">Скачать</v-btn>
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
  </v-container>

</template>

<style scoped lang="sass">

</style>