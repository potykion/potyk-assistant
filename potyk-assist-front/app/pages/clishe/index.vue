<template>
  <v-container>
    <h1><code>clishe</code></h1>
    <cite>Tired of typing shi~ in shell — try <b>clishe</b></cite>

    <v-row dense>
      <v-col cols="12">
        <h2><code>basis</code></h2>
        <code-block>cd /mnt/c/users/admin/PycharmProjects/ibs_vms/</code-block>
      </v-col>

      <v-col>
        <v-card title="Скачать логи агента">
          <v-card-text>
            <v-row dense>
              <v-col cols="6">
                <v-text-field
                  v-model="agentUser"
                  label="user"
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="agentDir"
                  label="dir"
                  hide-details
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="agentHostsText"
                  label="hosts"
                  hide-details
                ></v-textarea>
              </v-col>
              <v-col cols="12">
                <code-block :code="computedAgentCode" />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col>
        <v-card title="Скачать логи бека">
          <v-card-text>
            <v-row dense>
              <v-col cols="6">
                <v-text-field
                  v-model="user"
                  label="user"
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="dir"
                  label="dir"
                  hide-details
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="hostsText"
                  label="hosts"
                  hide-details
                ></v-textarea>
              </v-col>
              <v-col cols="4">
                <v-checkbox
                  v-model="logTypes.backend"
                  label="backend"
                  hide-details
                ></v-checkbox>
              </v-col>
              <v-col cols="4">
                <v-checkbox
                  v-model="logTypes.am1"
                  label="am-1"
                  hide-details
                ></v-checkbox>
              </v-col>
              <v-col cols="4">
                <v-checkbox
                  v-model="logTypes.am2"
                  label="am-2"
                  hide-details
                ></v-checkbox>
              </v-col>
              <v-col cols="12">
                <code-block :code="computedCode" />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
const user = ref("ibs");
const dir = ref("./logs");
const hosts = ref<string[]>(["10.0.87.108", "10.0.87.107", "10.0.87.91"]);

const logTypes = ref({
  backend: false,
  am1: true,
  am2: true,
});

const agentUser = ref("root");
const agentDir = ref("./log");
const agentHosts = ref<string[]>(["10.0.38.121"]);

const hostsText = computed({
  get: () => hosts.value.join("\n"),
  set: (value: string) => {
    hosts.value = value.split("\n").filter((h) => h.trim() !== "");
  },
});

const agentHostsText = computed({
  get: () => agentHosts.value.join("\n"),
  set: (value: string) => {
    agentHosts.value = value.split("\n").filter((h) => h.trim() !== "");
  },
});

const computedCode = computed(() => {
  const commands: string[] = [];

  hosts.value.forEach((host) => {
    const tail = host.split(".").pop() || host;

    if (logTypes.value.backend) {
      commands.push(
        `scp ${user.value}@${host}:/var/log/vms/backend.log ${dir.value}/${tail}-backend.log`,
      );
    }

    if (logTypes.value.am1) {
      commands.push(
        `scp ${user.value}@${host}:/var/log/vms/am-1/agent_manager.log ${dir.value}/${tail}-am-1.log`,
      );
    }

    if (logTypes.value.am2) {
      commands.push(
        `scp ${user.value}@${host}:/var/log/vms/am-2/agent_manager.log ${dir.value}/${tail}-am-2.log`,
      );
    }
  });

  return commands.join("\n");
});

const computedAgentCode = computed(() => {
  return agentHosts.value
    .map((host) => {
      const tail = host.split(".").pop() || host;
      return `scp ${agentUser.value}@${host}:/var/log/vms-agent/agent.log ${agentDir.value}/${tail}-agent.log`;
    })
    .join("\n");
});
</script>
