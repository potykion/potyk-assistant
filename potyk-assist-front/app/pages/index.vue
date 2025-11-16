<script lang="ts" setup>
const {data: beerArticles} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%beer%").order("date", "DESC").all()
)

</script>

<template>

  <v-container>
    <h1>potyk.io</h1>

    <h2>Блог</h2>
    <h3>Пиво</h3>
    <v-list>
      <v-list-item v-for="post in beerArticles" :key="post.id" :title="post.title" :to="post.path"
                   :subtitle="post.date.slice(0,10)"/>
    </v-list>

  </v-container>


</template>
