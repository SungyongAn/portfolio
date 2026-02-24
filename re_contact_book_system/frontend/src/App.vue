<template>
  <div id="app">
    <!-- ログイン画面以外でヘッダーを表示 -->
    <AppHeader v-if="showHeader" />
    
    <!-- メインコンテンツ -->
    <main :class="{ 'with-header': showHeader }">
      <router-view />
    </main>

    <!-- フッター（オプション） -->
    <AppFooter v-if="showHeader" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

const route = useRoute()

// ログイン画面と404ページではヘッダーを非表示
const showHeader = computed(() => {
  const hiddenRoutes = ['/login', '/404']
  return !hiddenRoutes.includes(route.path)
})
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

main.with-header {
  padding-top: 1rem;
  min-height: calc(100vh - 56px); /* ヘッダーの高さを引く */
}
</style>