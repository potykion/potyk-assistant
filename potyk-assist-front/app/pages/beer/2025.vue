<script setup lang="ts">

const ipaBeers = [
  {
    url: "https://untappd.com/b/midnight-project-citra-pre-order/6349012",
    photo: "https://assets.untappd.com/photos/2025_11_23/79ef619ae2e5d1d67496c988cee1b163_c_1530618259_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6349012_c92f5_sm.jpeg",
    title: "Citra? Pre-Order!",
    // brewery: "Midnight Project feat. Horror, Red Rocket",
    brewery: "Midnight Project × Horror × Red Rocket",
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
  {
    url: "https://untappd.com/b/ostrovica-relict/6171726",
    photo: "https://assets.untappd.com/photos/2025_04_26/436c478ee6bf0c721d184988d4d88803_c_1474271153_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6171726_744b7_sm.jpeg",
    title: "RELICT",
    brewery: "OSTROVICA × Big Village",
    style: "IPA — Session",
  },
  {
    url: "https://untappd.com/b/velka-morava-dunedin/6127822",
    photo: "https://assets.untappd.com/photos/2025_02_05/d81a63a6e9739c4596d0320079056cdc_c_1454596498_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6127822_90729_sm.jpeg",
    title: "Dunedin",
    brewery: "Velka Morava",
    style: "IPA — New Zealand",
  }, {
    url: "https://untappd.com//b/zagovor-brewery-dogma/6231793",
    photo: "https://assets.untappd.com/photos/2025_04_18/0a55d95d3479fdfd2086f181b1a574dd_c_1471873752_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6231793_955d6_sm.jpeg",
    title: "Dogma",
    brewery: "Zagovor",
    style: "IPA — Imperial / Double New England / Hazy",
  },
  {
    url: "https://untappd.com//b/midnight-project-hop-headshot-bru-1/6376078",
    photo: "https://assets.untappd.com/photos/2025_10_03/0ac5b22627dacc5ab741b7bb948052dd_c_1518016198_raw.jpg",
    icon: "https://assets.untappd.com/site/beer_logos/beer-6376078_ee8bf_sm.jpeg",
    title: "Hop Headshot: BRU-1",
    brewery: "Midnight Project",
    style: "IPA — Triple",
  },
]

</script>

<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="text-center">Пивные итоги 2025 года</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <h2 class="text-center rounded bg-amber-lighten-4 pa-2">IPA</h2>
      </v-col>
    </v-row>

    <v-row>

      <template v-for="beer in ipaBeers" :key="beer.url">
        <v-col md="4" sm="6">
          <v-card
              class="beer-card"
              :href="beer.url"
              rounded="lg"
          >
            <div class="beer-card__media">
              <v-img height="541" cover :src="beer.photo" rounded="lg"></v-img>
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