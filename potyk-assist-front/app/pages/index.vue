<script lang="ts" setup>
const { data: beerArticles } = await useAsyncData(() =>
  queryCollection("content")
    .where("path", "like", "%beer%")
    .order("date", "DESC")
    .all(),
);
const { data: newsArticles } = await useAsyncData(() =>
  queryCollection("content")
    .where("path", "like", "%life%")
    .order("date", "DESC")
    .all(),
);
</script>

<template>
  <v-container>
    <div class="mb-8">
      <h1 class="text-center text-h2 font-weight-bold">
        <code>potyk.io</code>
      </h1>
      <div class="text-center font-italic">блог пустоты</div>
    </div>

    <v-alert
      style="margin: 8px 0"
      color="warning"
      variant="tonal"
      title="Пивные итоги 2025"
    >
      <template #append>
        <v-btn icon to="/beer/2025" variant="text">
          <v-icon icon="mdi-open-in-new"></v-icon>
        </v-btn>
      </template>
    </v-alert>

    <v-alert
      style="margin: 8px 0"
      color="success"
      variant="tonal"
      title="Юбик"
      text="      Прив. 5 лет пытаюсь вести блог, 5 лет бросаю это дело. Пора отметить это очередным блогом 😂."
    ></v-alert>

    <h2>Почитать</h2>
    <h3 class="my-6 text-h5 font-weight-bold">🍻 Пиво</h3>
    <blog-post-list :posts="beerArticles" />

    <h3 class="my-6 text-h5 font-weight-bold">📰 Лайф</h3>
    <blog-post-list :posts="newsArticles" />

    <h2>Посмотреть</h2>
    <vid-movie-list :editable="false" />
  </v-container>
</template>
