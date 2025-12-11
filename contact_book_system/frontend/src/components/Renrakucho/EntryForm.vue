<template>
  <div class="d-flex justify-content-center mt-2 px-2">
    <div class="card p-4 w-100" style="max-width: 1200px">
      <!-- 提出済み -->
      <entry-result
        v-if="submittedEntry"
        :entry="submittedEntry"
        @new-entry="resetToNewEntry"
      ></entry-result>

      <!-- 確認画面 -->
      <div v-else-if="showConfirmation" class="alert alert-warning p-3">
        <h5>提出内容の確認</h5>
        <p><strong>入力日:</strong> {{ entryForm.inputDate }}</p>
        <p><strong>本日の体調:</strong> {{ entryForm.physicalCondition }}</p>
        <p><strong>本日のメンタル:</strong> {{ entryForm.mentalState }}</p>
        <p>
          <strong>体調・メンタルについて:</strong>
          {{ entryForm.physicalMentalNotes }}
        </p>
        <p><strong>前日の振り返り:</strong></p>
        <pre style="white-space: pre-wrap; word-wrap: break-word">
          {{ combinedReflection }}
        </pre>

        <div class="d-flex gap-2 flex-wrap">
          <button
            class="btn btn-secondary"
            @click="cancelConfirmation"
            :disabled="isSubmitting"
          >
            戻る
          </button>

          <button
            class="btn btn-success"
            @click="submitEntry"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? "提出中..." : "提出" }}
          </button>
        </div>
      </div>

      <!-- 未提出フォーム -->
      <div v-else>
        <!-- メッセージ -->
        <div
          v-if="message"
          :class="[
            'alert',
            messageType === 'success' ? 'alert-success' : 'alert-danger',
          ]"
          class="mb-3"
        >
          {{ message }}
        </div>

        <!-- 2カラムレイアウト -->
        <div class="row">
          <!-- 左列 -->
          <div class="col-md-5">
            <!-- 日付 -->
            <div class="mb-3">
              <label class="form-label">日付</label>
              <input
                type="date"
                class="form-control"
                v-model="entryForm.inputDate"
                disabled
              />
            </div>

            <!-- 体調 -->
            <div class="mb-3">
              <label class="form-label">本日の体調（1〜5）</label>
              <div
                class="d-flex justify-content-between"
                style="max-width: 300px"
              >
                <template v-for="n in 5" :key="n">
                  <label class="d-flex flex-column align-items-center">
                    <span style="font-size: 0.8rem">{{ n }}</span>
                    <input
                      type="radio"
                      :value="n"
                      v-model.number="entryForm.physicalCondition"
                    />
                  </label>
                </template>
              </div>
            </div>

            <!-- メンタル -->
            <div class="mb-3">
              <label class="form-label">本日のメンタル（1〜5）</label>
              <div
                class="d-flex justify-content-between"
                style="max-width: 300px"
              >
                <template v-for="n in 5" :key="n">
                  <label class="d-flex flex-column align-items-center">
                    <span style="font-size: 0.8rem">{{ n }}</span>
                    <input
                      type="radio"
                      :value="n"
                      v-model.number="entryForm.mentalState"
                    />
                  </label>
                </template>
              </div>
            </div>

            <!-- 自由記述 -->
            <div class="mb-3">
              <label class="form-label">体調・メンタルについて</label>
              <textarea
                class="form-control"
                rows="5"
                v-model="entryForm.physicalMentalNotes"
                :disabled="isSubmitting"
              ></textarea>
            </div>
          </div>

          <!-- 右列：振り返り -->
          <div class="col-md-7">
            <div class="mb-3">
              <h5 class="mb-3">
                前日の振り返り <span class="text-danger">*</span>
              </h5>

              <div class="mb-3">
                <label class="form-label fw-bold">授業</label>
                <textarea
                  class="form-control"
                  rows="4"
                  v-model="entryForm.reflection.lesson"
                ></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold">部活動</label>
                <textarea
                  class="form-control"
                  rows="4"
                  v-model="entryForm.reflection.club"
                ></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold">その他</label>
                <textarea
                  class="form-control"
                  rows="4"
                  v-model="entryForm.reflection.other"
                ></textarea>
              </div>
            </div>
          </div>
        </div>

        <!-- ボタン -->
        <div class="d-flex justify-content-end gap-2 flex-wrap mt-3">
          <button
            class="btn btn-secondary"
            @click="resetForm"
            :disabled="isSubmitting"
          >
            リセット
          </button>

          <button
            class="btn btn-primary"
            @click="confirmEntry"
            :disabled="!canSubmit || isSubmitting"
          >
            確認
          </button>
        </div>
      </div>
      <!-- end 未提出 -->
    </div>
  </div>
