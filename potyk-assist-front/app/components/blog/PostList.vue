<script setup lang="ts">
interface Post {
  id: string
  title: string
  path: string
  date: string
  tags?: string[]
}

interface Props {
  posts: Post[];
  showDate: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showDate: true
})

const handleTagClick = (tag: string, event: Event) => {
  event.preventDefault()
  event.stopPropagation()
  navigateTo(`/blog/search?tag=${encodeURIComponent(tag)}`)
}
</script>

<template>
  <v-list>
    <v-list-item v-for="post in posts" :key="post.id" :title="post.title" :to="post.path">
      <v-list-item-subtitle>
        <i>
          <template v-if="props.showDate">{{ post.date.slice(0, 10) }}</template>
          <template v-if="post.tags?.length"> •
            <span v-for="(tag, index) in post.tags" :key="tag">
              <span v-if="index > 0"> </span>
              <a
                href="#"
                class="tag-link"
                @click="handleTagClick(tag, $event)"
              >#{{ tag }}</a>
            </span>
          </template>
        </i>
      </v-list-item-subtitle>
    </v-list-item>
  </v-list>
</template>

<style scoped>
.tag-link {
  color: inherit;
  text-decoration: none;
  cursor: pointer;
}

.tag-link:hover {
  text-decoration: underline;
}
</style>
