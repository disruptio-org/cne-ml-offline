import { PropsWithChildren, useCallback, useRef, useState } from "react";

interface Props {
  onFiles: (files: FileList | File[]) => void;
}

function UploadDropzone({ onFiles, children }: PropsWithChildren<Props>) {
  const [isDragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFiles = useCallback(
    (fileList: FileList | File[]) => {
      const files = Array.isArray(fileList) ? fileList : Array.from(fileList ?? []);
      if (files.length > 0) {
        onFiles(files);
      }
    },
    [onFiles]
  );

  const onDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setDragging(false);
      if (event.dataTransfer.files) {
        handleFiles(event.dataTransfer.files);
      }
    },
    [handleFiles]
  );

  const openFileDialog = useCallback(() => {
    inputRef.current?.click();
  }, []);

  return (
    <div
      className={`upload-area ${isDragging ? "dragging" : ""}`}
      onDragOver={(event) => {
        event.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={onDrop}
      onClick={openFileDialog}
    >
      <input
        ref={inputRef}
        type="file"
        hidden
        onChange={(event) => {
          if (event.target.files) {
            handleFiles(event.target.files);
            event.target.value = "";
          }
        }}
      />
      {children}
    </div>
  );
}

export default UploadDropzone;