</template>

<script>
import EntryResult from "./EntryResult.vue";
import axios from "axios";

export default {
  name: "EntryForm",
  components: { EntryResult },
  props: ["currentUser"],
  emits: ["updateTitle"],
  data() {
    const today = new Date().toISOString().slice(0, 10);
    return {
      submittedEntry: null,
      submittedDate: today,
      entryForm: {
        inputDate: today,
        physicalCondition: null,
        mentalState: null,
        physicalMentalNotes: "",
        reflection: {
          lesson: "",
          club: "",
          other: "",
        },
      },
      isSubmitting: false,
      message: "",
      messageType: "",
      showConfirmation: false,
    };
  },
  computed: {
    canSubmit() {
      return (
        this.entryForm.physicalCondition !== null &&
        this.entryForm.mentalState !== null &&
        (this.entryForm.reflection.lesson.trim() ||
          this.entryForm.reflection.club.trim() ||
          this.entryForm.reflection.other.trim())
      );
    },
    combinedReflection() {
      return (
        `授業：\n${this.entryForm.reflection.lesson}\n\n` +
        `部活動：\n${this.entryForm.reflection.club}\n\n` +
        `その他：\n${this.entryForm.reflection.other}`
      );
    },
  },
  mounted() {
    this.$emit("updateTitle", {
      title: "連絡帳の作成",
      icon: "fas fa-book",
      showBackButton: true,
    });
  },
  beforeUnmount() {
    this.$emit("updateTitle", {
      title: "",
      icon: "",
      showBackButton: false,
    });
  },
  methods: {
    confirmEntry() {
      if (!this.canSubmit) return;
      this.showConfirmation = true;
    },
    cancelConfirmation() {
      this.showConfirmation = false;
    },
    async submitEntry() {
      if (!this.canSubmit) return;

      this.isSubmitting = true;
      this.message = "";
      this.messageType = "";

      const payload = {
        student_id: Number(this.currentUser.id),
        submitted_date: this.submittedDate,
        target_date: this.entryForm.inputDate,
        physical_condition: Number(this.entryForm.physicalCondition),
        mental_state: Number(this.entryUser.mentalState),
        physical_mental_notes: this.entryForm.physicalMentalNotes.trim(),
        daily_reflection: this.combinedReflection.trim(),
      };

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/renrakucho-management/entry-renrakucho",
          payload
        );

        if (response.data.success) {
          this.submittedEntry = response.data.data || payload;
          this.showConfirmation = false;
        } else {
          this.showConfirmation = false;
          this.message = response.data.message || "提出に失敗しました。";
          this.messageType = "error";
        }
      } catch (error) {
        this.showConfirmation = false;
        this.messageType = "error";
        this.message =
          error.response?.data?.detail ||
          "提出に失敗しました（サーバー通信エラー）。";
      } finally {
        this.isSubmitting = false;
      }
    },
    resetForm() {
      this.entryForm.physicalCondition = null;
      this.entryForm.mentalState = null;
      this.entryForm.physicalMentalNotes = "";
      this.entryForm.reflection.lesson = "";
      this.entryForm.reflection.club = "";
      this.entryForm.reflection.other = "";
      this.showConfirmation = false;
      this.message = "";
      this.messageType = "";
    },
    resetToNewEntry() {
      this.submittedEntry = null;
      this.resetForm();
    },
  },
};
</script>
