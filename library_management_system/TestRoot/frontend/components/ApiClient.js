// APIクライアント - バックエンド(FastAPI)との通信を管理

const ApiClient = {
    // バックエンドのベースURL (環境に応じて変更)
    baseURL: 'http://localhost:8000',

    /**
     * 汎用APIリクエスト送信メソッド
     * @param {string} endpoint - APIエンドポイント (例: '/api/login')
     * @param {object} payload - 送信するペイロードオブジェクト
     * @param {string} method - HTTPメソッド ('GET', 'POST', 'PUT', 'DELETE')
     * @returns {Promise<object>} レスポンスデータ
     */
    async sendRequest(endpoint, payload = {}, method = 'POST') {
        try {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            };

            // GETメソッド以外はbodyを追加
            if (method !== 'GET') {
                options.body = JSON.stringify(payload);
            }

            console.log(`[API Request] ${method} ${this.baseURL}${endpoint}`);
            console.log('[Payload]', payload);

            const response = await fetch(`${this.baseURL}${endpoint}`, options);

            // レスポンスのログ
            console.log(`[API Response] Status: ${response.status}`);

            // エラーハンドリング
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({
                    message: `HTTPエラー: ${response.status}`
                }));
                throw new Error(errorData.message || `HTTPエラー: ${response.status}`);
            }

            const data = await response.json();
            console.log('[Response Data]', data);

            return {
                success: true,
                data: data,
                message: data.message || '成功'
            };

        } catch (error) {
            console.error('[API Error]', error);
            return {
                success: false,
                data: null,
                message: error.message || 'APIリクエストに失敗しました'
            };
        }
    },

    /**
     * AllPayloadスキーマに基づくペイロード作成
     * @param {object} params - パラメータオブジェクト
     * @returns {object} バリデーション済みペイロード
     */
    createPayload(params = {}) {
        const payload = {
            // ユーザー関連
            user_id: params.user_id || null,
            username: params.username || null,
            admission_year: params.admission_year || null,
            graduation_year: params.graduation_year || null,
            email: params.email || null,
            password: params.password || null,
            
            // 資料関連
            material_id: params.material_id || null,
            barcode: params.barcode || null,
            title: params.title || null,
            author: params.author || null,
            publisher: params.publisher || null,
            ndc_code: params.ndc_code || null,
            type_name: params.type_name || null,
            affiliation: params.affiliation || null,
            shelf: params.shelf || null,
            registration_date: params.registration_date || null
        };

        // nullの値を除外 (Optionalフィールドのため)
        return Object.fromEntries(
            Object.entries(payload).filter(([_, v]) => v !== null)
        );
    },

    // ===== 認証関連API =====

    /**
     * ログイン
     */
    async login(userId, password) {
        const payload = this.createPayload({
            user_id: userId,
            password: password
        });
        return await this.sendRequest('/api/login', payload, 'POST');
    },

    /**
     * ログアウト
     */
    async logout(userId) {
        const payload = this.createPayload({
            user_id: userId
        });
        return await this.sendRequest('/api/logout', payload, 'POST');
    },

    // ===== ユーザー管理API =====

    /**
     * ユーザー登録
     */
    async registerUser(userData) {
        const payload = this.createPayload({
            user_id: userData.userId,
            username: userData.username,
            admission_year: userData.admissionYear,
            graduation_year: userData.graduationYear,
            email: userData.email,
            password: userData.password,
            affiliation: userData.affiliation
        });
        return await this.sendRequest('/api/users/register', payload, 'POST');
    },

    /**
     * ユーザー削除
     */
    async deleteUser(userId) {
        const payload = this.createPayload({
            user_id: userId
        });
        return await this.sendRequest('/api/users/delete', payload, 'DELETE');
    },

    /**
     * ユーザー情報取得
     */
    async getUserInfo(userId) {
        const payload = this.createPayload({
            user_id: userId
        });
        return await this.sendRequest('/api/users/info', payload, 'GET');
    },

    /**
     * ユーザー情報更新
     */
    async updateUser(userData) {
        const payload = this.createPayload({
            user_id: userData.userId,
            username: userData.username,
            email: userData.email,
            affiliation: userData.affiliation,
            admission_year: userData.admissionYear,
            graduation_year: userData.graduationYear
        });
        return await this.sendRequest('/api/users/update', payload, 'PUT');
    },

    // ===== 資料管理API =====

    /**
     * 資料検索
     */
    async searchMaterials(searchParams) {
        const payload = this.createPayload({
            title: searchParams.title,
            author: searchParams.author,
            publisher: searchParams.publisher,
            ndc_code: searchParams.ndcCode,
            type_name: searchParams.typeName,
            barcode: searchParams.barcode
        });
        return await this.sendRequest('/api/materials/search', payload, 'POST');
    },

    /**
     * 資料登録
     */
    async registerMaterial(materialData) {
        const payload = this.createPayload({
            barcode: materialData.barcode,
            title: materialData.title,
            author: materialData.author,
            publisher: materialData.publisher,
            ndc_code: materialData.ndcCode,
            type_name: materialData.typeName,
            affiliation: materialData.affiliation,
            shelf: materialData.shelf,
            registration_date: materialData.registrationDate
        });
        return await this.sendRequest('/api/materials/register', payload, 'POST');
    },

    /**
     * 資料更新
     */
    async updateMaterial(materialData) {
        const payload = this.createPayload({
            material_id: materialData.materialId,
            barcode: materialData.barcode,
            title: materialData.title,
            author: materialData.author,
            publisher: materialData.publisher,
            ndc_code: materialData.ndcCode,
            type_name: materialData.typeName,
            affiliation: materialData.affiliation,
            shelf: materialData.shelf
        });
        return await this.sendRequest('/api/materials/update', payload, 'PUT');
    },

    /**
     * 資料削除
     */
    async deleteMaterial(materialId) {
        const payload = this.createPayload({
            material_id: materialId
        });
        return await this.sendRequest('/api/materials/delete', payload, 'DELETE');
    },

    /**
     * 資料詳細取得
     */
    async getMaterialDetail(materialId) {
        const payload = this.createPayload({
            material_id: materialId
        });
        return await this.sendRequest('/api/materials/detail', payload, 'GET');
    },

    // ===== テスト用メソッド =====

    /**
     * テスト接続 - バックエンドの疎通確認
     */
    async testConnection() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            return response.ok;
        } catch (error) {
            console.error('バックエンド接続エラー:', error);
            return false;
        }
    },

    /**
     * カスタムリクエスト - 任意のエンドポイントとペイロードで送信
     */
    async customRequest(endpoint, params, method = 'POST') {
        const payload = this.createPayload(params);
        return await this.sendRequest(endpoint, payload, method);
    }
};

// グローバルに公開
window.ApiClient = ApiClient;
