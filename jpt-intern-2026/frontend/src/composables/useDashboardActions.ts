import { useRouter } from "vue-router";

export function useDashboardActions() {
  const router = useRouter();

  /**
   * 通常画面遷移
   */
  const movePage = async (path: string) => {
    await router.push(path);
  };

  /**
   * 案件詳細へ遷移
   */
  const moveProjectDetail = async (projectId: number) => {
    await router.push(`/projects/${projectId}`);
  };

  /**
   * 担当者：進行中案件一覧
   */
  const moveProjectList = async () => {
    await router.push("/projects?status=APPROVED,IN_PROGRESS");
  };

  /**
   * 申請者：自分の申請案件一覧
   */
  const moveApplicantList = async (filter: string) => {
    const pathMap: Record<string, string> = {
      pending: "/projects?status=PENDING_DEPT,PENDING_HQ",
      draft: "/projects?status=DRAFT",
      rejected: "/projects?status=REJECTED",
      risk: "/projects?alertLevel=danger,warning",
      budget: "/budget",
    };

    await router.push(pathMap[filter] ?? "/projects");
  };

  /**
   * 新規タブで開く
   */
  const openInNewTab = (path: string) => {
    window.open(path, "_blank", "noopener,noreferrer");
  };

  /**
   * 承認待ち案件一覧
   */
  const moveApprovalPage = async () => {
    await router.push("/projects?status=PENDING_DEPT,PENDING_HQ");
  };

  /**
   * 完了案件一覧
   */
  const moveCompletedPage = async () => {
    await router.push("/projects?status=COMPLETED");
  };

  return {
    movePage,
    moveProjectDetail,
    moveProjectList,
    moveApplicantList,
    moveApprovalPage,
    moveCompletedPage,
    openInNewTab,
  };
}
