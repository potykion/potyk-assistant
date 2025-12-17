<script setup lang="ts">
const props = defineProps<{
  code?: string;
}>();

const copied = ref(false);
const codeRef = ref<HTMLElement | null>(null);

const copyToClipboard = async () => {
  let codeText = props.code || "";

  if (!codeText && codeRef.value) {
    codeText = codeRef.value.textContent || codeRef.value.innerText || "";
  }

  if (!codeText) return;

  try {
    await navigator.clipboard.writeText(codeText.trim());
    copied.value = true;
    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch (err) {
    console.error("Failed to copy:", err);
  }
};
</script>

<template>
  <div class="code-block-wrapper position-relative">
    <v-btn
      class="copy-button"
      size="small"
      icon
      variant="text"
      @click="copyToClipboard"
    >
      <v-icon icon="mdi-content-copy"> </v-icon>
    </v-btn>

    <pre
      class="bg-grey-lighten-4 rounded pa-2 mb-0"
    ><code ref="codeRef"><slot>{{ code }}</slot></code></pre>
  </div>
</template>

<style scoped lang="sass">
.code-block-wrapper
  position: relative
  margin: 8px 0

.copy-button
  position: absolute
  top: 0
  right: 0
  z-index: 1

pre
  position: relative
  margin: 0
  overflow-x: auto

  code
    font-family: 'Courier New', monospace
    font-size: 14px
    line-height: 1.5
    white-space: pre
</style>

