<template>
  <v-app>
    <v-app-bar color="amber-lighten-5" :elevation="0" density="compact">
      <v-app-bar-title>
        <v-btn size="x-small" to="/">potyk.io</v-btn>

        <v-btn size="x-small" to="/blog">blog</v-btn>
        <v-btn size="x-small" to="/img">img</v-btn>
        <v-btn size="x-small" to="/vid">vid</v-btn>
        <v-btn size="x-small" to="/mu">mu</v-btn>
        <v-btn size="x-small" to="/feed">feed</v-btn>
        <v-btn size="x-small" to="/clishe">clishe</v-btn>
      </v-app-bar-title>
    </v-app-bar>

    <!-- bg-pink-lighten-5 -->
    <v-main class="pb-10 bg-amber-lighten-5">
      <!-- <v-main class="pb-10 bg-yellow-lighten-5"> -->
      <!-- <v-main class="pb-10 bg-blue-lighten-5"> -->
      <slot />
    </v-main>
  </v-app>
</template>
<script setup lang="ts"></script>
