<template>
  <div class="container mt-4">
    <h2 class="mb-4">ダッシュボード</h2>

    <div class="row g-4">
      <!-- 測定結果の入力 / 承認依頼 -->
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>測定結果の入力/承認依頼</h5>
            <router-link :to="`/manager/record`" class="btn btn-primary mt-3">
              測定結果の入力
            </router-link>
          </div>
        </div>
      </div>

      <!-- 承認依頼中のステータス確認 -->
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>承認依頼中のステータス確認</h5>
            <router-link :to="`/manager/status`" class="btn btn-warning mt-3">
              承認依頼中のステータス確認
            </router-link>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
</script>
