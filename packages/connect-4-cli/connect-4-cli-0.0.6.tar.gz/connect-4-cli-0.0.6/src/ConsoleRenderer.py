import os
from rich.console import Console
import src.constants as const


class ConsoleRenderer():
    """Renders app into the console"""

    def __init__(self) -> None:
        """Constructor."""
        self.console = Console()
        self.char_cell_empty = "[bold grey37]•[/bold grey37]"
        self.char_cell_red = "[bold red]•[/bold red]"
        self.char_cell_yellow = "[bold yellow]•[/bold yellow]"
        self.board_for_print = [
            [self.char_cell_empty for i in range(const.BOARD_TOTAL_COLUMNS)]
            for j in range(const.BOARD_TOTAL_ROWS_PER_COLUMN)]
        self.col_selection = [
            self.char_cell_empty for i in range(const.BOARD_TOTAL_COLUMNS)]
        self.print_buffer = []

    def render(self, match):
        """Render/print screen seen by player, using current match"""
        self.clear_console()
        self._clear_buffer()
        self._set_header()
        self._set_current_infos(match)
        self._set_column_selector(match)
        self._set_board(match)
        self._set_tail()
        self._print_buffer()

    def clear_console(self):
        """Clear console"""
        command = 'clear'
        if os.name in ('nt', 'dos'):
            # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    def _update_board_for_print(self, columns):
        """Make board representation used for printing"""
        for i, col in enumerate(columns):
            for j, cell in enumerate(col.cells):
                if cell.is_red():
                    self.board_for_print[j][i] = self.char_cell_red
                elif cell.is_yellow():
                    self.board_for_print[j][i] = self.char_cell_yellow
                else:
                    self.board_for_print[j][i] = self.char_cell_empty

    def _update_column_selection_for_print(self, match):
        """Make representation of selected column for printing"""
        for i in range(const.BOARD_TOTAL_COLUMNS):
            self.col_selection[i] = "  "
            if (i == match.column_selected and
                    match.state == const.MatchState.PLAYING):
                if match.player_turn == const.PlayerTurn.RED:
                    self.col_selection[i] = self.char_cell_red
                elif match.player_turn == const.PlayerTurn.YELLOW:
                    self.col_selection[i] = self.char_cell_yellow

    def _set_header(self):
        """Add header string lines to print buffer"""
        self.print_buffer.append(" ")
        self.print_buffer.append("[bold cyan]»\tConnect4\t«[/bold cyan]")
        self.print_buffer.append(" ")
        self.print_buffer.append(" ")
        self.print_buffer.append(
            "[bold cyan]'q'[/bold cyan]  "
            "[cyan]quits game[/cyan]")
        self.print_buffer.append(
            "[bold cyan]'r'[/bold cyan]  "
            "[cyan]restarts game[/cyan]")
        self.print_buffer.append(
            "[bold cyan]← → [/bold cyan] "
            "[cyan]arrows change column[/cyan]")
        self.print_buffer.append(
            "[bold cyan]←┘[/bold cyan]   "
            "[cyan]enter drops checker[/cyan]")
        self.print_buffer.append(" ")

    def _set_current_infos(self, match):
        """Add current match information to print buffer"""
        self.print_buffer.append(" ")
        p_name = match.player_turn.name
        tag = p_name.lower()
        if match.state == const.MatchState.PLAYING:
            self.print_buffer.append(
                f"  Turn for player [bold {tag}]{p_name}[/bold {tag}]")
        elif match.state == const.MatchState.TIE:
            self.print_buffer.append(
                "  This match is a [bold]tie[/bold]")
        else:
            self.print_buffer.append(
                f" [bold {tag}]Victory for player {p_name}!![/bold {tag}]")
        self.print_buffer.append(" ")

    def _set_column_selector(self, match):
        """Add column selector indicator to print buffer"""
        self._update_column_selection_for_print(match)
        self.print_buffer.append(" " * 3)
        self.print_buffer[-1] += (" ".join(self.col_selection))
        self.print_buffer.append(" ")

    def _set_board(self, match):
        """Add connect4 board representation to print buffer"""
        self._update_board_for_print(match.board.columns)
        for row in self.board_for_print[::-1]:
            self.print_buffer.append(" " * 3)
            self.print_buffer[-1] += ("  ".join(row))

    def _set_tail(self):
        """Add tail/bottom information to print buffer"""
        self.print_buffer.append(" ")
        self.print_buffer.append(" ")
        self.print_buffer.append(
            "[grey37]made with [dark_red]♥[/dark_red] "
            "by gmso (github.com/gmso)[/grey37]")

    def _print_buffer(self):
        """Print buffer into console"""
        for line in self.print_buffer:
            self.console.print(line)

    def _clear_buffer(self):
        """Clear print buffer"""
        self.print_buffer = []
