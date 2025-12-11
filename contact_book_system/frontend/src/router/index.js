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
  { path: "/", component: LoginForm },
  { path: "/menu", component: MainMenu },

  // Account
  { path: "/account-management", component: AccountManagementMenu },
  { path: "/account/form", component: AccountForm },
  { path: "/account/search", component: AccountSearch },
  { path: "/account/search-results", component: AccountSearchResults },
  { path: "/account/update", component: AccountUpdateTable },
  { path: "/yearly-processing", component: YearlyProcessingMenu },

  // Renrakucho
  { path: "/entry", component: EntryForm },
  { path: "/past-search", component: PastRenrakuchoSearch },
  { path: "/submission-status", component: SubmissionStatus },
  { path: "/class-entry", component: ClassEntryRenrakucho },
  { path: "/class-past", component: ClassPastRenrakucho },
  { path: "/nurse-dashboard", component: SchoolNurseDashboard },

  // Chat
  { path: "/chat", component: ChatRoomList },
  { path: "/chat/:id", component: ChatRoom },

  // Archive
  { path: "/archive", component: ArchiveManagement },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
