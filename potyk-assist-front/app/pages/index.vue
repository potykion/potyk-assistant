<script lang="ts" setup>
const {data: beerArticles} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%beer%").order("date", "DESC").all()
)

</script>

<template>

  <v-container>
    <h1><code>potyk.io</code></h1>
    <v-alert style="margin: 8px 0 " color="success" variant="tonal" title="Юбик"
             text="      Прив. 5 лет пытаюсь вести блог, 5 лет бросаю это дело. Пора отметить это очередным блогом 😂."></v-alert>

    <cite>

    </cite>

    <h2>Блог</h2>
    <h3>🍻 Пиво</h3>
    <v-list>
      <v-list-item v-for="post in beerArticles" :key="post.id" :title="post.title" :to="post.path"
                   :subtitle="post.date.slice(0,10)"/>
    </v-list>

  </v-container>


</template>
