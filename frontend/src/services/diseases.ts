import { apiGet } from "./api";
import type { Disease } from "../types/disease";

export function fetchDiseases(): Promise<Disease[]> {
  return apiGet<Disease[]>("/diseases");
}
