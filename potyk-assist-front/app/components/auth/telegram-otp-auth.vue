<script setup lang="ts">
interface Props {
  modelValue: boolean;
}

interface Emits {
  (e: "update:modelValue", value: boolean): void;
  (e: "success"): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const { onOtpAuthSuccess } = useTelegramAuth();

const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const username = ref("");
const otp = ref("");
const step = ref<"username" | "otp">("username");
const loading = ref(false);
const error = ref<string | null>(null);
const botUsername = ref<string | null>(null);

const apiBaseUrl = import.meta.dev
  ? "http://127.0.0.1:5000"
  : "http://84.201.131.244:5000";

const requestOtp = async () => {
  if (!username.value.trim()) {
    error.value = "Введите username";
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    const response = await $fetch<{ message?: string; error?: string; bot_username?: string }>(
      `${apiBaseUrl}/auth/telegram/otp/request`,
      {
        method: "POST",
        body: { username: username.value.trim().replace(/^@/, "") },
      }
    );

    if (response.error) {
      error.value = response.error;
      if (response.bot_username) {
        botUsername.value = response.bot_username;
      }
    } else {
      step.value = "otp";
      error.value = null;
    }
  } catch (e: any) {
    error.value = e.data?.error || e.message || "Ошибка при запросе OTP";
    if (e.data?.bot_username) {
      botUsername.value = e.data.bot_username;
    }
  } finally {
    loading.value = false;
  }
};

const verifyOtp = async () => {
  if (!otp.value.trim()) {
    error.value = "Введите код";
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    const response = await $fetch<{
      user?: { id: number; first_name: string; username?: string };
      is_admin?: boolean;
      error?: string;
    }>(`${apiBaseUrl}/auth/telegram/otp/verify`, {
      method: "POST",
      body: {
        username: username.value.trim().replace(/^@/, ""),
        otp: otp.value.trim(),
      },
    });

    if (response.error) {
      error.value = response.error;
    } else if (response.user && response.is_admin !== undefined) {
      // Успешная авторизация - сохраняем через composable
      await onOtpAuthSuccess({
        user: response.user,
        is_admin: response.is_admin,
      });
      // Эмитим событие success
      emit("success");
      dialog.value = false;
      // Сбрасываем форму
      username.value = "";
      otp.value = "";
      step.value = "username";
    }
  } catch (e: any) {
    error.value = e.data?.error || e.message || "Ошибка при проверке кода";
  } finally {
    loading.value = false;
  }
};

const reset = () => {
  username.value = "";
  otp.value = "";
  step.value = "username";
  error.value = null;
  botUsername.value = null;
};

watch(dialog, (newValue) => {
  if (!newValue) {
    reset();
  }
});
</script>

<template>
  <v-dialog v-model="dialog" max-width="400">
    <v-card>
      <v-card-title>Авторизация через Telegram</v-card-title>
      <v-card-text>
        <div v-if="step === 'username'">
          <v-text-field
            v-model="username"
            label="Telegram username"
            placeholder="@username или username"
            variant="outlined"
            class="mb-3"
            :disabled="loading"
            @keyup.enter="requestOtp"
          ></v-text-field>
          <v-alert v-if="error" type="error" density="compact" class="mb-3">
            {{ error }}
            <div v-if="botUsername" class="mt-2">
              Начните диалог с ботом:
              <a :href="`https://t.me/${botUsername}`" target="_blank">
                @{{ botUsername }}
              </a>
            </div>
          </v-alert>
        </div>

        <div v-else>
          <v-alert type="info" density="compact" class="mb-3">
            Код отправлен в Telegram. Проверьте сообщения от бота.
          </v-alert>
          <v-text-field
            v-model="otp"
            label="Код из Telegram"
            placeholder="000000"
            variant="outlined"
            class="mb-3"
            :disabled="loading"
            maxlength="6"
            @keyup.enter="verifyOtp"
          ></v-text-field>
          <v-alert v-if="error" type="error" density="compact" class="mb-3">
            {{ error }}
          </v-alert>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="dialog = false" :disabled="loading">Отмена</v-btn>
        <v-btn
          v-if="step === 'username'"
          color="primary"
          @click="requestOtp"
          :loading="loading"
        >
          Получить код
        </v-btn>
        <v-btn
          v-else
          color="primary"
          @click="verifyOtp"
          :loading="loading"
        >
          Войти
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

