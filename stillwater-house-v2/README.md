# STILLWATER HOUSE II

A larger, taller continuation of Stillwater House. The original limestone, oak and bronze palette now carries a stepped two-storey residence, a third-level glazed atelier, and a generous leisure garden.

## The expanded design

- A residence roughly 23 meters wide, rising to approximately 10.9 meters at the atelier canopy.
- A furnished upper salon and bedroom, shaded wraparound terrace, glazed balustrades and operable-style timber screens.
- A tall glazed stair lantern with modeled stair treads, landings, handrails and a furnished writing atelier.
- An additional ground-floor wellness and reading pavilion.
- A 14-meter swimming pool, separate spa and layered limestone terraces.
- An outdoor kitchen and six-seat dining pavilion beneath oak louvers.
- A sunken fireside lounge, open lawn, olive trees, cypresses and flowering borders.
- Integrated rooftop solar panels, concealed downlights and restrained landscape lighting.

## Open the editable model

Open **Stillwater-House-II.blend** in Blender 4.5 LTS or newer. Objects are named and grouped in purpose-specific collections. Units are meters. The scene has no external textures, linked libraries or required add-ons.

This is an architectural concept visualization, not construction documentation or an engineering-approved design. The building services, structure, access and safety details have not been professionally resolved.

## Rendered views

1. **Expanded Residence**: the whole residence and leisure garden, 2600 × 1700.
2. **Poolside Architecture**: a lower view across the water toward the glazed residence, 2400 × 1600.
3. **Garden Leisure**: the opposite garden view, 2600 × 1700.

PNG files are in `renders/`. The `-draft` versions are early composition proofs, not the final photographs.

## Rebuild and render

```bash
blender -b --threads 8 --python build_scene.py -- --output . --mode build
blender -b --threads 8 --python render_scene.py -- --output . --samples 160
blender -b --python verify_scene.py -- .
```

For a small preview, add `--preview --shot 1` to the render command. `--shot 2` or `--shot 3` selects the other view. CPU rendering is the default; `--gpu` opts into OptiX when available.

`base_scene.py` preserves the original interior and material vocabulary. `geometry.py` uses direct mesh construction to avoid repeated dependency-graph updates. `build_scene.py` owns the architectural expansion, lighting and cameras. `garden_extension.py` and `backdrop.py` own the landscape.

The optional `stillwater_ii_notebook.py` provides a local marimo gallery. Keep it beside the scene and `renders/` folder.

## Verification and preservation

The final scene was generated and rendered with the official Blender 4.5.3 LTS release. Its downloaded distribution was checked against Blender's published SHA-256 checksum. Every final image was visually inspected. `scene-manifest.json`, render receipts, `validation.json` and `SHA256SUMS` record the delivered artifacts.

Stillwater House V1 is preserved separately and was not modified.
