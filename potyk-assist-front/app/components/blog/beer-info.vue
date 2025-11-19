<!--
Usage in content/**/*.md:

::blog-beer-info{country-flag="🇩🇪" style="Пшеничка" :abv="4.9" tap-date="06.25" :price="220" place="ВкусВилл" :rating="4.25"}
::

Will render:

🇩🇪 • Пшеничка • ABV: 4.9° • Розлив: 06.25 • Цена: 220₽ @ ВкусВилл • 4.25 / 5 ⭐
-->

<script setup lang="ts">
const props = defineProps<{
  countryFlag: string
  styleName: string
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
  <p  class="font-weight-semibold font-italic   text-grey-darken-4">
      {{ props.countryFlag }}
      •
      🍺: {{ props.styleName }}
      •
      💪: {{ props.abv }}°
      •
      📅: {{ props.tapDate }}
      •
      💵: {{ props.price }}₽
      •
      🏪: {{ props.place }}
      •
      ⭐: {{ props.rating }} / {{ maxRating }}
  </p>
</template>

