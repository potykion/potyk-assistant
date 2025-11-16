<script setup lang="ts">
const {data: articles} = await useAsyncData(() =>
    queryCollection('content').all()
)

useSeoMeta({
  title: 'Блог',
  description: 'Список статей блога'
})
</script>

<template>
  <v-container>
    <h1>Блог</h1>

    <v-list>
      <v-list-item v-for="post in articles" :key="post.id" :title="post.title" :to="post.path" :subtitle="post.meta.date"/>
    </v-list>

  </v-container>
</template>
