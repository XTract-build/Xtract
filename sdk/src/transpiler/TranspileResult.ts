export interface Diagnostic {
  severity: 'error' | 'warning' | 'info';
  message: string;
  line?: number;
}

export interface TranspileResult {
  success: boolean;
  rustCode: string;
  diagnostics: Diagnostic[];
}
