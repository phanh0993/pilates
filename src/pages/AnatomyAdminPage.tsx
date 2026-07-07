import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import type { AnatomyConcept, AnatomyDiagram, DiagramHotspot } from "../types/anatomy";

type AnatomyAdminPageProps = {
  concepts: AnatomyConcept[];
};

export const AnatomyAdminPage = ({ concepts }: AnatomyAdminPageProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [imageUrl, setImageUrl] = useState("");
  const [diagramName, setDiagramName] = useState("Sơ đồ mới");
  const [hotspots, setHotspots] = useState<DiagramHotspot[]>([]);
  const [nextNumber, setNextNumber] = useState(1);
  const [selectedConceptId, setSelectedConceptId] = useState(concepts[0]?.id ?? "");

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setImageUrl(URL.createObjectURL(file));
    setHotspots([]);
    setNextNumber(1);
  };

  const handleImageClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (!imageUrl || !selectedConceptId || !containerRef.current) return;

    const rect = containerRef.current.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;

    const hotspot: DiagramHotspot = {
      id: `h${nextNumber}`,
      number: nextNumber,
      x: Math.round(x * 10) / 10,
      y: Math.round(y * 10) / 10,
      conceptId: selectedConceptId,
    };

    setHotspots((prev) => [...prev, hotspot]);
    setNextNumber((n) => n + 1);
  };

  const handleRemoveHotspot = (id: string) => {
    setHotspots((prev) => prev.filter((h) => h.id !== id));
  };

  const handleExportDiagram = () => {
    const diagram: AnatomyDiagram = {
      id: diagramName.toLowerCase().replace(/\s+/g, "-"),
      name: diagramName,
      packId: "emma-anatomy-1",
      imageUrl: "/images/anatomy/your-upload.jpg",
      hotspots,
    };

    const blob = new Blob([JSON.stringify([diagram], null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "diagram-export.json";
    anchor.click();
    URL.revokeObjectURL(url);
  };

  const handleExportConceptsTemplate = () => {
    const template = concepts.map(({ id, term, termVi, definition, category, packId }) => ({
      id,
      term,
      termVi,
      definition,
      category,
      packId,
    }));
    const blob = new Blob([JSON.stringify(template, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "concepts-template.json";
    anchor.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <Link to="/" className="text-sm text-slate-600 hover:underline">
        ← Trang chủ
      </Link>

      <h1 className="mt-4 text-2xl font-bold text-slate-900">Tool import Giải phẫu</h1>
      <p className="mt-2 text-sm text-slate-600">
        Bước 1: Chạy script OCR trên folder ảnh. Bước 2: Upload sơ đồ, bấm vào vị trí để gán
        số và thuật ngữ. Bước 3: Export JSON và copy vào{" "}
        <code className="rounded bg-slate-100 px-1">public/data/anatomy/</code>.
      </p>

      <div className="mt-6 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm">
        <p className="font-semibold text-slate-800">Import ảnh bằng terminal:</p>
        <pre className="mt-2 overflow-x-auto rounded-lg bg-slate-900 p-3 text-xs text-emerald-300">
          {`python3 scripts/import_anatomy_photos.py \\
  --input ~/Downloads/anatomy-pages \\
  --output public/data/anatomy/import-draft.json`}
        </pre>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Upload ảnh sơ đồ</span>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="mt-1 block w-full text-sm"
          />
        </label>
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Tên sơ đồ</span>
          <input
            type="text"
            value={diagramName}
            onChange={(e) => setDiagramName(e.target.value)}
            className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2"
          />
        </label>
        <label className="block sm:col-span-2">
          <span className="text-sm font-medium text-slate-700">
            Thuật ngữ cho điểm tiếp theo (#{nextNumber})
          </span>
          <select
            value={selectedConceptId}
            onChange={(e) => setSelectedConceptId(e.target.value)}
            className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2"
          >
            {concepts.map((c) => (
              <option key={c.id} value={c.id}>
                {c.term} — {c.termVi}
              </option>
            ))}
          </select>
        </label>
      </div>

      {imageUrl && (
        <div
          ref={containerRef}
          className="relative mt-6 cursor-crosshair overflow-hidden rounded-2xl border-2 border-dashed border-teal-300 bg-white"
          onClick={handleImageClick}
          onKeyDown={() => undefined}
          role="button"
          tabIndex={0}
          aria-label="Bấm để đặt điểm trên sơ đồ"
        >
          <img src={imageUrl} alt="Sơ đồ đang gán nhãn" className="w-full select-none" />
          {hotspots.map((hotspot) => (
            <span
              key={hotspot.id}
              className="absolute flex h-7 w-7 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-teal-600 text-xs font-bold text-white shadow"
              style={{ left: `${hotspot.x}%`, top: `${hotspot.y}%` }}
            >
              {hotspot.number}
            </span>
          ))}
        </div>
      )}

      {hotspots.length > 0 && (
        <ul className="mt-4 space-y-2">
          {hotspots.map((hotspot) => {
            const concept = concepts.find((c) => c.id === hotspot.conceptId);
            return (
              <li
                key={hotspot.id}
                className="flex items-center justify-between rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm"
              >
                <span>
                  #{hotspot.number} ({hotspot.x}%, {hotspot.y}%) → {concept?.term}
                </span>
                <button
                  type="button"
                  onClick={() => handleRemoveHotspot(hotspot.id)}
                  className="text-rose-600 hover:underline"
                >
                  Xóa
                </button>
              </li>
            );
          })}
        </ul>
      )}

      <div className="mt-6 flex flex-wrap gap-3">
        <button
          type="button"
          onClick={handleExportDiagram}
          disabled={hotspots.length === 0}
          className="rounded-xl bg-teal-600 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-500 disabled:bg-slate-300"
        >
          Export diagrams.json
        </button>
        <button
          type="button"
          onClick={handleExportConceptsTemplate}
          className="rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
        >
          Tải mẫu concepts.json
        </button>
      </div>
    </div>
  );
};
