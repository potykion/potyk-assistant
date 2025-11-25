<script setup lang="ts">
const {data: beerArticles} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%beer/%").order("date", "DESC").all()
)
const {data: newsArticles} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%life/%").order("date", "DESC").all()
)
const {data: meta} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%meta/%").order("date", "DESC").all()
)
const {data: it} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%it/%").order("date", "DESC").all()
)
const {data: food} = await useAsyncData(() =>
    queryCollection('content').where("path", "like", "%food/%").order("date", "DESC").all()
)

</script>

<template>
  <v-container>
    <h1>Блог</h1>


    <h2>🍻 Пиво</h2>
    <blog-post-list :posts="beerArticles"/>

    <h2>📰 Лайф</h2>
    <blog-post-list :posts="newsArticles"/>

    <h2>🧠 Мета</h2>
    <blog-post-list :posts="meta"/>

    <h2>Черновички</h2>
    <h3>🧑‍💻 IT</h3>
    <blog-post-list :posts="it"/>
    <h3>😋 Жрачка</h3>
    <blog-post-list :posts="food"/>


  </v-container>
</template>
