# World of AICraft

Working repository for the World of AICraft mod experiments.

## Layout

- `mod-playable-races/` contains playable race database changes.
- `mod-remix/` contains remix-system source and database changes.
- `tools/` contains build and verification scripts used to generate client/database artifacts.
- `artifacts/` keeps lightweight generated SQL/install/image outputs in git. Large generated client assets such as MPQs, DBCs, models, textures, and staging folders are intentionally ignored locally.

Large generated files should be rebuilt from the checked-in tools or published separately with Git LFS/release artifacts if we decide they need long-term storage.
