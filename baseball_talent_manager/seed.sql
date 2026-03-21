-- seed.sql
-- テスト用初期データ
-- パスワード: password123
-- ハッシュ値: $argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ

-- ユーザーデータ
INSERT INTO users (email, password_hash, name, grade, role, status) VALUES
-- マネージャー
('manager1@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '山田 花子', NULL, 'manager', 'active'),
('manager2@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '鈴木 美咲', NULL, 'manager', 'active'),
-- コーチ
('coach@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '伊藤 コーチ', NULL, 'coach', 'active'),
-- 監督
('director@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '渡辺 監督', NULL, 'director', 'active'),
-- 部員（1年生）
('member1_1@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '田中 太郎', 1, 'member', 'active'),
('member1_2@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '佐藤 次郎', 1, 'member', 'active'),
('member1_3@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '高橋 三郎', 1, 'member', 'active'),
('member1_4@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '松田 四郎', 1, 'member', 'active'),
('member1_5@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '木村 五郎', 1, 'member', 'active'),
-- 部員（2年生）
('member2_1@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '中村 六郎', 2, 'member', 'active'),
('member2_2@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '小林 七郎', 2, 'member', 'active'),
('member2_3@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '加藤 八郎', 2, 'member', 'active'),
('member2_4@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '吉田 九郎', 2, 'member', 'active'),
('member2_5@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '山本 十郎', 2, 'member', 'active'),
-- 部員（3年生）
('member3_1@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '松本 一郎', 3, 'member', 'active'),
('member3_2@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '井上 二郎', 3, 'member', 'active'),
('member3_3@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '木下 三郎', 3, 'member', 'active'),
('member3_4@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '清水 四郎', 3, 'member', 'active'),
('member3_5@jpt.com', '$argon2id$v=19$m=65536,t=3,p=4$b43xXmttTel9T2ntPWdsDQ$kTFEXNxGTMiAzIpe+/kqKaAUCqUfnSEdrIA2SsEy4GQ', '近藤 五郎', 3, 'member', 'active');

-- 測定記録データ
-- user_id: 5=田中太郎(1年), 6=佐藤次郎(1年), 7=高橋三郎(1年), 8=松田四郎(1年), 9=木村五郎(1年)
--          10=中村六郎(2年), 11=小林七郎(2年), 12=加藤八郎(2年), 13=吉田九郎(2年), 14=山本十郎(2年)
--          15=松本一郎(3年), 16=井上二郎(3年), 17=木下三郎(3年), 18=清水四郎(3年), 19=近藤五郎(3年)

-- =============================================
-- 第1回測定: 2025-08-01（approved）
-- =============================================

-- 田中 太郎（1年）- 走力型
INSERT INTO measurements (user_id, measurement_date, sprint_50m, base_running, throwing_distance, pitch_speed, batting_speed, swing_speed, bench_press, squat, status) VALUES
(5, '2025-08-01', 6.80, 14.20, 52.0, 105.0, 98.0, 102.0, 55.0, 75.0, 'approved'),
-- 佐藤 次郎（1年）- 肩力型
(6, '2025-08-01', 7.10, 14.80, 62.0, 118.0, 95.0, 98.0, 52.0, 72.0, 'approved'),
-- 高橋 三郎（1年）- 打力型
(7, '2025-08-01', 7.20, 15.00, 50.0, 100.0, 110.0, 115.0, 58.0, 80.0, 'approved'),
-- 松田 四郎（1年）- 筋力型
(8, '2025-08-01', 7.30, 15.20, 48.0, 98.0, 105.0, 108.0, 68.0, 95.0, 'approved'),
-- 木村 五郎（1年）- バランス型
(9, '2025-08-01', 7.00, 14.50, 55.0, 108.0, 100.0, 105.0, 60.0, 82.0, 'approved'),
-- 中村 六郎（2年）- 走力型
(10, '2025-08-01', 6.60, 13.80, 58.0, 112.0, 102.0, 106.0, 60.0, 82.0, 'approved'),
-- 小林 七郎（2年）- 肩力型
(11, '2025-08-01', 6.90, 14.30, 68.0, 125.0, 100.0, 104.0, 58.0, 78.0, 'approved'),
-- 加藤 八郎（2年）- 打力型
(12, '2025-08-01', 7.00, 14.60, 55.0, 106.0, 118.0, 122.0, 62.0, 85.0, 'approved'),
-- 吉田 九郎（2年）- 筋力型
(13, '2025-08-01', 7.10, 14.80, 52.0, 102.0, 112.0, 115.0, 72.0, 100.0, 'approved'),
-- 山本 十郎（2年）- バランス型
(14, '2025-08-01', 6.80, 14.10, 60.0, 115.0, 108.0, 112.0, 65.0, 88.0, 'approved'),
-- 松本 一郎（3年）- 走力型・エース
(15, '2025-08-01', 6.30, 13.20, 65.0, 125.0, 112.0, 118.0, 70.0, 95.0, 'approved'),
-- 井上 二郎（3年）- 肩力型
(16, '2025-08-01', 6.60, 13.70, 72.0, 132.0, 108.0, 112.0, 68.0, 90.0, 'approved'),
-- 木下 三郎（3年）- 打力型
(17, '2025-08-01', 6.80, 14.00, 62.0, 115.0, 125.0, 130.0, 72.0, 98.0, 'approved'),
-- 清水 四郎（3年）- 筋力型
(18, '2025-08-01', 6.90, 14.20, 58.0, 110.0, 118.0, 122.0, 80.0, 110.0, 'approved'),
-- 近藤 五郎（3年）- バランス型
(19, '2025-08-01', 6.50, 13.50, 68.0, 122.0, 115.0, 120.0, 72.0, 98.0, 'approved');

-- =============================================
-- 第2回測定: 2025-10-01（approved）
-- =============================================

-- 田中 太郎（1年）
INSERT INTO measurements (user_id, measurement_date, sprint_50m, base_running, throwing_distance, pitch_speed, batting_speed, swing_speed, bench_press, squat, status) VALUES
(5, '2025-10-01', 6.72, 14.00, 54.0, 107.0, 100.0, 104.0, 57.0, 78.0, 'approved'),
-- 佐藤 次郎（1年）
(6, '2025-10-01', 7.05, 14.65, 64.0, 120.0, 97.0, 100.0, 54.0, 74.0, 'approved'),
-- 高橋 三郎（1年）
(7, '2025-10-01', 7.12, 14.82, 52.0, 102.0, 113.0, 118.0, 60.0, 83.0, 'approved'),
-- 松田 四郎（1年）
(8, '2025-10-01', 7.22, 15.05, 50.0, 100.0, 107.0, 110.0, 70.0, 98.0, 'approved'),
-- 木村 五郎（1年）
(9, '2025-10-01', 6.92, 14.35, 57.0, 110.0, 102.0, 107.0, 62.0, 85.0, 'approved'),
-- 中村 六郎（2年）
(10, '2025-10-01', 6.52, 13.62, 60.0, 114.0, 104.0, 108.0, 62.0, 85.0, 'approved'),
-- 小林 七郎（2年）
(11, '2025-10-01', 6.82, 14.15, 70.0, 127.0, 102.0, 106.0, 60.0, 80.0, 'approved'),
-- 加藤 八郎（2年）
(12, '2025-10-01', 6.92, 14.45, 57.0, 108.0, 120.0, 124.0, 64.0, 87.0, 'approved'),
-- 吉田 九郎（2年）
(13, '2025-10-01', 7.02, 14.62, 54.0, 104.0, 114.0, 117.0, 74.0, 103.0, 'approved'),
-- 山本 十郎（2年）
(14, '2025-10-01', 6.72, 13.95, 62.0, 117.0, 110.0, 114.0, 67.0, 91.0, 'approved'),
-- 松本 一郎（3年）
(15, '2025-10-01', 6.22, 13.05, 67.0, 127.0, 114.0, 120.0, 72.0, 98.0, 'approved'),
-- 井上 二郎（3年）
(16, '2025-10-01', 6.52, 13.55, 74.0, 134.0, 110.0, 114.0, 70.0, 93.0, 'approved'),
-- 木下 三郎（3年）
(17, '2025-10-01', 6.72, 13.85, 64.0, 117.0, 127.0, 132.0, 74.0, 101.0, 'approved'),
-- 清水 四郎（3年）
(18, '2025-10-01', 6.82, 14.05, 60.0, 112.0, 120.0, 124.0, 82.0, 113.0, 'approved'),
-- 近藤 五郎（3年）
(19, '2025-10-01', 6.42, 13.35, 70.0, 124.0, 117.0, 122.0, 74.0, 101.0, 'approved');

-- =============================================
-- 第3回測定: 2025-12-01（approved）
-- =============================================

INSERT INTO measurements (user_id, measurement_date, sprint_50m, base_running, throwing_distance, pitch_speed, batting_speed, swing_speed, bench_press, squat, status) VALUES
-- 田中 太郎（1年）
(5, '2025-12-01', 6.65, 13.82, 56.0, 109.0, 102.0, 106.0, 59.0, 80.0, 'approved'),
-- 佐藤 次郎（1年）
(6, '2025-12-01', 6.98, 14.50, 66.0, 122.0, 99.0, 102.0, 56.0, 76.0, 'approved'),
-- 高橋 三郎（1年）
(7, '2025-12-01', 7.05, 14.65, 54.0, 104.0, 116.0, 121.0, 62.0, 86.0, 'approved'),
-- 松田 四郎（1年）
(8, '2025-12-01', 7.15, 14.88, 52.0, 102.0, 109.0, 112.0, 72.0, 101.0, 'approved'),
-- 木村 五郎（1年）
(9, '2025-12-01', 6.85, 14.20, 59.0, 112.0, 104.0, 109.0, 64.0, 88.0, 'approved'),
-- 中村 六郎（2年）
(10, '2025-12-01', 6.45, 13.45, 62.0, 116.0, 106.0, 110.0, 64.0, 88.0, 'approved'),
-- 小林 七郎（2年）
(11, '2025-12-01', 6.75, 14.00, 72.0, 129.0, 104.0, 108.0, 62.0, 82.0, 'approved'),
-- 加藤 八郎（2年）
(12, '2025-12-01', 6.85, 14.30, 59.0, 110.0, 122.0, 126.0, 66.0, 89.0, 'approved'),
-- 吉田 九郎（2年）
(13, '2025-12-01', 6.95, 14.45, 56.0, 106.0, 116.0, 119.0, 76.0, 106.0, 'approved'),
-- 山本 十郎（2年）
(14, '2025-12-01', 6.65, 13.80, 64.0, 119.0, 112.0, 116.0, 69.0, 94.0, 'approved'),
-- 松本 一郎（3年）
(15, '2025-12-01', 6.15, 12.90, 69.0, 129.0, 116.0, 122.0, 74.0, 101.0, 'approved'),
-- 井上 二郎（3年）
(16, '2025-12-01', 6.45, 13.40, 76.0, 136.0, 112.0, 116.0, 72.0, 96.0, 'approved'),
-- 木下 三郎（3年）
(17, '2025-12-01', 6.65, 13.70, 66.0, 119.0, 129.0, 134.0, 76.0, 104.0, 'approved'),
-- 清水 四郎（3年）
(18, '2025-12-01', 6.75, 13.90, 62.0, 114.0, 122.0, 126.0, 84.0, 116.0, 'approved'),
-- 近藤 五郎（3年）
(19, '2025-12-01', 6.35, 13.20, 72.0, 126.0, 119.0, 124.0, 76.0, 104.0, 'approved');

-- =============================================
-- 第4回測定: 2026-02-01（承認フロー確認用）
-- =============================================

-- approved（承認済み）
INSERT INTO measurements (user_id, measurement_date, sprint_50m, base_running, throwing_distance, pitch_speed, batting_speed, swing_speed, bench_press, squat, status) VALUES
(15, '2026-02-01', 6.10, 12.75, 71.0, 131.0, 118.0, 124.0, 76.0, 104.0, 'approved'),
(16, '2026-02-01', 6.40, 13.25, 78.0, 138.0, 114.0, 118.0, 74.0, 99.0, 'approved'),
(17, '2026-02-01', 6.60, 13.55, 68.0, 121.0, 131.0, 136.0, 78.0, 107.0, 'approved');

-- pending_coach（コーチ承認待ち）
INSERT INTO measurements (user_id, measurement_date, sprint_50m, base_running, throwing_distance, pitch_speed, batting_speed, swing_speed, bench_press, squat, status) VALUES
(18, '2026-02-01', 6.70, 13.75, 64.0, 116.0, 124.0, 128.0, 86.0, 119.0, 'pending_coach'),
(19, '2026-02-01', 6.30, 13.05, 74.0, 128.0, 121.0, 126.0, 78.0, 107.0, 'pending_coach');

-- pending_member（部員承認待ち）
INSERT INTO measurements (user_id, measurement_date, sprint_50m, base_running, throwing_distance, pitch_speed, batting_speed, swing_speed, bench_press, squat, status) VALUES
(5, '2026-02-01', 6.58, 13.65, 58.0, 111.0, 104.0, 108.0, 61.0, 82.0, 'pending_member'),
(6, '2026-02-01', 6.92, 14.35, 68.0, 124.0, 101.0, 104.0, 58.0, 78.0, 'pending_member'),
(10, '2026-02-01', 6.38, 13.28, 64.0, 118.0, 108.0, 112.0, 66.0, 91.0, 'pending_member');

-- rejected（否認）
INSERT INTO measurements (user_id, measurement_date, sprint_50m, base_running, throwing_distance, pitch_speed, batting_speed, swing_speed, bench_press, squat, status) VALUES
(7, '2026-02-01', 6.98, 14.48, 56.0, 106.0, 118.0, 123.0, 64.0, 88.0, 'rejected'),
(11, '2026-02-01', 6.68, 13.85, 74.0, 131.0, 106.0, 110.0, 64.0, 84.0, 'rejected');

-- draft（未送信）
INSERT INTO measurements (user_id, measurement_date, sprint_50m, base_running, throwing_distance, pitch_speed, batting_speed, swing_speed, bench_press, squat, status) VALUES
(8, '2026-02-01', 7.08, 14.72, 54.0, 104.0, 111.0, 114.0, 74.0, 104.0, 'draft'),
(12, '2026-02-01', 6.78, 14.12, 61.0, 112.0, 124.0, 128.0, 68.0, 92.0, 'draft');