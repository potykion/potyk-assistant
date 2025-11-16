<template>
  <div style="display: flex; justify-content: center; padding-bottom: 4px; padding-top: 4px;">
    <img
        style="border-radius: 4px"
        :src="refinedSrc"
        :alt="props.alt"
        :width="props.width"
        :height="props.height"
    />
  </div>
</template>

<script setup lang="ts">
import {withTrailingSlash, withLeadingSlash, joinURL} from 'ufo'
import {useRuntimeConfig, computed} from '#imports'


const props = defineProps({
  src: {
    type: String,
    default: '',
  },
  alt: {
    type: String,
    default: '',
  },
  width: {
    type: [String, Number],
    default: undefined,
  },
  height: {
    type: [String, Number],
    default: undefined,
  },
})

const refinedSrc = computed(() => {
  if (props.src?.startsWith('/') && !props.src.startsWith('//')) {
    const _base = withLeadingSlash(withTrailingSlash(useRuntimeConfig().app.baseURL))
    if (_base !== '/' && !props.src.startsWith(_base)) {
      return joinURL(_base, props.src)
    }
  }
  return props.src
})
</script>

