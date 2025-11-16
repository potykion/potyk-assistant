<script setup lang="ts">
const route = useRoute()

const {data: page} = await useAsyncData(() => queryCollection('content').path(route.path).first())

useSeoMeta({
  title: page.value?.title,
  description: page.value?.description
})
</script>

<template>
  <v-container max-width="800">

        <i>{{ page.meta.date }}</i>

        <ContentRenderer v-if="page" :value="page"/>
        <div v-else>Home not found</div>

  </v-container>
</template>

<style scoped lang="sass">

</style>
