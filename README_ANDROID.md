Android APK for tester6.py

What this adds
- android_kivy/: a Kivy app that:
  - Bundles the original tester6.py inside the APK (visible under the “tester6.py” tab)
  - Provides a “Demo” tab with:
    - Safe, local Python logic (no network) to demonstrate functionality
    - A “Run full network workflow” button that executes tester6.main() and streams logs into the app
- buildozer.spec: ready-to-build spec using Kivy/Buildozer with full network dependencies enabled
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
- Full network workflow enabled:
  - buildozer.spec includes: python3,kivy,aiohttp,openssl,certifi,yarl,multidict,async-timeout,aiosignal,frozenlist,attrs,setuptools
  - INTERNET permission is declared
  - tester6 saves images to app-private storage (profile_images/), so no external storage permission is required
- If you encounter SSL or dependency issues on certain Android versions/CPUs, try:
  - Clearing buildozer .buildozer cache and rebuilding
  - Updating android.api to match your SDK
  - Removing arm64 or armv7 temporarily to isolate arch-specific issues

GitHub Actions (optional)
You can enable CI builds with the provided workflow:
- Commit and push to your repository (with android_kivy/ present)
- Enable Actions in your repo
- On push to main, the workflow will build the APK and upload it as an artifact