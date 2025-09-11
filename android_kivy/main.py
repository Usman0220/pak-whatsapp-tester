from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window

# Local sample logic (safe subset) separated from the original network-heavy script
import sample_logic


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

        demo_layout.add_widget(self.result_label)
        demo_layout.add_widget(generate_btn)
        demo_tab.add_widget(demo_layout)
        self.add_widget(demo_tab)

        # Code tab - shows bundled tester6.py source
        code_tab = TabbedPanelItem(text="tester6.py")
        code_layout = BoxLayout(orientation="vertical")
        self.code_view = Label(text=self._load_tester6_source(),
                               halign="left", valign="top", text_size=(Window.width - 40, None))
        self.code_view.bind(texture_size=self._update_label_height)

        scroll = ScrollView(do_scroll_x=True, do_scroll_y=True)
        scroll.add_widget(self.code_view)
        code_layout.add_widget(scroll)
        code_tab.add_widget(scroll)
        self.add_widget(code_tab)

    def _update_label_height(self, *_):
        # Expand label height to its texture to make ScrollView content size correct
        self.code_view.height = self.code_view.texture_size[1] + 20

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


class Tester6Apk(App):
    def build(self):
        self.title = "tester6 APK demo"
        return Root()


if __name__ == "__main__":
    Tester6Apk().run()