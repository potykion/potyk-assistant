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
    <v-list>
      <v-list-item v-for="post in newsArticles" :key="post.id" :title="post.title" :to="post.path"
                   :subtitle="post.date.slice(0,10)"/>
    </v-list>
    <h2>🍻 Пиво</h2>
    <v-list>
      <v-list-item v-for="page in beerArticles" :key="page.id" :title="page.title" :to="page.path"
      >
        <v-list-item-subtitle>
          <i>{{ page.date.slice(0, 10) }}</i> • <i>{{ page.tags.map(tag => `#${tag}`).join(' ') }}</i>

        </v-list-item-subtitle>
      </v-list-item>
    </v-list>

  </v-container>
</template>
