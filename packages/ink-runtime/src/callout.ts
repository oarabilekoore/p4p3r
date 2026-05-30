import * as tf from "@tensorflow/tfjs";
import "@tensorflow/tfjs-backend-cpu"; // Safe for non-AVX processors
import { PNG } from "pngjs";
import { pathToFileURL } from "url";
import { resolve } from "path";

type Detection = { prediction: string; confidence: number };

async function detectCalloutShape(imagePath: string): Promise<Detection> {
  const labels = ["circle", "triangle", "rectangle", "square"];
  const modelPath = pathToFileURL(
    resolve("../models/tfjs_model/model.json"),
  ).href;

  await tf.setBackend("cpu");
  await tf.ready();

  const model = await tf.loadGraphModel(modelPath);

  // 1. Resize using Bun's native image API and export to a PNG ArrayBuffer
  const imageBuffer = await Bun.file(imagePath)
    .image()
    .resize(28, 28)
    .png()
    .buffer();

  // 2. Decode the encoded PNG buffer into raw RGBA pixels using pngjs
  const png = PNG.sync.read(Buffer.from(imageBuffer));

  // 3. Construct the tensor from the flat array of RGBA pixels
  const tensor = tf
    .tensor3d(new Uint8Array(png.data), [28, 28, 4])
    .slice([0, 0, 0], [-1, -1, 3]) // Drop the alpha channel to get standard RGB
    .toFloat()
    .expandDims();

  const prediction = model.predict(tensor) as tf.Tensor;
  const scores = await prediction.data();
  const maxIndex = [...scores].indexOf(Math.max(...scores));

  tf.dispose([tensor, prediction]);

  return {
    prediction: labels[maxIndex],
    confidence: scores[maxIndex],
  } as Detection;
}

detectCalloutShape("testimage.jpg").then(console.log);
