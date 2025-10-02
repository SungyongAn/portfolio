const MaterialSearch = {
    data() {
        return {
            form: {
                materialId: '',
                title: '',
                author: '',
                publisher: ''
            },
            searchResults: [] // バックエンドからの結果を格納
        };
    },

    methods: {
        async handleSearch() {
            try {
                const response = await fetch("http://127.0.0.1:8000/material/search", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ ...this.form })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || `HTTPエラー: ${response.status}`);
                }

                const result = await response.json();

                // result に検索結果が入っている想定
                if (Array.isArray(result)) {
                    this.searchResults = result;
                } else if (result.success && Array.isArray(result.data)) {
                    this.searchResults = result.data;
                } else {
                    this.searchResults = [];
                    alert(result.message || "検索結果が取得できませんでした");
                }

            } catch (error) {
                console.error("検索エラー:", error);
                alert("検索中にエラーが発生しました: " + error.message);
            }
        }
    },
    template: `
        <div class="p-3">
            <h4>資料検索</h4>
            <form @submit.prevent="handleSearch">
                <div class="mb-3">
                    <label class="form-label">資料ID</label>
                    <input v-model="form.materialId" type="text" class="form-control">
                </div>
                <div class="mb-3">
                    <label class="form-label">タイトル</label>
                    <input v-model="form.title" type="text" class="form-control">
                </div>
                <div class="mb-3">
                    <label class="form-label">著者名</label>
                    <input v-model="form.author" type="text" class="form-control">
                </div>
                <div class="mb-3">
                    <label class="form-label">出版社</label>
                    <input v-model="form.publisher" type="text" class="form-control">
                </div>
                <button 
                    type="submit"
                    class="btn btn-primary"
                    :disabled="!form.materialId && !form.title && !form.author && !form.publisher">
                    検索
                </button>
            </form>

            <div v-if="searchResults.length" class="mt-4">
                <h5>検索結果</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>資料ID</th>
                            <th>タイトル</th>
                            <th>著者</th>
                            <th>出版社</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in searchResults" :key="item.materialId">
                            <td>{{ item.materialId }}</td>
                            <td>{{ item.title }}</td>
                            <td>{{ item.author }}</td>
                            <td>{{ item.publisher }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `
};
