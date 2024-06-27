import PrimeVue from "primevue/config";
import { createApp } from "vue";

import App from "@/App.vue";

import "primevue/resources/themes/aura-light-teal/theme.css";
import "@/assets/main.css";

const app = createApp(App);
app.use(PrimeVue);
app.mount("#app");
