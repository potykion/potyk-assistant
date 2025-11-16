<script setup lang="ts">
const { data: articles } = await useAsyncData(() =>
  queryCollection('content').path('/blog').all()
)

useSeoMeta({
  title: 'Блог',
  description: 'Список статей блога'
})
</script>

<template>
  <div>
    <h1>Блог</h1>

    <div v-if="articles?.length">
      <v-list>
        <v-list-item
          v-for="article in articles"
          :key="article._id"
          :to="article._path"
          link
          :title="article.title || article._path"
        >
        </v-list-item>
      </v-list>
    </div>
    <div v-else>
      Статей пока нет
    </div>
  </div>
</template>
