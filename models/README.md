# Ink-Runtime Model Dependencies 

This folder contains multiple models that the ink-runtime needs in order 
to perfom multiple element separation functions to build the Ink-AST defined at `docs/ASTScheme.md` .

Below are all sources of these models: 

## Paper.Md Scanner Layout Detection 

This model is the custom layout detection for handwritten notes 
that the entire project depends on. You may refer to the `training` directory for more models, model related training code. 

## Shape Detecttion for Callouts

Sourced from: [https://github.com/Shahir-Abdullah/Handwritten-Geometric-Shape-Detector](Shahir Abdullah)

Refer to `callout.ts` and the `ShapeDetectorConverter.
ipynb` file. Furthermore to the `tfjs_model` dir.

## Pix2Text_Mfr
