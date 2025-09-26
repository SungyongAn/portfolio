<template>
    <div class="card mb-4">
        <div class="card-body">
            <form @submit.prevent="handleSearch">
            <div class="row mb-3">
                <div class="col-md-3">
                    <select v-model="searchType" class="form-select">
                        <option value="userId">ユーザーID</option>
                        <option value="username">ユーザー名</option>
                        <option value="admission_year">入学年</option>
              <option value="graduation_year">卒業予定年</option>
              <option value="email">メールアドレス</option>
              <option value="affiliation">所属校</option>
            </select>
          </div>
          <div class="col-md-6">
            <input
              v-model="searchValue"
              :type="getInputType(searchType)"
              class="form-control"
              :placeholder="getInputPlaceholder(searchType)"
            />
          </div>
          <div class="col-md-3">
            <button class="btn btn-primary" :disabled="isLoading">
              検索
              <span
                v-if="isLoading"
                class="spinner-border spinner-border-sm ms-2"
              ></span>
            </button>
          </div>
        </div>
      </form>

      <div v-if="error" class="alert alert-warning">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      searchType: "userId",
      searchValue: "",
      error: "",
      isLoading: false,
    };
  },
  methods: {
    getInputType(type) {
      return type === "admission_year" || type === "graduation_year"
        ? "number"
        : "text";
    },
    getInputPlaceholder(type) {
      const map = {
        userId: "ユーザーIDを入力",
        username: "ユーザー名を入力",
        admission_year: "入学年を入力",
        graduation_year: "卒業予定年を入力",
        email: "メールアドレスを入力",
        affiliation: "所属校を入力",
      };
      return map[type] || "";
    },
    async handleSearch() {
      if (!this.searchValue.trim()) {
        this.error = "検索条件を入力してください。";
        return;
      }

      this.isLoading = true;
      this.error = "";

      let filter = {};
      if (
        this.searchType === "admission_year" ||
        this.searchType === "graduation_year"
      ) {
        const num = parseInt(this.searchValue);
        if (isNaN(num)) {
          this.error = "数値で入力してください。";
          this.isLoading = false;
          return;
        }
        filter[this.searchType] = num;
      } else {
        filter[this.searchType] = this.searchValue;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/account-management/search-accounts",
          {
            filters: [filter],
          }
        );
        this.$emit("search-results", response.data.users_list);
      } catch (err) {
        this.error = "検索中にエラーが発生しました";
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
