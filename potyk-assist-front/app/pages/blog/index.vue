<script setup lang="ts">
const {data: beerArticles} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%beer%").order("date", "DESC").all()
)
const {data: newsArticles} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%life%").order("date", "DESC").all()
)

</script>

<template>
  <v-container>
    <h1>Блог</h1>


    <h2>🍻 Пиво</h2>
    <blog-post-list :posts="beerArticles"  />

    <h2>📰 Лайф</h2>
    <blog-post-list :posts="newsArticles" />

  </v-container>
</template>
