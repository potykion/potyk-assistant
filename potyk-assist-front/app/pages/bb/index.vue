<template>
  <v-container>
    <v-form>
      <v-text-field v-model="bbToken" label="bb token" />
    </v-form>
  </v-container>
</template>

<script setup lang="ts">

const config = useRuntimeConfig();
const bbToken = ref(config.public.bbToken);
</script>
