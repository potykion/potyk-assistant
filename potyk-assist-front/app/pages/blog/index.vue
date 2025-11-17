<script setup lang="ts">
const {data: beerArticles} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%beer%").order("date", "DESC").all()
)
const {data: newsArticles} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%news%").order("date", "DESC").all()
)

</script>

<template>
  <v-container>
    <h1>Блог</h1>

    <h2>📰 Новости</h2>
    <blog-post-list :posts="newsArticles" />
    <h2>🍻 Пиво</h2>
    <blog-post-list :posts="beerArticles"  />

  </v-container>
</template>
