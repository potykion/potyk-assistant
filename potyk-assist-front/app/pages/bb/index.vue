<script setup lang="ts">
const config = useRuntimeConfig()

const apiBaseUrl = import.meta.dev
  ? "http://127.0.0.1:5000"
  : "http://84.201.131.244:5000"

const bbEmail = ref("")
const bbToken = ref(config.public.bbToken || "")
const bbOrg = ref("")
const bbRepo = ref("")
const bbBranch = ref("master")
const bbPath = ref("")
const bbMsg = ref("")
const bbFileSrc = ref("")
const bbFormStorageKey = "bb-form-v1"

const readLoading = ref(false)
const commitLoading = ref(false)
const bbError = ref("")
const bbSuccess = ref("")
const bbSnackbar = ref(false)

onMounted(() => {
  const raw = localStorage.getItem(bbFormStorageKey)
  if (!raw) {
    return
  }

  try {
    const saved = JSON.parse(raw) as {
      email?: string
      token?: string
      org?: string
      repo?: string
      branch?: string
      msg?: string
      fileSrc?: string
    }
    bbEmail.value = saved.email || ""
    bbToken.value = saved.token || bbToken.value
    bbOrg.value = saved.org || ""
    bbRepo.value = saved.repo || ""
    bbBranch.value = saved.branch || "master"
    bbMsg.value = saved.msg || ""
    bbFileSrc.value = saved.fileSrc || ""
  } catch {
    // ignore malformed localStorage payload
  }
})

watch([bbEmail, bbToken, bbOrg, bbRepo, bbBranch, bbMsg, bbFileSrc], () => {
  localStorage.setItem(
    bbFormStorageKey,
    JSON.stringify({
      email: bbEmail.value,
      token: bbToken.value,
      org: bbOrg.value,
      repo: bbRepo.value,
      branch: bbBranch.value,
      msg: bbMsg.value,
      fileSrc: bbFileSrc.value,
    }),
  )
})

const showError = (message: string) => {
  bbError.value = message
  bbSuccess.value = ""
  bbSnackbar.value = true
}

const showSuccess = (message: string) => {
  bbSuccess.value = message
  bbError.value = ""
  bbSnackbar.value = true
}

const requireReadParams = () => {
  if (!bbEmail.value.trim()) return "email is required"
  if (!bbToken.value.trim()) return "api_token is required"
  if (!bbOrg.value.trim()) return "org is required"
  if (!bbRepo.value.trim()) return "repo is required"
  if (!bbPath.value.trim()) return "path is required"
  return ""
}

const fetchFile = async () => {
  const validationError = requireReadParams()
  if (validationError) {
    showError(validationError)
    return
  }

  readLoading.value = true
  try {
    const response = await $fetch<{ content: string }>(`${apiBaseUrl}/bb/src`, {
      method: "POST",
      body: {
        email: bbEmail.value.trim(),
        api_token: bbToken.value.trim(),
        org: bbOrg.value.trim(),
        repo: bbRepo.value.trim(),
        path: bbPath.value.trim(),
        branch: bbBranch.value.trim() || "master",
      },
    })
    bbFileSrc.value = response.content || ""
    showSuccess("File loaded")
  } catch (error: any) {
    showError(error?.data?.error || error?.message || "Failed to load file")
  } finally {
    readLoading.value = false
  }
}

const commitFile = async () => {
  const validationError = requireReadParams()
  if (validationError) {
    showError(validationError)
    return
  }
  if (!bbFileSrc.value.trim()) {
    showError("file content is empty")
    return
  }

  commitLoading.value = true
  try {
    await $fetch(`${apiBaseUrl}/bb/commit`, {
      method: "POST",
      body: {
        email: bbEmail.value.trim(),
        api_token: bbToken.value.trim(),
        org: bbOrg.value.trim(),
        repo: bbRepo.value.trim(),
        path: bbPath.value.trim(),
        branch: bbBranch.value.trim() || "master",
        msg: bbMsg.value.trim() || undefined,
        content: bbFileSrc.value,
      },
    })
    showSuccess("Commit created")
  } catch (error: any) {
    showError(error?.data?.error || error?.message || "Failed to commit file")
  } finally {
    commitLoading.value = false
  }
}
</script>

<template>
  <v-container>
    <h1 class="mb-4">bb</h1>

    <v-card variant="plain" >
      <v-card-title class="px-0">Get file</v-card-title>
      <v-form @submit.prevent="fetchFile">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field v-model="bbEmail" label="email" variant="outlined" />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="bbToken" label="api token" type="password" variant="outlined" />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="bbOrg" label="org" variant="outlined" />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="bbRepo" label="repo" variant="outlined" />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field v-model="bbBranch" label="branch" variant="outlined" />
          </v-col>
          <v-col cols="12">
            <v-text-field v-model="bbPath" label="path (e.g. README.md)" variant="outlined" />
          </v-col>
        </v-row>
        <v-btn type="submit" color="primary" :loading="readLoading" :disabled="readLoading">Get src</v-btn>
      </v-form>
    </v-card>

    <v-card variant="plain" >
      <v-card-title class="px-0">Commit file</v-card-title>
      <v-form @submit.prevent="commitFile">
        <v-textarea
          v-model="bbFileSrc"
          label="file src"
          rows="16"
          auto-grow
          variant="outlined"
          class="mb-3"
        />
        <v-text-field
          v-model="bbMsg"
          label="commit msg (optional)"
          variant="outlined"
          class="mb-2"
        />
        <v-btn type="submit" color="primary" :loading="commitLoading" :disabled="commitLoading">Commit</v-btn>
      </v-form>
    </v-card>

    <v-snackbar v-model="bbSnackbar" :color="bbError ? 'error' : 'success'" location="bottom">
      {{ bbError || bbSuccess }}
    </v-snackbar>
  </v-container>
</template>
