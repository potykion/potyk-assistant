<script setup lang="ts">
const route = useRoute()

const {data: page} = await useAsyncData(() => queryCollection('content').path(route.path).first())

</script>

<template>
  <v-container max-width="800">
        <i>{{ page.date.slice(0,10) }}</i> • <i>{{ page.tags.map(tag => `#${tag}`).join(' ')  }}</i>

        <ContentRenderer v-if="page" :value="page"/>
        <div v-else>Home not found</div>

  </v-container>
</template>

<style scoped lang="sass">

</style>
