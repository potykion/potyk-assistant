<template>
  <v-app>

    <v-app-bar :elevation="0" density="compact" >

      <v-app-bar-title >
        <v-btn to="/">potyk.io</v-btn>

        <v-btn to="/blog">blog</v-btn>
        <v-btn to="/img">img</v-btn>
        <v-btn to="/vid">vid</v-btn>
        <v-btn to="/mu">mu</v-btn>
        <v-btn to="/feed">feed</v-btn>

      </v-app-bar-title>


    </v-app-bar>

    <v-main>
      <slot/>
    </v-main>

  </v-app>


</template>
<script setup lang="ts">
</script>