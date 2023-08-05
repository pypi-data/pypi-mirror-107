from subprocess import check_output
from os import geteuid

import re
import py_cui

from recoverpy import window_handler as WINDOW_HANDLER
from recoverpy import logger as LOGGER


class ParametersMenu:
    """Parameters menu is the first window displayed.
    User is prompted to select a partition and a string to search in it.

    Attributes:
        partition_to_search (str): Partition selected by user.
        string_to_search (str): String entered by user.
        partitions_list (list): Raw list of lsblk output.
        partitions_dict (dict): Dictionnary of system partitions found with
                lsblk command and their attributes.
    """

    def __init__(self, master: py_cui.PyCUI):
        """Constructor for Parameters menu

        Args:
            master (py_cui.PyCUI): PyCUI constructor
        """

        self.master = master

        self.partition_to_search = None
        self.string_to_search = None

        LOGGER.write("info", "Starting 'ParametersMenu' CUI window")

        self.is_user_root()

        self.partitions_list = self.lsblk()
        self.partitions_dict = self.format_partitions_list()

        self.create_ui_content()
        self.add_partitions_to_list()

    def create_ui_content(self):
        """Handles the creation of the UI elements."""

        self.partitions_list_cell = self.master.add_scroll_menu(
            "Select a partition to search:", 0, 0, row_span=9, column_span=5
        )
        self.partitions_list_cell.add_key_command(py_cui.keys.KEY_ENTER, self.select_partition)

        # Color rules
        self.partitions_list_cell.add_text_color_rule("Mounted at", py_cui.YELLOW_ON_BLACK, "contains")
        self.partitions_list_cell.set_selected_color(py_cui.GREEN_ON_BLACK)

        self.string_text_box = self.master.add_text_block("Enter a text to search:", 0, 5, row_span=9, column_span=5)

        self.start_search_button = self.master.add_button(
            "Start search",
            9,
            4,
            row_span=1,
            column_span=2,
            padx=0,
            pady=0,
            command=self.start_search,
        )

    def is_user_root(self) -> bool:
        """Checks if user has root privileges.
        The method is simply verifying if EUID == 0.
        It may be problematic in some edge cases. (Some particular OS)
        But, as grep search will not exit quickly, exception handling
        can't be used.

        Returns:
            bool: User is root
        """

        if geteuid() == 0:
            LOGGER.write("info", "User is root")
            return True

        self.master.show_error_popup("Not root", "You have to be root or use sudo.")
        LOGGER.write("warning", "User is not root")
        return False

    def format_partitions_list(self) -> dict:
        """Uses lsblk command to find partitions.

        Returns:
            dict: Found partitions with format :
                    {Name: FSTYPE, IS_MOUNTED, MOUNT_POINT}
        """

        # Create dict with relevant infos
        partitions_dict = {}
        for partition in self.partitions_list:
            if len(partition) < 3:
                # Ignore if no FSTYPE detected
                continue

            if len(partition) < 4:
                is_mounted = False
                mount_point = None
            else:
                is_mounted = True
                mount_point = partition[3]

            partitions_dict[partition[0]] = {
                "FSTYPE": partition[2],
                "IS_MOUNTED": is_mounted,
                "MOUNT_POINT": mount_point,
            }

        # Warn the user if no partition found with lsblk
        if len(partitions_dict) == 0:
            LOGGER.write("Error", "No partition found !")
            self.master.show_error_popup("Error", "No partition found.")
            return None

        LOGGER.write("debug", "Partition list generated using 'lsblk'")
        LOGGER.write(
            "debug",
            f"{str(len(partitions_dict))} partitions found",
        )

        return partitions_dict

    def lsblk(self) -> list:
        """Uses 'lsblk' utility to generate a list of detected
        system partions."

        Returns:
            list: List of system partitions.
        """

        lsblk_output = check_output(["lsblk", "-r", "-n", "-o", "NAME,TYPE,FSTYPE,MOUNTPOINT"], encoding="utf-8")
        partitions_list_raw = [
            line.strip() for line in lsblk_output.splitlines() if " loop " not in line and "swap" not in line
        ]
        partitions_list_formatted = [line.split(" ") for line in partitions_list_raw]

        LOGGER.write(
                    "debug",
                    str(partitions_list_formatted),
                )

        return partitions_list_formatted

    def add_partitions_to_list(self):
        """Populates the partition list with partition found previously."""

        if self.partitions_dict is None:
            return

        for partition in self.partitions_dict:
            if self.partitions_dict[partition]["IS_MOUNTED"]:
                self.partitions_list_cell.add_item(
                    "Name: {name}  -  Type: {fstype}  -  Mounted at: {mountpoint}".format(
                        name=partition,
                        fstype=self.partitions_dict[partition]["FSTYPE"],
                        mountpoint=self.partitions_dict[partition]["MOUNT_POINT"],
                    )
                )
            else:
                self.partitions_list_cell.add_item(
                    "Name: {name}  -  Type: {fstype}".format(
                        name=partition, fstype=self.partitions_dict[partition]["FSTYPE"]
                    )
                )

            LOGGER.write(
                "debug",
                f"Partition added to list: {str(partition)}",
            )

    def select_partition(self):
        """Handles the user selection of a partition in the list."""

        selected_partition = re.findall(r"Name\:\ ([^\ \n]+)\ ", self.partitions_list_cell.get())[0]

        if self.partitions_dict[selected_partition]["IS_MOUNTED"]:
            # Warn the user to unmount his partition first
            self.master.show_warning_popup(
                "Warning",
                f"It is highly recommended to unmount {selected_partition} first.",
            )
        else:
            self.master.show_message_popup("", f"Partition {selected_partition} selected.")

        self.partition_to_search = "/dev/" + selected_partition.strip()

        LOGGER.write(
            "info",
            f"Partition selected: {self.partition_to_search}",
        )

    def start_search(self):
        """Checks if partition is selected and string is given.
        If all required elements are present, launch confirm_search function.
        """

        if not self.is_user_root():
            return

        self.string_to_search = self.string_text_box.get()

        LOGGER.write("info", "Starting search")

        if self.partition_to_search == "":
            # No partition selected
            self.master.show_message_popup("Error", "You have to select a partition to search.")
            LOGGER.write("warning", "No partition selected for search")
        elif self.string_to_search.replace(" ", "").replace("\n", "").replace("\t", "") == "":
            # Blank string to search
            self.master.show_message_popup("Error", "You have to enter a text to search.")
            LOGGER.write("warning", "No string given for search")
        else:
            # Prompt to confirm string
            self.master.show_yes_no_popup(
                "Do you want to start searching this text on partition {partition} ?".format(
                    partition=self.partition_to_search
                ),
                self.confirm_search,
            )

    def confirm_search(self, is_confirmed: bool):
        """Closes parameters menu and open search menu if confirmed.

        Args:
            is_confirmed (bool): User popup selection
        """
        if is_confirmed:
            WINDOW_HANDLER.close_parameters_menu()
            WINDOW_HANDLER.open_search_menu(
                partition=self.partition_to_search,
                string_to_search=self.string_to_search.strip(),
            )
        else:
            pass
