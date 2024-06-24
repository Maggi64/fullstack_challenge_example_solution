<script setup lang="ts">
import Message from 'primevue/message';
import Panel from 'primevue/panel';
import { onBeforeMount, ref } from 'vue';

import { getData } from './client';


type TimeGetResponse = {
  current_time: string;
};

const dbCurrentTime = ref<Date | null>(null);

onBeforeMount(async () => {
  const data = await getData<TimeGetResponse>("/");
  dbCurrentTime.value = new Date(data.current_time);
});
</script>

<template>
  <header>
    <img alt="envelio logo" class="logo" src="@/assets/logo.svg" />
    <h1>envelio Coding Challenge</h1>
  </header>

  <main>
    <Panel class="welcome-info" header="Welcome to the envelio Coding Challenge!">
      <p>This component provides a very basic boilerplate for the UI of the app. It
        includes a sample API request to help you get started with the provided setup.
        The response is displayed below:</p>
      <Message severity="secondary" :closable="false">
        <label>Current database time</label>
        {{ dbCurrentTime }}
      </Message>
      <p>The boilerplate is intentionally kept very simple and doesn't follow best
        practices regarding code structure and separation of concerns yet. Therefore, it
        doesn't serve as a blueprint for your implementation. Please follow known best
        practices and patterns when implementing the task and change the existing code
        as you see fit.</p>
      <p>Good luck with the task!</p>
    </Panel>
  </main>
</template>

<style scoped>
header {
  display: flex;
  align-items: center;
  padding-inline: 1.5rem;
  border-bottom: var(--gray-300) 1px solid;
}

header .logo {
  height: 2rem;
  margin-right: 1.5rem;
}

header h1 {
  font-size: 1.5rem;
}

main {
  padding: 1.5rem;
  display: flex;
  flex-grow: 1;
  justify-content: center;
  align-items: center;
  background-color: var(--gray-100);
}

.welcome-info {
  max-width: 50rem;
  padding: .75rem;
}

.welcome-info label {
  display: block;
  margin-bottom: .35rem;
  font-size: .8rem;
  color: var(--gray-500);
}
</style>
