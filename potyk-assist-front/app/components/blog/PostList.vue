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
</script>

<template>
  <v-list>
    <v-list-item v-for="post in posts" :key="post.id" :title="post.title" :to="post.path">
      <v-list-item-subtitle>
        <i>
          <template v-if="props.showDate">{{ post.date.slice(0, 10) }}</template>
          <template v-if="post.tags?.length"> • {{ post.tags?.map(tag => `#${tag}`).join(' ') }}
          </template>
        </i>
      </v-list-item-subtitle>
    </v-list-item>
  </v-list>
</template>
