Android APK for tester6.py

What this adds
- android_kivy/: a minimal Kivy app that:
  - Bundles the original tester6.py inside the APK (visible under the “tester6.py” tab)
  - Provides a simple “Demo” tab that runs safe, local Python logic (no network) to demonstrate functionality
- buildozer.spec: ready-to-build spec using Kivy/Buildozer
- Optional CI (GitHub Actions) provided below to build an APK automatically using Docker

Local build (recommended)
Prereqs (macOS/Linux):
- Python 3.10+
- Java JDK 8+ (OpenJDK works)
- Git
- Docker (recommended) or full Android SDK/NDK if not using Docker
- Buildozer: pip install buildozer

Steps:
1) cd android_kivy
2) If using Docker (simplest):
   - buildozer android debug
   - Output APK will be at bin/tester6demo-0.1.0-armeabi-v7a-debug.apk and/or arm64 builds
3) If not using Docker, install SDK/NDK per Buildozer docs and run:
   - buildozer android debug

Install on device:
- Enable “Install from unknown sources” on your Android device
- Transfer the generated APK from android_kivy/bin/ to the device and install

Notes
- The original tester6.py contains heavy network dependencies (aiohttp/asyncio and SSL). To keep the APK build simple and reliable, the app:
  - Bundles tester6.py as-is so its source is present in the APK
  - Demonstrates a safe subset of the logic (number generation) via android_kivy/sample_logic.py
- If you want to run the full network workflow from tester6.py on Android, the build requirements must include aiohttp and its dependencies, and you may need to adjust SSL, permissions, and timeouts. This is not enabled by default here for reliability.

GitHub Actions (optional)
You can enable CI builds with the provided workflow:
- Commit and push to your repository (with android_kivy/ present)
- Enable Actions in your repo
- On push to main, the workflow will build the APK and upload it as an artifact