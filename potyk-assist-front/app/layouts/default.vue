<template>
  <v-app>
    <v-app-bar :elevation="0" density="compact">
      <v-app-bar-title>
        <v-btn size="x-small" to="/">potyk.io</v-btn>

        <v-btn size="x-small" to="/blog">blog</v-btn>
        <v-btn size="x-small" to="/img">img</v-btn>
        <v-btn size="x-small" to="/vid">vid</v-btn>
        <v-btn size="x-small" to="/mu">mu</v-btn>
        <v-btn size="x-small" to="/feed">feed</v-btn>
      </v-app-bar-title>
    </v-app-bar>

    <v-main CLASS="pb-10">
      <slot />
    </v-main>
  </v-app>
</template>
<script setup lang="ts"></script>
