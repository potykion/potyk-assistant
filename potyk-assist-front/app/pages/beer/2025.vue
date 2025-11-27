<script setup lang="ts">

const ipaBeers = [
  {
    url: "https://untappd.com/b/midnight-project-citra-pre-order/6349012",
    photo: "https://assets.untappd.com/photos/2025_11_23/79ef619ae2e5d1d67496c988cee1b163_c_1530618259_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6349012_c92f5_sm.jpeg",
    title: "Citra? Pre-Order!",
    brewery: "Midnight Project",
    style: "IPA — American",
  },

  {
    url: "https://untappd.com/b/sigma-brau-sigma-brau-auster-shymkentskij-marakas/6061139",
    photo: "https://assets.untappd.com/photos/2025_09_13/2711911f164c991e7272c38e2f8639e9_c_1513123889_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6061139_dff87_sm.jpeg",
    title: "Шымкентский Маракас",
    brewery: "Sigma Bräu",
    style: "IPA — New England / Hazy",
  },
]

</script>

<template>
  <v-container>
    <v-row>
      <h1>Пивные итоги 2025 года</h1>
    </v-row>

    <v-row>
      <h2>IPA</h2>
    </v-row>

    <v-row>

      <template v-for="beer in ipaBeers" :key="beer.url">
        <v-col cols="3" sm="4">
          <v-card
              class="beer-card"
              :href="beer.url"
              rounded="lg"
          >
            <div class="beer-card__media">
              <v-img :src="beer.photo" rounded="lg"></v-img>
              <v-avatar
                  class="beer-card__icon"
                  size="100"
                  rounded="lg"
                  :image="beer.icon"
              />
            </div>
            <v-card-title class="text-center font-weight-bold mt-5 pb-0">{{ beer.title }}</v-card-title>
            <v-card-subtitle class="text-center pb-3 ">
              <div>{{ beer.brewery }}</div>
            </v-card-subtitle>
            <v-divider></v-divider>
            <v-card-text class="text-center">
              {{ beer.style }}

            </v-card-text>

          </v-card>
        </v-col>
      </template>
    </v-row>


  </v-container>
</template>

<style scoped lang="sass">
.beer-card
  position: relative
  overflow: visible

.beer-card__media
  position: relative

.beer-card__icon
  position: absolute
  left: 50%
  bottom: -20px
  transform: translateX(-50%)
  width: 80px
  height: 80px
  box-shadow: 0 1px 20px rgba(0, 0, 0, 0.35)
  border-radius: 0
  z-index: 2

</style>