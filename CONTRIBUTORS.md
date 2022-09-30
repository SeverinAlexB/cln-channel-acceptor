# Contributors

## Release new version

1. Bump version in `__version__.py` in `x.x.x` format.
2. Commit git with message `Bump version to vx.x.x`.
3. Tag commit with
```bash
git tag v0.0.1
git push origin v0.0.1
```
4. Create release with `./create_release.sh`.
5. Upload files in `release` to Github.