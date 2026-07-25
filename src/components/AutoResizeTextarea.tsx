import { useEffect, useRef } from "react";

type AutoResizeTextareaProps = {
  value: string;
  onChange: (value: string) => void;
  minRows?: number;
  className?: string;
  "aria-label"?: string;
  placeholder?: string;
  /** Class cho bản in (div), mặc định padding giống ô bảng */
  printClassName?: string;
};

const LINE_PX = 24;

const fitHeight = (el: HTMLTextAreaElement, minRows: number) => {
  const minHeight = minRows * LINE_PX;
  el.style.height = "0px";
  el.style.height = `${Math.max(el.scrollHeight, minHeight)}px`;
};

export const AutoResizeTextarea = ({
  value,
  onChange,
  minRows = 3,
  className = "",
  "aria-label": ariaLabel,
  placeholder,
  printClassName = "px-2 py-2 text-[10pt] leading-snug text-slate-800",
}: AutoResizeTextareaProps) => {
  const ref = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    fitHeight(el, minRows);
  }, [value, minRows]);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const handleResize = () => fitHeight(el, minRows);
    window.addEventListener("resize", handleResize);

    const parent = el.parentElement;
    let observer: ResizeObserver | undefined;
    if (parent && typeof ResizeObserver !== "undefined") {
      observer = new ResizeObserver(handleResize);
      observer.observe(parent);
    }

    return () => {
      window.removeEventListener("resize", handleResize);
      observer?.disconnect();
    };
  }, [minRows]);

  return (
    <>
      <textarea
        ref={ref}
        value={value}
        rows={minRows}
        aria-label={ariaLabel}
        placeholder={placeholder}
        onChange={(e) => {
          const el = e.currentTarget;
          onChange(el.value);
          fitHeight(el, minRows);
        }}
        className={`box-border overflow-hidden print:hidden ${className}`}
      />
      {/* Bản in: div hiển thị đủ chữ (textarea bị trình duyệt cắt khi print) */}
      <div
        aria-hidden="true"
        className={`hidden whitespace-pre-wrap break-words print:block ${printClassName}`}
      >
        {value || "\u00A0"}
      </div>
    </>
  );
};
