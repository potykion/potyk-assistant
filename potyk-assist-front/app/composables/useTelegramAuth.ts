interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
  auth_date?: number;
  hash?: string;
}

interface AuthResponse {
  user: TelegramUser;
  is_admin: boolean;
}

interface OtpVerifyResponse {
  user: TelegramUser;
  is_admin: boolean;
}

export const useTelegramAuth = () => {
  const apiBaseUrl = import.meta.dev
    ? "http://127.0.0.1:5000"
    : "http://84.201.131.244:5000";

  const user = useState<TelegramUser | null>("telegram_user", () => null);
  const isAdmin = useState<boolean>("is_admin", () => false);

  const onTelegramAuth = async (tgUser: TelegramUser) => {
    try {
      const response = await $fetch<AuthResponse>(`${apiBaseUrl}/auth/telegram`, {
        method: "POST",
        body: tgUser,
      });

      user.value = response.user;
      isAdmin.value = response.is_admin;

      // Сохраняем в localStorage для сохранения состояния при перезагрузке
      if (process.client) {
        localStorage.setItem("telegram_user", JSON.stringify(response.user));
        localStorage.setItem("is_admin", String(response.is_admin));
      }
    } catch (error) {
      console.error("Ошибка при авторизации через Telegram:", error);
    }
  };

  const logout = () => {
    user.value = null;
    isAdmin.value = false;
    if (process.client) {
      localStorage.removeItem("telegram_user");
      localStorage.removeItem("is_admin");
    }
  };

  // Восстанавливаем состояние из localStorage при загрузке (только на клиенте)
  const initAuth = () => {
    if (process.client) {
      const savedUser = localStorage.getItem("telegram_user");
      const savedIsAdmin = localStorage.getItem("is_admin");
      if (savedUser) {
        try {
          user.value = JSON.parse(savedUser);
          isAdmin.value = savedIsAdmin === "true";
        } catch (e) {
          console.error("Ошибка при восстановлении состояния авторизации:", e);
        }
      }
    }
  };

  // Инициализируем при первом вызове на клиенте
  if (process.client) {
    initAuth();
  }

  const onOtpAuthSuccess = async (otpResponse: OtpVerifyResponse) => {
    user.value = otpResponse.user;
    isAdmin.value = otpResponse.is_admin;

    // Сохраняем в localStorage для сохранения состояния при перезагрузке
    if (process.client) {
      localStorage.setItem("telegram_user", JSON.stringify(otpResponse.user));
      localStorage.setItem("is_admin", String(otpResponse.is_admin));
    }
  };

  return {
    user: readonly(user),
    isAdmin: readonly(isAdmin),
    onTelegramAuth,
    onOtpAuthSuccess,
    logout,
    initAuth,
  };
};

