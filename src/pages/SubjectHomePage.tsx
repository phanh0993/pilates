import { Link } from "react-router-dom";

export const SubjectHomePage = () => (
  <div className="mx-auto max-w-3xl px-4 py-8">
    <div className="rounded-3xl bg-gradient-to-br from-violet-600 to-indigo-700 p-8 text-white shadow-lg">
      <h1 className="text-3xl font-black tracking-tight">Trắc nghiệm cho Vợ Ánh</h1>
      <p className="mt-2 text-violet-100">Chọn môn học để bắt đầu.</p>
    </div>

    <div className="mt-8 grid gap-4 sm:grid-cols-2">
      <Link
        to="/pilates"
        className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-violet-300 hover:shadow-md"
      >
        <p className="text-2xl">🧘</p>
        <h2 className="mt-2 text-xl font-bold text-slate-900">Pilates</h2>
        <p className="mt-1 text-sm text-slate-500">
          Học tên động tác, nghe phát âm, xem hình các bước.
        </p>
      </Link>

      <Link
        to="/anatomy"
        className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-teal-300 hover:shadow-md"
      >
        <p className="text-2xl">🫀</p>
        <h2 className="mt-2 text-xl font-bold text-slate-900">Giải phẫu</h2>
        <p className="mt-1 text-sm text-slate-500">
          Thuộc khái niệm theo chương — trắc nghiệm & điền thuật ngữ.
        </p>
      </Link>
    </div>

    <p className="mt-6 text-center text-xs text-slate-400">
      <Link to="/admin/anatomy" className="underline hover:text-slate-600">
        Tool import & gán nhãn sơ đồ
      </Link>
    </p>
  </div>
);
