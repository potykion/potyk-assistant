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

  const textToCopy = codeText.trim();

  // Пробуем современный API (работает только на HTTPS или localhost)
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(textToCopy);
      copied.value = true;
      setTimeout(() => {
        copied.value = false;
      }, 2000);
      return;
    } catch (err) {
      console.error("Clipboard API failed:", err);
      // Продолжаем к fallback методу
    }
  }

  // Fallback: старый метод через execCommand (работает на HTTP)
  try {
    const textArea = document.createElement("textarea");
    textArea.value = textToCopy;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    const successful = document.execCommand("copy");
    document.body.removeChild(textArea);

    if (successful) {
      copied.value = true;
      setTimeout(() => {
        copied.value = false;
      }, 2000);
    } else {
      console.error("execCommand copy failed");
    }
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
      <v-icon :icon="copied ? 'mdi-check' : 'mdi-content-copy'"> </v-icon>
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


