import { ValidationFlag } from "../types";

const ICON_MAP: Record<ValidationFlag, string> = {
  OK: "✔️",
  AVISO: "⚠️",
  ERRO: "⛔",
};

interface Props {
  value: ValidationFlag;
}

function ValidationIcon({ value }: Props) {
  return <span className={`validation-flag validation-${value.toLowerCase()}`}>{ICON_MAP[value]} {value}</span>;
}

export default ValidationIcon;
