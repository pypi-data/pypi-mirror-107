from coopui.cli.CliAtomicUserInteraction import CliAtomicUserInteraction
from coopui.cli.CliMenu import CliMenu
from coopgantt.cli.user_operations import UserOperations


def main(menu_title: str = "MAIN MENU"):
    ui = CliAtomicUserInteraction()
    uo = UserOperations(ui)
    main_menu = CliMenu(f"************{menu_title}*****************",
                        {
                            "G": ("[G]enerate Gantt", lambda: uo.generate_a_gantt()),
                            "R": ("[R]ender an HTML", lambda: uo.render_an_html()),
                            "S": ("[S]ave Gantt", lambda: uo.save_gantt_data()),
                            "E": ("[E]nd to end", lambda: uo.create_render_and_save()),
                            "T": ("Set s[T]ate", lambda: uo.set_state()),
                            "X": ("E[X]it", None)
                        },
                        ui.notify_user)


    main_menu.run()

