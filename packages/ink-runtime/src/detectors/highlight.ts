import Jimp from "jimp"
import { Style } from "../../../types/src/ast";

export type StyleSpan = { startChar: number; endChar: number; style: Style }

// the function retuens pixel x-ranges where a highlight color was detected
export async function detecthighlight(buffer: Buffer): Promise<{ xStart: number; xEnd: number; color: string }[]> {
  const image = await Jimp.read(buffer);
  const spans: { xStart: number; xEnd: number; color: string }[] = [];


}
