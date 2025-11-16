<script setup lang="ts">
const {data: beerArticles} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%beer%").order("date", "DESC").all()
)

useSeoMeta({
  title: 'Блог',
  description: 'Список статей блога'
})
</script>

<template>
  <v-container>
    <h1>Блог</h1>

    <h2>🍻 Пиво</h2>
    <v-list>
      <v-list-item v-for="post in beerArticles" :key="post.id" :title="post.title" :to="post.path"
                   :subtitle="post.date.slice(0,10)"/>
    </v-list>

  </v-container>
</template>
