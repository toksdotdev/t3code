"""Apply isolation to the pinned redesign source; fail if upstream anchors drift."""
from pathlib import Path
import json


def replace(path, old, new, count=1):
    file = Path(path)
    source = file.read_text()
    assert source.count(old) == count, f"Unexpected source in {path}: {old!r}"
    file.write_text(source.replace(old, new))


replace('scripts/build-desktop-artifact.ts', 'const DESKTOP_APP_ID = "com.t3tools.t3code";',
        'const DESKTOP_APP_ID = "dev.toks.t3-redesign";')
replace('scripts/build-desktop-artifact.ts', 'artifactName: "T3-Code-${version}-${arch}.${ext}"',
        'artifactName: "T3-Redesign-${version}-${arch}.${ext}"')
# Keep the internal app origin, but never register this app for the standard OS URL schemes.
replace('scripts/build-desktop-artifact.ts', '''      protocols: [
        {
          name: "T3 Code",
          schemes: ["t3code", "t3code-dev"],
        },
        {
          name: "Web site URL",
          schemes: ["http", "https"],
          role: "Viewer",
        },
      ],''', '      protocols: [],')
file = Path('apps/desktop/package.json')
package = json.loads(file.read_text())
package['productName'] = 'T3 Redesign'
file.write_text(json.dumps(package, indent=2) + '\n')
replace('apps/desktop/src/app/DesktopStatePaths.ts', 'input.homeDirectory, ".t3"',
        'input.homeDirectory, ".t3-redesign"')
replace('apps/desktop/src/app/DesktopConfig.ts', 't3Home: trimmedString("T3CODE_HOME")',
        't3Home: trimmedString("T3CODE_REDESIGN_HOME")')
replace('apps/desktop/src/app/DesktopConfig.ts',
        'disableAutoUpdate: optionalBoolean("T3CODE_DISABLE_AUTO_UPDATE")',
        'disableAutoUpdate: Config.succeed(true)')
replace('apps/desktop/src/app/DesktopUserData.ts',
        '{ current: "t3code-v2", legacy: "T3 Code (Alpha)" }',
        '{ current: "t3code-redesign", legacy: "T3 Redesign (Legacy)" }')
replace('apps/desktop/src/app/DesktopLegacyLocalStorage.ts',
        'const V1_PROFILE_NAMES = ["T3 Code (Alpha)", "t3code"];',
        'const V1_PROFILE_NAMES: string[] = [];')
replace('apps/desktop/src/app/DesktopEnvironment.ts',
        'displayName: `${APP_BASE_NAME} (${stageLabel})`,',
        'displayName: "T3 Redesign",')
replace('scripts/smoke-desktop-app.ts', 'T3CODE_HOME: t3Home,',
        'T3CODE_HOME: t3Home,\n      T3CODE_REDESIGN_HOME: t3Home,')
print('Prepared isolated T3 Redesign build.')
