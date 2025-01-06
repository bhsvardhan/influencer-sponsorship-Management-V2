import { compile, createApp } from "vue";
import { createWebHistory, createRouter } from "vue-router";

import App from "./App.vue";
import MainPage from "./components/MainPage.vue";
import Login from "./components/LoginPage.vue";
import admin_dashboard1 from "./components/admin_dashboard1.vue";
import admin_dashboard from "./components/admin_dashboard.vue";
import stats from "./components/stats.vue";
import authPlugin from "./auth/authPlugin";
import influencer_dashboard from "./components/influencer_dashboard.vue";
import influencer_dashboard1 from "./components/influencer_dashboard1.vue";
import sponsor_dashboard from "./components/sponsor_dashboard.vue";
import sponsor_dashboard1 from "./components/sponsor_dashboard1.vue";
import add_campaign from "./components/add_campaign.vue";
import sponsor_dashboard2 from "./components/sponsor_dashboard2.vue";

const routes = [
  { path: "/", component: MainPage },
  { path: "/login", component: Login },
  { path: "/admin_dashboard", component: admin_dashboard },
  { path: "/admin_dashboard1", component: admin_dashboard1 },
  { path: "/stats", component: stats },
  { path: "/influencer_dashboard",component: influencer_dashboard},
  { path: "/influencer_dashboard1",component: influencer_dashboard1},
  { path: "/sponsor_dashboard",component: sponsor_dashboard},
  { path: "/sponsor_dashboard1",component: sponsor_dashboard1},
  { path: "/add_campaign",component:add_campaign},
  { path: "/sponsor_dashboard2",component:sponsor_dashboard2},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);
app.use(router);
app.use(authPlugin);
app.mount("#app");
