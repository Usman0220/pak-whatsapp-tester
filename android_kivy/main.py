from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.clock import Clock

import threading
import builtins
import asyncio

# Local sample logic (safe subset) separated from the original network-heavy script
import sample_logic

# Import the full tester6 workflow (bundled with the APK)
import tester6


class Root(TabbedPanel):
    do_default_tab = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tab_height = "40dp"

        # Demo tab
        demo_tab = TabbedPanelItem(text="Demo")
        demo_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.result_label = Label(text="Press 'Generate' to run sample Python logic.",
                                  size_hint_y=None, height=120)
        generate_btn = Button(text="Generate number", size_hint_y=None, height=50)
        generate_btn.bind(on_release=self.on_generate)

        # Full workflow controls + log
        self.run_btn = Button(text="Run full network workflow", size_hint_y=None, height=50)
        self.run_btn.bind(on_release=self.on_run_full)

        self.log_label = Label(text="[log] idle", halign="left", valign="top",
                               size_hint_y=None, markup=True)
        self.log_label.bind(texture_size=self._update_log_height)

        log_scroll = ScrollView(do_scroll_x=True, do_scroll_y=True, size_hint_y=1)
        log_scroll.add_widget(self.log_label)

        demo_layout.add_widget(self.result_label)
        demo_layout.add_widget(generate_btn)
        demo_layout.add_widget(self.run_btn)
        demo_layout.add_widget(log_scroll)
        demo_tab.add_widget(demo_layout)
        self.add_widget(demo_tab)

        # Code tab - shows bundled tester6.py source
        code_tab = TabbedPanelItem(text="tester6.py")
        self.code_view = Label(text=self._load_tester6_source(),
                               halign="left", valign="top", text_size=(Window.width - 40, None))
        self.code_view.bind(texture_size=self._update_label_height)

        scroll = ScrollView(do_scroll_x=True, do_scroll_y=True)
        scroll.add_widget(self.code_view)
        code_tab.add_widget(scroll)
        self.add_widget(code_tab)

        self._is_running = False

    def _update_label_height(self, *_):
        # Expand label height to its texture to make ScrollView content size correct
        self.code_view.height = self.code_view.texture_size[1] + 20

    def _update_log_height(self, *_):
        self.log_label.text_size = (Window.width - 40, None)
        self.log_label.height = self.log_label.texture_size[1] + 20

    def _append_log(self, line):
        # Schedule UI update on the main thread
        def _do_update(dt):
            if self.log_label.text == "[log] idle":
                self.log_label.text = line
            else:
                self.log_label.text += "\n" + line
        Clock.schedule_once(_do_update, 0)

    def _load_tester6_source(self):
        # tester6.py is bundled alongside this main.py within the APK
        try:
            with open("tester6.py", "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            return f"Could not load tester6.py: {e}"

    def on_generate(self, *_):
        n = sample_logic.generate_number()
        msg = (
            f"Generated:\n"
            f" local = {n['local']}\n"
            f" waInt = {n['waInt']}\n"
            f" waLink = {n['waLink']}"
        )
        self.result_label.text = msg

    def on_run_full(self, *_):
        if self._is_running:
            return
        self._is_running = True
        self.run_btn.text = "Running..."
        self._append_log("[info] starting full workflow...")

        t = threading.Thread(target=self._run_full_thread, daemon=True)
        t.start()

    def _run_full_thread(self):
        # Monkeypatch print to stream into the Kivy log view
        original_print = builtins.print

        def patched_print(*args, **kwargs):
            msg = " ".join(str(a) for a in args)
            self._append_log(msg)
            original_print(*args, **kwargs)

        builtins.print = patched_print
        try:
            # Run the async main from tester6 in this worker thread
            asyncio.run(tester6.main())
        except Exception as e:
            self._append_log(f"[error] {e}")
        finally:
            builtins.print = original_print

            def _finish(dt):
                self._is_running = False
                self.run_btn.text = "Run full network workflow"
                self._append_log("[info] workflow finished.")

            Clock.schedule_once(_finish, 0)


class Tester6Apk(App):
    def build(self):
        self.title = "tester6 APK demo"
        return Root()


if __name__ == "__main__":
    Tester6Apk().run()