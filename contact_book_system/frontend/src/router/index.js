import { createRouter, createWebHistory } from "vue-router";

// Auth / Menu
import LoginForm from "../components/LoginForm.vue";
import MainMenu from "../components/MainMenu.vue";

// Account Management
import AccountManagementMenu from "../components/AccountManagement/AccountManagementMenu.vue";
import AccountForm from "../components/AccountManagement/AccountForm.vue";
import AccountSearch from "../components/AccountManagement/AccountSearch.vue";
import AccountSearchResults from "../components/AccountManagement/AccountSearchResults.vue";
import AccountUpdateTable from "../components/AccountManagement/AccountUpdateTable.vue";
import YearlyProcessingMenu from "../components/AccountManagement/YearlyProcessingMenu.vue";

// Renrakucho
import EntryForm from "../components/Renrakucho/EntryForm.vue";
import PastRenrakuchoSearch from "../components/Renrakucho/PastRenrakuchoSearch.vue";
import SubmissionStatus from "../components/Renrakucho/SubmissionStatus.vue";
import ClassEntryRenrakucho from "../components/Renrakucho/ClassEntryRenrakucho.vue";
import ClassPastRenrakucho from "../components/Renrakucho/ClassPastRenrakucho.vue";
import SchoolNurseDashboard from "../components/Renrakucho/SchoolNurseDashboard.vue";

// Chat
import ChatRoomList from "../components/ChatRoomList.vue";
import ChatRoom from "../components/ChatRoom.vue";

// Archive
import ArchiveManagement from "../components/ArchiveManagement.vue";

const routes = [
  { path: "/", component: LoginForm, props: true },
  { path: "/menu", component: MainMenu, props: true },

  // Account
  {
    path: "/account-management",
    name: "account-management",
    component: AccountManagementMenu,
    props: true,
  },
  {
    path: "/account/form",
    name: "account-form",
    component: AccountForm,
    props: true,
  },
  {
    path: "/account/search",
    name: "account-search",
    component: AccountSearch,
    props: true,
  },
  {
    path: "/account/search-results",
    name: "account-search-results",
    component: AccountSearchResults,
    props: true,
  },
  {
    path: "/account/update",
    name: "account-update",
    component: AccountUpdateTable,
    props: true,
  },
  {
    path: "/yearly-processing",
    name: "yearly-processing-menu",
    component: YearlyProcessingMenu,
    props: true,
  },

  // Renrakucho
  { path: "/entry", name: "entry-form", component: EntryForm, props: true },
  {
    path: "/past-search",
    name: "past-search",
    component: PastRenrakuchoSearch,
    props: true,
  },
  {
    path: "/submission-status",
    name: "submission-status",
    component: SubmissionStatus,
    props: true,
  },
  {
    path: "/class-entry",
    name: "class-entry-renrakucho",
    component: ClassEntryRenrakucho,
    props: true,
  },
  {
    path: "/class-past",
    name: "class-past-renrakucho",
    component: ClassPastRenrakucho,
    props: true,
  },
  {
    path: "/nurse-dashboard",
    name: "school-nurse-dashboard",
    component: SchoolNurseDashboard,
    props: true,
  },

  // Chat
  {
    path: "/chat",
    name: "chat-room-list",
    component: ChatRoomList,
    props: true,
  },
  { path: "/chat/:id", name: "chat-room", component: ChatRoom, props: true },

  // Archive
  {
    path: "/archive",
    name: "archive-management",
    component: ArchiveManagement,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
