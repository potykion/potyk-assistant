<script setup lang="ts">
interface Post {
  id: string;
  title: string;
  path: string;
  date: string;
  tags?: string[];
}

interface Props {
  posts: Post[];
  showDate: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showDate: true,
});

const handleTagClick = (tag: string, event: Event) => {
  event.preventDefault();
  event.stopPropagation();
  navigateTo(`/blog/search?tag=${encodeURIComponent(tag)}`);
};
</script>

<template>
  <v-row class="flex-sm-column flex-md-row">
    <v-col v-for="post in posts" :key="post.id" md="4" xl="3" sm="12">
      <v-card :title="post.title" :to="post.path" variant="outlined">
        <template #subtitle>
          <i>
            <template v-if="props.showDate">{{
              post.date.slice(0, 10)
            }}</template>
            <template v-if="post.tags?.length">
              •
              <span v-for="(tag, index) in post.tags" :key="tag">
                <span v-if="index > 0"> </span>
                <a
                  href="#"
                  class="tag-link"
                  @click="handleTagClick(tag, $event)"
                  >#{{ tag }}</a
                >
              </span>
            </template>
          </i>
        </template>
      </v-card>
    </v-col>
  </v-row>
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
