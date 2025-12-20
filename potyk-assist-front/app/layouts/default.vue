<template>
  <v-app>
    <v-app-bar v-if="!shouldHideAppBar" color="amber-lighten-5" :elevation="0" density="compact">
      <v-app-bar-title>
        <v-btn size="x-small" to="/">potyk.io</v-btn>

        <v-btn size="x-small" to="/blog">blog</v-btn>
        <v-btn size="x-small" to="/vid">vid</v-btn>
        <v-btn size="x-small" to="/mu">mu</v-btn>
        <v-btn size="x-small" to="/clishe">clishe</v-btn>
      </v-app-bar-title>

      <template v-slot:append>
        <div v-if="!user" id="telegram-auth-container"></div>
        <v-btn v-if="user" icon="mdi-logout" @click="logout" size="small" title="Выйти"></v-btn>
      </template>
    </v-app-bar>

    <!-- bg-pink-lighten-5 -->
    <v-main class="pb-10 bg-amber-lighten-5">
      <!-- <v-main class="pb-10 bg-yellow-lighten-5"> -->
      <!-- <v-main class="pb-10 bg-blue-lighten-5"> -->
      <slot />
    </v-main>
  </v-app>


</template>
<script setup lang="ts">
const route = useRoute()
const shouldHideAppBar = computed(() => route.query.share === '1')

const { user, onTelegramAuth, logout, initAuth } = useTelegramAuth()

// Функция для загрузки Telegram Widget
const loadTelegramWidget = () => {
  if (process.client) {
    const container = document.getElementById('telegram-auth-container')
    if (container) {
      // Удаляем старый скрипт, если есть
      const oldScript = container.querySelector('script')
      if (oldScript) {
        oldScript.remove()
      }

      // Загружаем новый скрипт только если пользователь не авторизован
      if (!user.value) {
        const script = document.createElement('script')
        script.async = true
        script.src = 'https://telegram.org/js/telegram-widget.js?22'
        script.setAttribute('data-telegram-login', 'test_potyk_assist_bot')
        script.setAttribute('data-size', 'medium')
        script.setAttribute('data-onauth', 'onTelegramAuth(user)')
        script.setAttribute('data-request-access', 'write')
        container.appendChild(script)
      }
    }
  }
}

// Делаем onTelegramAuth доступной глобально для Telegram Widget
if (process.client) {
  // Устанавливаем функцию глобально до монтирования
  ;(window as any).onTelegramAuth = onTelegramAuth

  onMounted(() => {
    // Инициализируем авторизацию из localStorage
    initAuth()

    // Обновляем ссылку на функцию при монтировании (на случай, если composable пересоздался)
    ;(window as any).onTelegramAuth = onTelegramAuth

    // Загружаем виджет
    loadTelegramWidget()
  })

  // Следим за изменением состояния авторизации и перезагружаем виджет
  watch(user, () => {
    loadTelegramWidget()
  })
}
</script>
