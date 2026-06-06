// formula.ts
import * as ort from "onnxruntime-node";
import sharp from "sharp";
import { readFileSync } from "fs";
import { resolve } from "path";
import { fileURLToPath } from "url";
import type { Formula } from "../../types/src/ast";

const __dirname = fileURLToPath(new URL(".", import.meta.url));
const MODEL_DIR = resolve(__dirname, "../models/pix2text_mfr");
const ONNX_DIR = resolve(MODEL_DIR, "onnx");

const IMG_SIZE = 384;
const MEAN = [0.5, 0.5, 0.5];
const STD = [0.5, 0.5, 0.5];

let encoder: ort.InferenceSession | null = null;
let decoder: ort.InferenceSession | null = null;
let idToToken: Map<number, string> | null = null;
let BOS_ID = 0;
let EOS_ID = 2;

async function load() {
  if (encoder) return;

  // Read special token IDs from generation_config.json
  const genCfg = JSON.parse(
    readFileSync(resolve(MODEL_DIR, "generation_config.json"), "utf-8"),
  );
  BOS_ID = genCfg.decoder_start_token_id ?? genCfg.bos_token_id ?? 0;
  EOS_ID = genCfg.eos_token_id ?? 2;

  // Build id→token map directly from tokenizer.json vocab
  const tokJson = JSON.parse(
    readFileSync(resolve(MODEL_DIR, "tokenizer.json"), "utf-8"),
  );
  const vocab: Record<string, number> = tokJson.model.vocab;
  idToToken = new Map(Object.entries(vocab).map(([tok, id]) => [id, tok]));

  [encoder, decoder] = await Promise.all([
    ort.InferenceSession.create(resolve(ONNX_DIR, "encoder_model.onnx"), {
      executionProviders: ["cpu"],
    }),
    ort.InferenceSession.create(resolve(ONNX_DIR, "decoder_model.onnx"), {
      executionProviders: ["cpu"],
    }),
  ]);
}

// ── Decode token IDs → LaTeX string ─────────────────────────────────────────
function decodeTokens(ids: number[]): string {
  return ids
    .map((id) => idToToken!.get(id) ?? "")
    .join("")
    .replace(/Ġ/g, " ") // RoBERTa BPE space marker (U+0120)
    .replace(/Ċ/g, "\n") // RoBERTa BPE newline marker (U+010A)
    .replace(/▁/g, " ") // SentencePiece space marker (U+2581)
    .trim();
}

// ── Image → float32 CHW tensor ────────────────────────────────────────────────
async function toTensor(buf: Buffer): Promise<ort.Tensor> {
  const { data } = await sharp(buf)
    .resize(IMG_SIZE, IMG_SIZE, {
      fit: "contain",
      background: { r: 255, g: 255, b: 255 },
    })
    .removeAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });

  const f32 = new Float32Array(3 * IMG_SIZE * IMG_SIZE);
  const area = IMG_SIZE * IMG_SIZE;
  for (let i = 0; i < area; i++) {
    f32[i] = (data[i * 3] / 255 - MEAN[0]) / STD[0];
    f32[i + area] = (data[i * 3 + 1] / 255 - MEAN[1]) / STD[1];
    f32[i + area * 2] = (data[i * 3 + 2] / 255 - MEAN[2]) / STD[2];
  }
  return new ort.Tensor("float32", f32, [1, 3, IMG_SIZE, IMG_SIZE]);
}

// ── Greedy decode loop ────────────────────────────────────────────────────────
async function greedyDecode(
  hiddenStates: ort.Tensor,
  maxLen = 300,
): Promise<number[]> {
  const ids: number[] = [BOS_ID];

  for (let step = 0; step < maxLen; step++) {
    const len = ids.length;
    const out = await decoder!.run({
      input_ids: new ort.Tensor("int64", BigInt64Array.from(ids.map(BigInt)), [
        1,
        len,
      ]),
      attention_mask: new ort.Tensor("int64", new BigInt64Array(len).fill(1n), [
        1,
        len,
      ]),
      encoder_hidden_states: hiddenStates,
    });

    const logits = out.logits.data as Float32Array;
    const vocabSz = out.logits.dims[2];
    const offset = (len - 1) * vocabSz;

    let best = -Infinity,
      next = 0;
    for (let v = 0; v < vocabSz; v++) {
      if (logits[offset + v] > best) {
        best = logits[offset + v];
        next = v;
      }
    }

    if (next === EOS_ID) break;
    ids.push(next);
  }

  return ids.slice(1); // drop BOS
}

export async function formulaToLatex(imgBuffer: Buffer): Promise<string> {
  await load();
  const pixelValues = await toTensor(imgBuffer);
  const encOut = await encoder!.run({ pixel_values: pixelValues });
  const tokenIds = await greedyDecode(encOut.last_hidden_state);
  return decodeTokens(tokenIds);
}

export async function recognizeFormula(imgBuffer: Buffer): Promise<string> {
  const d = await formulaToLatex(imgBuffer);
  return d;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const buf = readFileSync(resolve(__dirname, "./formula.png"));
  const node = await recognizeFormula(buf);
  console.log("LaTeX :", node);
  console.log("Node  :", JSON.stringify(node, null, 2));
}
