<!--
Usage in content/**/*.md:

::blog-beer-info{country-flag="🇩🇪" name="Пшеничка" :abv="4.9" tap-date="06.25" :price="220" place="ВкусВилл" :rating="4.25"}
::

Will render:

🇩🇪 • Пшеничка • ABV: 4.9° • Розлив: 06.25 • Цена: 220₽ @ ВкусВилл • 4.25 / 5 ⭐
-->

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
  <p>
    <i>
      {{ props.countryFlag }}
      •
      {{ props.name }}
      •
      ABV: {{ props.abv }}°
      •
      Розлив: {{ props.tapDate }}
      •
      Цена: {{ props.price }}₽
      @
      {{ props.place }}
      •
      {{ props.rating }} / {{ maxRating }} ⭐
    </i>
  </p>
</template>

