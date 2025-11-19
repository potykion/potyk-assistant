<!--
Usage in content/**/*.md:

::blog-beer-info{country-flag="🇩🇪" style="Пшеничка" :abv="4.9" tap-date="06.25" :price="220" place="ВкусВилл" :rating="4.25"}
::

Will render:

🇩🇪 • Пшеничка • ABV: 4.9° • Розлив: 06.25 • Цена: 220₽ @ ВкусВилл • 4.25 / 5 ⭐
-->

<script setup lang="ts">
import BeerInfo from "~/components/blog/beer-info.vue";

const props = defineProps<{
  title: string
  url: string
  img: string
  countryFlag: string
  styleName: string
  abv: number
  tapDate: string
  price: number
  place: string
  rating: number
}>()

</script>

<template>

  <div style="display: flex; gap: 16px; align-items: center; margin-top: 8px; margin-bottom: 8px; padding: 8px; border-radius: 16px" class="bg-amber-lighten-5
">
    <img :src="img" width="64" height="64" style="border-radius: 16px">
    <div>
      <a :href="url"><h2 style="margin-bottom: 0px; margin-top: 0;">{{ title }}</h2></a>
      <beer-info
          :country-flag="props.countryFlag" :style-name="props.styleName" :abv="props.abv"
          :tap-date="props.tapDate" :price="props.price" :place="props.place" :rating="props.rating"/>
    </div>

  </div>


</template>

