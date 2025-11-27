<script setup lang="ts">

const beers = [
  {
    url: "https://untappd.com/b/midnight-project-citra-pre-order/6349012",
    photo: "https://assets.untappd.com/photos/2025_11_23/79ef619ae2e5d1d67496c988cee1b163_c_1530618259_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6349012_c92f5_sm.jpeg",
    title: "Citra? Pre-Order!",
    brewery: "Midnight Project"
  }
]

</script>

<template>
  <v-container>
    <v-row>
      <h1>Пивные итоги 2025 года</h1>
    </v-row>


    <v-row>

      <template v-for="beer in beers" :key="beer.url">
        <v-col cols="3">
          <v-card :href="beer.url">
            <v-img :src="beer.photo"></v-img>
            <v-card-title>{{ beer.title }}</v-card-title>
            <v-card-subtitle>{{ beer.brewery }}</v-card-subtitle>
          </v-card>
        </v-col>
      </template>
    </v-row>


  </v-container>
</template>

<style scoped lang="sass">

</style>