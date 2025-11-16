<script setup lang="ts">
const props = defineProps<{
  title: string
  artist: string
}>()
</script>

<template>
  <v-list-item>
    <v-list-item-title>{{ props.title }}</v-list-item-title>
    <v-list-item-subtitle>{{ props.artist }}</v-list-item-subtitle>
  </v-list-item>
</template>

<style scoped lang="sass">
</style>