import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  createEmptyPlan,
  createSampleWarmupPlan,
  deletePlan,
  loadPlans,
  upsertPlan,
} from "../lib/lessonPlan";
import type { LessonPlan } from "../types/lessonPlan";

const formatDate = (iso: string) =>
  new Date(iso).toLocaleString("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

export const LessonPlanHomePage = () => {
  const navigate = useNavigate();
  const [plans, setPlans] = useState<LessonPlan[]>([]);

  useEffect(() => {
    setPlans(loadPlans());
  }, []);

  const handleCreate = () => {
    const plan = upsertPlan(createEmptyPlan());
    navigate(`/lesson-plans/${plan.id}`);
  };

  const handleSample = () => {
    const plan = upsertPlan(createSampleWarmupPlan());
    setPlans(loadPlans());
    navigate(`/lesson-plans/${plan.id}`);
  };

  const handleDelete = (id: string, title: string) => {
    if (!window.confirm(`Xóa giáo án “${title}”?`)) return;
    deletePlan(id);
    setPlans(loadPlans());
  };

  const handleDuplicate = (plan: LessonPlan) => {
    const copy = upsertPlan({
      ...structuredClone(plan),
      id: `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`,
      title: `${plan.title} (bản sao)`,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    });
    setPlans(loadPlans());
    navigate(`/lesson-plans/${copy.id}`);
  };

  return (
    <div className="mx-auto min-h-screen max-w-3xl px-3 pb-8 pt-4 sm:px-4 sm:py-6">
      <Link
        to="/"
        className="inline-flex min-h-10 items-center text-sm font-medium text-emerald-700"
      >
        ← Trang chủ
      </Link>

      <div className="mt-3 rounded-3xl bg-gradient-to-br from-emerald-700 to-teal-800 p-5 text-white shadow-lg sm:p-7">
        <h1 className="text-2xl font-black tracking-tight sm:text-3xl">Giáo án</h1>
        <p className="mt-2 text-sm leading-relaxed text-emerald-100 sm:text-base">
          Soạn trên điện thoại, xuất PDF A4 để in.
        </p>
      </div>

      <div className="mt-4 grid gap-2 sm:grid-cols-2">
        <button
          type="button"
          onClick={handleCreate}
          className="min-h-12 rounded-2xl bg-emerald-700 px-4 text-base font-semibold text-white active:bg-emerald-800"
        >
          + Giáo án trống
        </button>
        <button
          type="button"
          onClick={handleSample}
          className="min-h-12 rounded-2xl border border-emerald-200 bg-white px-4 text-base font-semibold text-emerald-800 active:bg-emerald-50"
        >
          Mẫu Khởi động
        </button>
      </div>

      {plans.length === 0 ? (
        <p className="mt-10 px-2 text-center text-sm leading-relaxed text-slate-500">
          Chưa có giáo án. Bấm nút phía trên để tạo mới hoặc lấy mẫu.
        </p>
      ) : (
        <ul className="mt-5 space-y-3">
          {plans.map((plan) => (
            <li
              key={plan.id}
              className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
            >
              <Link
                to={`/lesson-plans/${plan.id}`}
                className="block px-4 py-4 active:bg-slate-50"
              >
                <h2 className="text-lg font-bold leading-snug text-slate-900">
                  {plan.title || "Không tiêu đề"}
                </h2>
                {plan.subtitle ? (
                  <p className="mt-0.5 text-sm text-slate-500">{plan.subtitle}</p>
                ) : null}
                <p className="mt-1 text-xs text-slate-400">
                  {plan.sections.length} phần · {formatDate(plan.updatedAt)}
                </p>
              </Link>
              <div className="grid grid-cols-3 border-t border-slate-100">
                <Link
                  to={`/lesson-plans/${plan.id}`}
                  className="flex min-h-12 items-center justify-center text-sm font-semibold text-emerald-700 active:bg-emerald-50"
                >
                  Sửa
                </Link>
                <button
                  type="button"
                  onClick={() => handleDuplicate(plan)}
                  className="flex min-h-12 items-center justify-center border-x border-slate-100 text-sm font-medium text-slate-700 active:bg-slate-50"
                >
                  Sao chép
                </button>
                <button
                  type="button"
                  onClick={() => handleDelete(plan.id, plan.title)}
                  className="flex min-h-12 items-center justify-center text-sm font-medium text-rose-600 active:bg-rose-50"
                >
                  Xóa
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
