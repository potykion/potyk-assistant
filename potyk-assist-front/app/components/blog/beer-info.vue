<script setup lang="ts">
const props = defineProps<{
  countryFlag: string
  name: string
  abv: number
  tapDate: string
  price: number
  place: string
  rating: number
  maxRating?: number
}>()

const maxRating = props.maxRating ?? 5
</script>

<template>
  <div class="beer-info">
    <span>{{ props.countryFlag }}</span>
    <span>•</span>
    <span>{{ props.name }}</span>
    <span>•</span>
    <span>ABV: {{ props.abv }}°</span>
    <span>•</span>
    <span>Розлив: {{ props.tapDate }}</span>
    <span>•</span>
    <span>Цена: {{ props.price }}₽</span>
    <span>@</span>
    <span>{{ props.place }}</span>
    <span>•</span>
    <span>{{ props.rating }} / {{ maxRating }} ⭐</span>
  </div>
</template>

<style scoped lang="sass">
.beer-info
  display: flex
  align-items: center
  gap: 4px
  flex-wrap: wrap
</style>