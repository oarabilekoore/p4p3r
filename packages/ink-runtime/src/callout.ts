import * as tf from "@tensorflow/tfjs";
import "@tensorflow/tfjs-backend-cpu";
import sharp from "sharp";
import { pathToFileURL } from "url";
import { resolve } from "path";

type Detection = { prediction: string, confidence: number }
async function detectCalloutShape(imagePath: string): Promise<Detection> {
  const labels = ["circle", "triangle", "rectangle", "square"];
  const modelPath = pathToFileURL(resolve("../models/tfjs_model/model.json")).href;

  await tf.setBackend("cpu");
  await tf.ready();

  const model = await tf.loadGraphModel(modelPath);

  const { data, info } = await sharp(imagePath)
    .resize(28, 28)
    .raw()
    .toBuffer({ resolveWithObject: true });

  const tensor = tf.tensor3d(new Uint8Array(data), [28, 28, info.channels])
    .toFloat()
    .expandDims();

  const prediction = model.predict(tensor) as tf.Tensor;
  const scores = await prediction.data();
  const maxIndex = [...scores].indexOf(Math.max(...scores));

  tf.dispose([tensor, prediction]);
  return {
    prediction: labels[maxIndex],
    confidence: scores[maxIndex]
  } as Detection
}

detectCalloutShape("testimage.jpg");
