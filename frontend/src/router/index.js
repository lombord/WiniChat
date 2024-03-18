// Router plugin
import { inject } from "vue";
import { createRouter, createWebHistory } from "vue-router";

/**
 * Router Guard to check if session is authenticated.
 * Used when defining routes to protect routes.
 * Called before accessing a route
 */
function IfAuthenticated(from, to) {
  const session = inject("session");
  if (!session.isAuthenticated) {
    return { name: "login" };
  }
}

/**
 * Router Guard to check if session is not authenticated.
 * Used when defining routes to protect routes.
 * Called before accessing a route
 */
function IfNotAuthenticated(from, to) {
  const session = inject("session");
  if (session.isAuthenticated) {
    if (!from.meta.requiresAuth) return { name: "home" };
    return from;
  }
}

const routes = [
  {
    path: "/",
    redirect: (to) => {
      return { name: "home" };
    },
  },

  {
    path: "/chat/",
    name: "home",
    component: () => import("@/views/ChatView.vue"),
  },

  {
    path: "/test/",
    name: "test",
    component: () => import("@/views/TestView.vue"),
  },

  {
    path: "/login/",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
    beforeEnter: IfNotAuthenticated,
  },

  {
    path: "/register/",
    name: "register",
    component: () => import("@/views/RegisterView.vue"),
    beforeEnter: IfNotAuthenticated,
  },
  {
    path: "/logout/",
    name: "logout",
    component: () => import("@/views/LogoutView.vue"),
  },
];

// initialize all routes with no beforeEnter attribute
routes.forEach((route) => {
  if (!route.beforeEnter) {
    route.beforeEnter = IfAuthenticated;
    (route.meta || (route.meta = {})).requiresAuth = true;
  }
});

const router = createRouter({
  mode: "history",
  routes,
  history: createWebHistory(import.meta.env.BASE_URL),
});

export default router;
