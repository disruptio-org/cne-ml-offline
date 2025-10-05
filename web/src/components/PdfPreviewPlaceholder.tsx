interface Props {
  jobId: string;
  fileName?: string;
}

function PdfPreviewPlaceholder({ jobId, fileName }: Props) {
  return (
    <div
      style={{
        border: "1px solid #d1d5db",
        borderRadius: "12px",
        padding: "24px",
        minHeight: "320px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        color: "#6b7280",
        background: "#f8fafc",
      }}
    >
      <span style={{ fontSize: "64px", marginBottom: "16px" }}>📄</span>
      <strong>Pré-visualização PDF</strong>
      <span style={{ marginTop: "8px" }}>Job {jobId}</span>
      {fileName && <span style={{ marginTop: "4px" }}>{fileName}</span>}
      <p style={{ maxWidth: "320px", textAlign: "center", marginTop: "12px" }}>
        Integração com pdf.js será adicionada posteriormente. Para já, esta área serve como placeholder visual.
      </p>
    </div>
  );
}

export default PdfPreviewPlaceholder;
