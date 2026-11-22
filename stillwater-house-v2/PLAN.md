# Stillwater House II

Completion: preserve V1; deliver an independently rebuildable, editable V2 Blender scene, early draft, and three inspected full-resolution renders.

## Feature playbook / architectural ownership
- Acceptance: clearly taller and larger residence, sophisticated asymmetrical massing, expanded garden with swimming, dining, lounging, planted leisure spaces.
- Core data: Blender scene collections in meters. base_scene.py preserves original furniture and material vocabulary. build_scene.py owns V2 massing and cameras. garden_extension.py owns new exterior leisure garden.
- Early vertical slice: build whole massing and garden, render 1000 px exterior and inspect before final 2600 px render.
- Architecture exploration: scaling V1 would also overscale furniture and create a larger pavilion without stronger architecture. Chosen: preserve the crafted living interior, add a stepped two-storey east wing, a taller glazed stair/atelier tower and expansive connected terraces.
- Verification: generator runtime, actual draft and final image inspection, fresh-process saved-scene open, external dependency and light visibility checks, hashes.
- TDD/interrogate skipped: visual concept acceptance is proven on renders, not unit-test assertions. Geometry checks supplement visual inspection.

## Workflow
1. Inspect and copy original source without changing V1.
2. Build distinct architecture and garden modules.
3. Real CPU draft render, correct framing and materials.
4. Render full-resolution exterior, intimate garden view and upper terrace/stair view.
5. Reopen, verify, package source/render/blend.

## Verified checkpoints
- V1 copied and unchanged hash recorded.
- Direct mesh primitives replaced operator-heavy cube/sphere/cylinder construction after the initial build proved too slow.
- 1196 × 782 exterior proof inspected; residence and expanded garden compose coherently.
- Secondary poolside camera moved out of an olive canopy after rendered proof exposed foreground leaf obstruction.
- Official Blender 4.5.3 distribution verified against upstream SHA-256.
- Fresh-process reopen passed: 2,147 objects, 68 materials, three cameras, no external images or linked libraries.

## Principles that changed the outcome
Experience first: composition was settled with real proofs before final rendering. Fix root causes: direct mesh creation removed repeated scene graph updates rather than lowering scene detail. Prove it works: the saved file was reopened and images visually reviewed. Separate shared state: V2 lives independently and V1 is unchanged.
