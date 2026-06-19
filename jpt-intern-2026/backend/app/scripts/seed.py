from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.department import Department
from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus, DevelopmentMethod
from app.models.project_budget import ProjectBudget
from app.models.task import Task, TaskStatus
from app.models.worklog import Worklog
from app.models.expense import Expense, ExpenseType
from app.models.notification import Notification
from app.utils.security import hash_password
from decimal import Decimal

# ── 日付ヘルパー ──────────────────────────────────────────
TODAY = date.today()
DEMO_WINDOW_DAYS = (
    10  # 提出後の動作確認が数日ずれても「今日期限」タスクを確認できるようにする
)


def days_ago(n: int) -> str:
    return (TODAY - timedelta(days=n)).isoformat()


def days_later(n: int) -> str:
    return (TODAY + timedelta(days=n)).isoformat()


def days_offset(n: int) -> str:
    """提出後の確認日ずれに対応するため、今日基準の任意日付を返す"""
    return (TODAY + timedelta(days=n)).isoformat()


def today() -> str:
    return TODAY.isoformat()


def seed():
    db: Session = SessionLocal()
    try:
        if db.query(Department).count() > 0:
            print("シードデータは既に存在します。スキップします。")
            return

        print("シードデータを投入中...")

        # ── 部門 ────────────────────────────────────────────
        dept_product = Department(name="プロダクト開発部")
        dept_cs = Department(name="カスタマーソリューション部")
        dept_hq = Department(name="開発本部")
        db.add_all([dept_product, dept_cs, dept_hq])
        db.flush()
        print(
            f"  部門を作成しました: {dept_product.name}, {dept_cs.name}, {dept_hq.name}"
        )

        # ── ユーザー ─────────────────────────────────────────
        users = [
            User(
                name="田中 翔太",
                email="tanaka@nextflow.example.com",
                hashed_password=hash_password("password"),
                role=UserRole.APPLICANT,
                department_id=dept_product.id,
            ),
            User(
                name="佐藤 美咲",
                email="sato@nextflow.example.com",
                hashed_password=hash_password("password"),
                role=UserRole.APPLICANT,
                department_id=dept_cs.id,
            ),
            User(
                name="鈴木 健一",
                email="suzuki@nextflow.example.com",
                hashed_password=hash_password("password"),
                role=UserRole.DEPT_MANAGER,
                department_id=dept_product.id,
            ),
            User(
                name="山田 誠",
                email="yamada@nextflow.example.com",
                hashed_password=hash_password("password"),
                role=UserRole.DEPT_MANAGER,
                department_id=dept_cs.id,
            ),
            User(
                name="高橋 裕子",
                email="takahashi@nextflow.example.com",
                hashed_password=hash_password("password"),
                role=UserRole.HQ_MANAGER,
                department_id=dept_hq.id,
            ),
            User(
                name="亀田 大輔",
                email="kameda@nextflow.example.com",
                hashed_password=hash_password("password"),
                role=UserRole.TASK_MEMBER,
                department_id=dept_product.id,
            ),
            User(
                name="斉藤 彩香",
                email="saito@nextflow.example.com",
                hashed_password=hash_password("password"),
                role=UserRole.TASK_MEMBER,
                department_id=dept_cs.id,
            ),
            User(
                name="林 直樹",
                email="hayashi@nextflow.example.com",
                hashed_password=hash_password("password"),
                role=UserRole.TASK_MEMBER,
                department_id=dept_product.id,
            ),
            User(
                name="中村 葵",
                email="nakamura@nextflow.example.com",
                hashed_password=hash_password("password"),
                role=UserRole.TASK_MEMBER,
                department_id=dept_cs.id,
            ),
        ]
        db.add_all(users)
        db.flush()
        tanaka, sato, suzuki, yamada, takahashi, kameda, saito, hayashi, nakamura = (
            users
        )
        print(f"  ユーザーを作成しました: {[u.name for u in users]}")

        # ════════════════════════════════════════════════════
        # プロダクト開発部 案件（田中 翔太）
        # ════════════════════════════════════════════════════

        # ── 案件P1: FlowBase v3.2（進行中・ウォーターフォール）────
        project_p1 = Project(
            name="FlowBase v3.2 ワークフロー分岐機能",
            description="FlowBaseの次期バージョンにおけるワークフロー分岐機能の開発。条件分岐・並列処理・ループ処理に対応し、顧客の複雑な業務フローを実現する。",
            status=ProjectStatus.IN_PROGRESS,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=tanaka.id,
            department_id=dept_product.id,
            budget_amount=12_800_000,
            planned_months=12,
            start_date=days_ago(86),
            end_date=days_later(33),
        )
        db.add(project_p1)
        db.flush()
        db.add(
            ProjectBudget(
                project_id=project_p1.id,
                budget_amount=12_800_000,
                unit_price=1_000_000,
                planned_months=12,
                actual_amount=8_000_000,
            )
        )
        db.add_all(
            [
                Task(
                    project_id=project_p1.id,
                    phase_name="要件定義",
                    name="要件定義・仕様策定",
                    assignee_id=tanaka.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(86),
                    due_date=days_ago(72),
                ),
                Task(
                    project_id=project_p1.id,
                    phase_name="基本設計",
                    name="アーキテクチャ設計・API設計",
                    assignee_id=kameda.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(71),
                    due_date=days_ago(58),
                ),
                Task(
                    project_id=project_p1.id,
                    phase_name="実装",
                    name="バックエンド実装（分岐エンジン）",
                    assignee_id=tanaka.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(57),
                    due_date=days_ago(27),
                ),
                # 今日期限タスク（deadline）
                Task(
                    project_id=project_p1.id,
                    phase_name="実装",
                    name="フロントエンドUI実装",
                    assignee_id=kameda.id,
                    status=TaskStatus.IN_PROGRESS,
                    progress=60,
                    start_date=days_ago(27),
                    due_date=today(),
                ),
                # 継続対応中タスク（in_progress）
                Task(
                    project_id=project_p1.id,
                    phase_name="実装",
                    name="パフォーマンス計測・改善",
                    assignee_id=hayashi.id,
                    status=TaskStatus.IN_PROGRESS,
                    progress=50,
                    start_date=days_ago(10),
                    due_date=days_later(10),
                ),
                Task(
                    project_id=project_p1.id,
                    phase_name="結合テスト",
                    name="結合テスト・バグ修正",
                    assignee_id=tanaka.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_later(3),
                    due_date=days_later(23),
                ),
                Task(
                    project_id=project_p1.id,
                    phase_name="リリース",
                    name="リリース・ドキュメント作成",
                    assignee_id=kameda.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_later(24),
                    due_date=days_later(33),
                ),
                # 期限超過タスク（部門別期限超過グラフ確認用）
                Task(
                    project_id=project_p1.id,
                    phase_name="実装",
                    name="分岐条件レビュー修正（期限超過）",
                    assignee_id=hayashi.id,
                    status=TaskStatus.IN_PROGRESS,
                    progress=40,
                    start_date=days_ago(14),
                    due_date=days_ago(1),
                ),
            ]
        )
        db.add_all(
            [
                Worklog(
                    project_id=project_p1.id,
                    work_month=days_ago(86)[:7],
                    actual_months=Decimal("2.00"),
                ),
                Worklog(
                    project_id=project_p1.id,
                    work_month=days_ago(57)[:7],
                    actual_months=Decimal("3.00"),
                ),
                Worklog(
                    project_id=project_p1.id,
                    work_month=days_ago(27)[:7],
                    actual_months=Decimal("2.50"),
                ),
            ]
        )
        db.add(
            Expense(
                project_id=project_p1.id,
                expense_type=ExpenseType.LICENSE,
                amount=200_000,
                description="開発環境ライセンス費用",
                expense_date=days_ago(76),
            )
        )
        db.add_all(
            [
                Notification(
                    user_id=tanaka.id,
                    project_id=project_p1.id,
                    title="案件が承認されました",
                    message=f"「{project_p1.name}」が承認されました",
                    is_read=True,
                ),
                Notification(
                    user_id=tanaka.id,
                    project_id=project_p1.id,
                    title="案件が開始されました",
                    message=f"「{project_p1.name}」が着手されました",
                    is_read=True,
                ),
                Notification(
                    user_id=kameda.id,
                    project_id=project_p1.id,
                    title="案件にアサインされました",
                    message=f"「{project_p1.name}」にアサインされました",
                    is_read=False,
                ),
            ]
        )
        print(f"  案件を作成しました: {project_p1.name}")

        # ── 案件P2: 認証基盤リプレイス（部門承認待ち）──
        project_p2 = Project(
            name="プラットフォーム共通認証基盤リプレイス",
            description="現行の認証基盤をOAuth2/OIDCベースにリプレイス。セキュリティ強化と各サービスへのSSO対応を実現する。",
            status=ProjectStatus.PENDING_DEPT,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=tanaka.id,
            department_id=dept_product.id,
            budget_amount=8_000_000,
            planned_months=8,
            start_date=days_later(3),
            end_date=days_later(245),
        )
        db.add(project_p2)
        db.flush()
        db.add(
            Notification(
                user_id=suzuki.id,
                project_id=project_p2.id,
                title="新規案件申請",
                message=f"「{project_p2.name}」の承認依頼が届いています",
                is_read=False,
            )
        )
        print(f"  案件を作成しました: {project_p2.name}")

        # ── 案件P3: FlowBase モバイル対応（本部承認待ち）──
        project_p3 = Project(
            name="FlowBase モバイル対応SDK開発",
            description="FlowBaseのモバイル向けSDKを開発し、iOS・Androidアプリからワークフローを操作できるようにする。",
            status=ProjectStatus.PENDING_HQ,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=tanaka.id,
            department_id=dept_product.id,
            budget_amount=9_500_000,
            planned_months=10,
            start_date=days_later(34),
            end_date=days_later(337),
        )
        db.add(project_p3)
        db.flush()
        db.add(
            Notification(
                user_id=takahashi.id,
                project_id=project_p3.id,
                title="新規案件申請（最終承認依頼）",
                message=f"「{project_p3.name}」の最終承認依頼が届いています",
                is_read=False,
            )
        )
        print(f"  案件を作成しました: {project_p3.name}")

        # ── 案件P4: パフォーマンス改善（承認済）──
        project_p4 = Project(
            name="FlowBase APIパフォーマンス改善",
            description="高負荷時のAPIレスポンス遅延を解消するため、クエリ最適化・キャッシュ導入・非同期処理化を実施する。",
            status=ProjectStatus.APPROVED,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=tanaka.id,
            department_id=dept_product.id,
            budget_amount=3_200_000,
            planned_months=4,
            start_date=days_later(17),
            end_date=days_later(140),
        )
        db.add(project_p4)
        db.flush()
        db.add(
            ProjectBudget(
                project_id=project_p4.id,
                budget_amount=3_200_000,
                unit_price=800_000,
                planned_months=4,
                actual_amount=0,
            )
        )
        db.add_all(
            [
                # 今日開始タスク（starting）
                Task(
                    project_id=project_p4.id,
                    phase_name="調査",
                    name="ボトルネック調査・計測",
                    assignee_id=tanaka.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=today(),
                    due_date=days_later(30),
                ),
                Task(
                    project_id=project_p4.id,
                    phase_name="実装",
                    name="クエリ最適化",
                    assignee_id=kameda.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_later(31),
                    due_date=days_later(75),
                ),
                Task(
                    project_id=project_p4.id,
                    phase_name="テスト",
                    name="テスト環境構築・負荷テスト",
                    assignee_id=hayashi.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_later(63),
                    due_date=days_later(125),
                ),
                Task(
                    project_id=project_p4.id,
                    phase_name="実装",
                    name="キャッシュ導入・非同期処理化",
                    assignee_id=tanaka.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_later(95),
                    due_date=days_later(140),
                ),
            ]
        )
        # 提出後の確認日が数日ずれても、TASK_MEMBERで「今日期限」を確認できるデモ用タスク
        db.add_all(
            [
                Task(
                    project_id=project_p4.id,
                    phase_name="確認",
                    name=f"提出後確認用タスク（{offset}日後期限）",
                    assignee_id=kameda.id if offset % 2 else hayashi.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_offset(max(offset - 1, 0)),
                    due_date=days_offset(offset),
                )
                for offset in range(1, DEMO_WINDOW_DAYS + 1)
            ]
        )

        db.add(
            Notification(
                user_id=tanaka.id,
                project_id=project_p4.id,
                title="案件が承認されました",
                message=f"「{project_p4.name}」が承認されました",
                is_read=False,
            )
        )
        print(f"  案件を作成しました: {project_p4.name}")

        # ── 案件P5: 多言語対応（完了）──
        project_p5 = Project(
            name="FlowBase 多言語対応（英語・中国語）",
            description="FlowBaseのUI・メッセージリソースを英語・中国語に対応させ、海外顧客への展開基盤を整備する。",
            status=ProjectStatus.COMPLETED,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=tanaka.id,
            department_id=dept_product.id,
            budget_amount=5_000_000,
            planned_months=5,
            start_date=days_ago(238),
            end_date=days_ago(86),
        )
        db.add(project_p5)
        db.flush()
        db.add(
            ProjectBudget(
                project_id=project_p5.id,
                budget_amount=5_000_000,
                unit_price=900_000,
                planned_months=5,
                actual_amount=4_850_000,
            )
        )
        db.add_all(
            [
                Task(
                    project_id=project_p5.id,
                    phase_name="実装",
                    name="翻訳リソース整備",
                    assignee_id=tanaka.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(238),
                    due_date=days_ago(177),
                ),
                Task(
                    project_id=project_p5.id,
                    phase_name="実装",
                    name="UI実装・動作確認",
                    assignee_id=tanaka.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(176),
                    due_date=days_ago(116),
                ),
                Task(
                    project_id=project_p5.id,
                    phase_name="リリース",
                    name="リリース対応",
                    assignee_id=tanaka.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(115),
                    due_date=days_ago(86),
                ),
            ]
        )
        db.add(
            Notification(
                user_id=tanaka.id,
                project_id=project_p5.id,
                title="案件が完了しました",
                message=f"「{project_p5.name}」が完了しました",
                is_read=True,
            )
        )
        print(f"  案件を作成しました: {project_p5.name}")

        # ── 案件P6: セキュリティ診断対応（却下）──
        project_p6 = Project(
            name="FlowBase セキュリティ診断対応",
            description="外部セキュリティ診断で指摘された脆弱性の修正対応。XSS・SQLインジェクション・認証バイパス等の修正を行う。",
            status=ProjectStatus.REJECTED,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=tanaka.id,
            department_id=dept_product.id,
            budget_amount=2_000_000,
            planned_months=2,
            start_date=days_ago(27),
            end_date=days_later(33),
            reject_reason="予算計上時期が次期以降となるため却下。次回申請時に再提出すること。",
        )
        db.add(project_p6)
        db.flush()
        db.add(
            Notification(
                user_id=tanaka.id,
                project_id=project_p6.id,
                title="案件が却下されました",
                message=f"「{project_p6.name}」が却下されました",
                is_read=False,
            )
        )
        print(f"  案件を作成しました: {project_p6.name}")

        # ── 案件P7: BI連携プラグイン（ドラフト）──
        project_p7 = Project(
            name="FlowBase BI連携プラグイン開発",
            description="TableauやPower BIと連携するプラグインを開発し、ワークフローデータの可視化・分析を可能にする。",
            status=ProjectStatus.DRAFT,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=tanaka.id,
            department_id=dept_product.id,
            budget_amount=6_000_000,
            planned_months=6,
            start_date=days_later(64),
            end_date=days_later(247),
        )
        db.add(project_p7)
        db.flush()
        print(f"  案件を作成しました: {project_p7.name}（下書き）")

        # ════════════════════════════════════════════════════
        # カスタマーソリューション部 案件（佐藤 美咲）
        # ════════════════════════════════════════════════════

        # ── 案件C1: ABC商事（進行中・ウォーターフォール）──
        project_c1 = Project(
            name="ABC商事 請求書ワークフローカスタマイズ",
            description="ABC商事向けのFlowBaseカスタマイズ案件。請求書承認ワークフローに特殊な条件分岐（金額閾値による承認者変更）を追加実装する。",
            status=ProjectStatus.IN_PROGRESS,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=sato.id,
            department_id=dept_cs.id,
            budget_amount=4_800_000,
            planned_months=6,
            start_date=days_ago(97),
            end_date=days_ago(13),
        )
        db.add(project_c1)
        db.flush()
        db.add(
            ProjectBudget(
                project_id=project_c1.id,
                budget_amount=4_800_000,
                unit_price=900_000,
                planned_months=6,
                actual_amount=4_200_000,
            )
        )
        db.add_all(
            [
                Task(
                    project_id=project_c1.id,
                    phase_name="要件定義",
                    name="顧客要件ヒアリング・仕様確定",
                    assignee_id=sato.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(97),
                    due_date=days_ago(86),
                ),
                Task(
                    project_id=project_c1.id,
                    phase_name="実装",
                    name="カスタマイズ実装",
                    assignee_id=saito.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(85),
                    due_date=days_ago(43),
                ),
                # 継続対応中タスク（in_progress）
                Task(
                    project_id=project_c1.id,
                    phase_name="テスト",
                    name="顧客環境でのテスト",
                    assignee_id=sato.id,
                    status=TaskStatus.IN_PROGRESS,
                    progress=80,
                    start_date=days_ago(10),
                    due_date=days_later(5),
                ),
                # 期限超過タスク（部門別期限超過グラフ確認用）
                Task(
                    project_id=project_c1.id,
                    phase_name="テスト",
                    name="顧客指摘事項の再確認（期限超過）",
                    assignee_id=nakamura.id,
                    status=TaskStatus.IN_PROGRESS,
                    progress=60,
                    start_date=days_ago(12),
                    due_date=days_ago(2),
                ),
                # 今日期限タスク（deadline）
                Task(
                    project_id=project_c1.id,
                    phase_name="納品",
                    name="ドキュメント整備・引継ぎ",
                    assignee_id=nakamura.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_ago(3),
                    due_date=today(),
                ),
                Task(
                    project_id=project_c1.id,
                    phase_name="納品",
                    name="納品・検収対応",
                    assignee_id=saito.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_ago(3),
                    due_date=days_later(3),
                ),
            ]
        )
        db.add_all(
            [
                Worklog(
                    project_id=project_c1.id,
                    work_month=days_ago(97)[:7],
                    actual_months=Decimal("1.00"),
                ),
                Worklog(
                    project_id=project_c1.id,
                    work_month=days_ago(66)[:7],
                    actual_months=Decimal("1.50"),
                ),
                Worklog(
                    project_id=project_c1.id,
                    work_month=days_ago(35)[:7],
                    actual_months=Decimal("1.50"),
                ),
            ]
        )
        db.add_all(
            [
                Expense(
                    project_id=project_c1.id,
                    expense_type=ExpenseType.OUTSOURCING,
                    amount=500_000,
                    description="テスト自動化ツール導入支援（外注）",
                    expense_date=days_ago(81),
                ),
                Expense(
                    project_id=project_c1.id,
                    expense_type=ExpenseType.OTHER,
                    amount=50_000,
                    description="顧客先訪問交通費",
                    expense_date=days_ago(48),
                ),
            ]
        )
        db.add_all(
            [
                Notification(
                    user_id=sato.id,
                    project_id=project_c1.id,
                    title="案件が承認されました",
                    message=f"「{project_c1.name}」が承認されました",
                    is_read=True,
                ),
                Notification(
                    user_id=sato.id,
                    project_id=project_c1.id,
                    title="案件が開始されました",
                    message=f"「{project_c1.name}」が着手されました",
                    is_read=False,
                ),
                Notification(
                    user_id=saito.id,
                    project_id=project_c1.id,
                    title="案件にアサインされました",
                    message=f"「{project_c1.name}」にアサインされました",
                    is_read=False,
                ),
            ]
        )
        print(f"  案件を作成しました: {project_c1.name}")

        # ── 案件C2: XYZ物産（完了）──
        project_c2 = Project(
            name="XYZ物産 在庫管理フロー導入",
            description="XYZ物産の在庫管理業務にFlowBaseを導入。発注・入庫・出庫の承認フローを構築し、Excel管理からの脱却を支援する。",
            status=ProjectStatus.COMPLETED,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=sato.id,
            department_id=dept_cs.id,
            budget_amount=3_500_000,
            planned_months=4,
            start_date=days_ago(209),
            end_date=days_ago(86),
        )
        db.add(project_c2)
        db.flush()
        db.add(
            ProjectBudget(
                project_id=project_c2.id,
                budget_amount=3_500_000,
                unit_price=850_000,
                planned_months=4,
                actual_amount=3_200_000,
            )
        )
        db.add_all(
            [
                Task(
                    project_id=project_c2.id,
                    phase_name="要件定義",
                    name="現状業務分析・要件定義",
                    assignee_id=sato.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(209),
                    due_date=days_ago(178),
                ),
                Task(
                    project_id=project_c2.id,
                    phase_name="実装",
                    name="フロー設計・実装",
                    assignee_id=sato.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(177),
                    due_date=days_ago(133),
                ),
                Task(
                    project_id=project_c2.id,
                    phase_name="リリース",
                    name="ユーザー研修・運用サポート",
                    assignee_id=sato.id,
                    status=TaskStatus.DONE,
                    progress=100,
                    start_date=days_ago(132),
                    due_date=days_ago(86),
                ),
            ]
        )
        db.add(
            Notification(
                user_id=sato.id,
                project_id=project_c2.id,
                title="案件が完了しました",
                message=f"「{project_c2.name}」が完了しました",
                is_read=True,
            )
        )
        print(f"  案件を作成しました: {project_c2.name}")

        # ── 案件C3: DEF銀行（本部承認待ち）──
        project_c3 = Project(
            name="DEF銀行 稟議フロー刷新",
            description="DEF銀行の稟議承認フローをFlowBaseで刷新。承認階層の複雑化・監査ログ要件に対応したカスタマイズを実施する。",
            status=ProjectStatus.PENDING_HQ,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=sato.id,
            department_id=dept_cs.id,
            budget_amount=11_000_000,
            planned_months=10,
            start_date=days_later(34),
            end_date=days_later(337),
        )
        db.add(project_c3)
        db.flush()
        db.add(
            Notification(
                user_id=takahashi.id,
                project_id=project_c3.id,
                title="新規案件申請（最終承認依頼）",
                message=f"「{project_c3.name}」の最終承認依頼が届いています",
                is_read=False,
            )
        )
        print(f"  案件を作成しました: {project_c3.name}")

        # ── 案件C4: GHI製造（部門承認待ち）──
        project_c4 = Project(
            name="GHI製造 生産指示フロー導入",
            description="GHI製造の生産指示・変更承認フローをFlowBaseで構築。現場タブレットからの入力にも対応する。",
            status=ProjectStatus.PENDING_DEPT,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=sato.id,
            department_id=dept_cs.id,
            budget_amount=6_500_000,
            planned_months=7,
            start_date=days_later(64),
            end_date=days_later(277),
        )
        db.add(project_c4)
        db.flush()
        db.add(
            Notification(
                user_id=yamada.id,
                project_id=project_c4.id,
                title="新規案件申請",
                message=f"「{project_c4.name}」の承認依頼が届いています",
                is_read=False,
            )
        )
        print(f"  案件を作成しました: {project_c4.name}")

        # ── 案件C5: JKL商事（承認済）──
        project_c5 = Project(
            name="JKL商事 購買承認フロー改修",
            description="既存購買フローに予算照合・自動差戻し機能を追加。ERP連携APIの実装も含む。",
            status=ProjectStatus.APPROVED,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=sato.id,
            department_id=dept_cs.id,
            budget_amount=5_200_000,
            planned_months=5,
            start_date=days_later(3),
            end_date=days_later(155),
        )
        db.add(project_c5)
        db.flush()
        db.add(
            ProjectBudget(
                project_id=project_c5.id,
                budget_amount=5_200_000,
                unit_price=900_000,
                planned_months=5,
                actual_amount=0,
            )
        )
        db.add_all(
            [
                # 今日開始タスク（starting）
                Task(
                    project_id=project_c5.id,
                    phase_name="要件定義",
                    name="要件定義・ERP連携仕様確定",
                    assignee_id=sato.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=today(),
                    due_date=days_later(33),
                ),
                Task(
                    project_id=project_c5.id,
                    phase_name="実装",
                    name="フロー改修実装",
                    assignee_id=saito.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_later(34),
                    due_date=days_later(95),
                ),
                Task(
                    project_id=project_c5.id,
                    phase_name="テスト",
                    name="テスト・品質確認",
                    assignee_id=nakamura.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_later(96),
                    due_date=days_later(155),
                ),
                Task(
                    project_id=project_c5.id,
                    phase_name="実装",
                    name="ERP連携API実装・テスト",
                    assignee_id=sato.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_later(96),
                    due_date=days_later(155),
                ),
            ]
        )
        # 提出後の確認日が数日ずれても、CS部門のTASK_MEMBERで「今日期限」を確認できるデモ用タスク
        db.add_all(
            [
                Task(
                    project_id=project_c5.id,
                    phase_name="確認",
                    name=f"提出後確認用タスク（{offset}日後期限）",
                    assignee_id=saito.id if offset % 2 else nakamura.id,
                    status=TaskStatus.TODO,
                    progress=0,
                    start_date=days_offset(max(offset - 1, 0)),
                    due_date=days_offset(offset),
                )
                for offset in range(1, DEMO_WINDOW_DAYS + 1)
            ]
        )

        db.add(
            Notification(
                user_id=sato.id,
                project_id=project_c5.id,
                title="案件が承認されました",
                message=f"「{project_c5.name}」が承認されました",
                is_read=False,
            )
        )
        print(f"  案件を作成しました: {project_c5.name}")

        # ── 案件C6: MNO病院（却下）──
        project_c6 = Project(
            name="MNO病院 電子申請フロー構築",
            description="MNO病院の各種申請（休暇・備品購入・設備修繕）をFlowBaseで電子化。紙申請の撤廃を目指す。",
            status=ProjectStatus.REJECTED,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=sato.id,
            department_id=dept_cs.id,
            budget_amount=4_000_000,
            planned_months=4,
            start_date=days_ago(27),
            end_date=days_later(95),
            reject_reason="顧客側の予算確保が未確定のため、確定後に再申請すること。",
        )
        db.add(project_c6)
        db.flush()
        db.add(
            Notification(
                user_id=sato.id,
                project_id=project_c6.id,
                title="案件が却下されました",
                message=f"「{project_c6.name}」が却下されました",
                is_read=False,
            )
        )
        print(f"  案件を作成しました: {project_c6.name}")

        # ── 案件C7: PQR流通（ドラフト）──
        project_c7 = Project(
            name="PQR流通 配送管理フロー構築",
            description="PQR流通の配送指示・遅延報告フローをFlowBaseで構築。ドライバーのスマートフォンからの操作に対応する。",
            status=ProjectStatus.DRAFT,
            development_method=DevelopmentMethod.WATERFALL,
            applicant_id=sato.id,
            department_id=dept_cs.id,
            budget_amount=4_500_000,
            planned_months=5,
            start_date=days_later(95),
            end_date=days_later(247),
        )
        db.add(project_c7)
        db.flush()
        print(f"  案件を作成しました: {project_c7.name}（下書き）")

        db.commit()
        print("シードデータの投入が完了しました。")

    except Exception as e:
        db.rollback()
        print(f"エラーが発生しました: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
