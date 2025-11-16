<script setup lang="ts">

</script>

<template>

  <v-container>
    <h1>mu</h1>
    <h2>Featured</h2>

    <v-row>
      <v-col cols="3">

        <div>
          <v-img src="https://avatars.yandex.net/get-music-content/49876/cbf41616.a.89962-1/600x600"></v-img>
          <div class="font-weight-bold text-h6">Londinium</div>
          <div class="text-subtitle-2">Archive • 1996</div>

          <div class=" text-subtitle-2 font-italic">Highlighted track: <b>So Few Words</b></div>
          <audio src="/Archive%20-%20So%20Few%20Words.mp3" controls></audio>

          <mu-track title="So Few Words" artist="Londinium" ></mu-track>
        </div>


      </v-col>
    </v-row>

  </v-container>

</template>

<style scoped lang="sass">

</style>