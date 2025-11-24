<script setup lang="ts">
const route = useRoute()
const tag = computed(() => route.query.tag as string | undefined)
</script>

<template>
  <v-container>
    <h1>Поиск</h1>
    <div v-if="tag" class="text-h6">
      Тег: <strong>#{{ tag }}</strong>
    </div>
    <div v-else>
      Укажите тег для поиска
    </div>
  </v-container>
</template>

<style scoped lang="sass">

</style>