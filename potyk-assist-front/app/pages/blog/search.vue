<script setup lang="ts">
const route = useRoute()
const tag = computed(() => route.query.tag as string | undefined)

const {data: allPosts} = await useAsyncData(
  () => `blog-search-${tag.value || 'all'}`,
  () => queryCollection('content').order("date", "DESC").all(),
  {
    watch: [tag]
  }
)

const filteredPosts = computed(() => {
  if (!tag.value || !allPosts.value) return []
  
  return allPosts.value.filter((post: any) => 
    post.tags && Array.isArray(post.tags) && post.tags.includes(tag.value)
  )
})
</script>

<template>
  <v-container>
    <h1>Поиск</h1>
    <div v-if="tag" class="text-h6 mb-4">
      Тег: <strong>#{{ tag }}</strong>
    </div>
    <div v-else class="mb-4">
      Укажите тег для поиска
    </div>
    
    <div v-if="tag && filteredPosts && filteredPosts.length > 0">
      <blog-post-list :posts="filteredPosts" />
    </div>
    <div v-else-if="tag && filteredPosts && filteredPosts.length === 0" class="text-body-1">
      Постов с тегом <strong>#{{ tag }}</strong> не найдено
    </div>
  </v-container>
</template>

<style scoped lang="sass">

</style>