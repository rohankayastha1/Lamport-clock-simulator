import tkinter as tk
from tkinter import messagebox, Toplevel, Checkbutton, IntVar, Canvas, Scrollbar, Frame, Label, Button


class LogicalClock:
    def __init__(self, process_name):
        self.timestamp = 0
        self.process_name = process_name

    def trigger_event(self):
        """Handles a generic event by incrementing the timestamp."""
        self.timestamp += 1
        return self.timestamp

    def transmit_event(self):
        """Handles transmitting a message by incrementing the timestamp."""
        self.timestamp += 1
        return self.timestamp

    def accept_event(self, incoming_time):
        """Handles receiving a message and synchronizing the clock."""
        self.timestamp = max(self.timestamp, incoming_time) + 1
        return self.timestamp


class LogicalClockSimulation:
    def __init__(self, total_processes):
        self.processes = [LogicalClock(process_name=f"Process {i+1}") for i in range(total_processes)]
        self.snapshots = []
        self.pending_messages = []

    def get_timestamp(self, process_index):
        """Gets the current timestamp of the specified process."""
        return self.processes[process_index].timestamp

    def trigger_event(self, process_index):
        """Triggers a generic event for the specified process."""
        return self.processes[process_index].trigger_event()

    def transmit_event(self, process_index):
        """Triggers a transmission event for the specified process."""
        return self.processes[process_index].transmit_event()

    def accept_event(self, receiver_index, transmitted_time):
        """Triggers a reception event for the specified process."""
        return self.processes[receiver_index].accept_event(transmitted_time)

    def record_message(self, receiver_index, transmitted_time):
        """Records a transmitted message for later processing."""
        self.pending_messages.append((receiver_index, transmitted_time))

    def process_message(self, receiver_index, message_index):
        """Processes a specific message in the pending queue."""
        if 0 <= message_index < len(self.pending_messages):
            _, incoming_time = self.pending_messages.pop(message_index)
            self.accept_event(receiver_index, incoming_time)

    def capture_snapshot(self):
        """Captures the current state of all processes."""
        snapshot = {process.process_name: process.timestamp for process in self.processes}
        self.snapshots.append(snapshot)
        return snapshot


class LogicalClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logical Clock Simulator")

        self.simulation = None

        self.canvas = Canvas(self.root)
        self.scrollbar = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.setup_ui()

    def setup_ui(self):
        Label(self.scrollable_frame, text="Enter number of processes:").pack(pady=10)
        self.process_count_entry = tk.Entry(self.scrollable_frame)
        self.process_count_entry.pack(pady=10)

        Button(self.scrollable_frame, text="Initialize Processes", command=self.initialize_processes).pack(pady=10)

        self.process_frame = Frame(self.scrollable_frame)
        self.process_frame.pack(pady=20)

        self.snapshot_button = Button(self.scrollable_frame, text="Capture Snapshot", command=self.capture_snapshot, state=tk.DISABLED)
        self.snapshot_button.pack(pady=10)

        self.snapshot_label = Label(self.scrollable_frame, text="")
        self.snapshot_label.pack(pady=10)

    def initialize_processes(self):
        try:
            num_processes = int(self.process_count_entry.get())
            if num_processes <= 0:
                raise ValueError("Number of processes must be positive.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.simulation = LogicalClockSimulation(num_processes)

        for widget in self.process_frame.winfo_children():
            widget.destroy()

        for i in range(num_processes):
            process_label = Label(self.process_frame, text=f"Process {i+1} Clock: {self.simulation.get_timestamp(i)}")
            process_label.grid(row=i, column=0, padx=20, pady=5)

            Button(self.process_frame, text="Trigger Event", command=lambda idx=i, lbl=process_label: self.trigger_event(idx, lbl)).grid(row=i, column=1, padx=20, pady=5)
            Button(self.process_frame, text="Transmit Message", command=lambda idx=i, lbl=process_label: self.open_transmit_dialog(idx, lbl)).grid(row=i, column=2, padx=20, pady=5)
            Button(self.process_frame, text="Accept Message", command=lambda idx=i, lbl=process_label: self.accept_message_dialog(idx, lbl)).grid(row=i, column=3, padx=20, pady=5)

        self.snapshot_button.config(state=tk.NORMAL)

    def trigger_event(self, process_index, label):
        self.simulation.trigger_event(process_index)
        label.config(text=f"Process {process_index+1} Clock: {self.simulation.get_timestamp(process_index)}")

    def open_transmit_dialog(self, sender_index, label):
        dialog = Toplevel(self.root)
        dialog.title("Select Recipients")

        checkboxes = []
        recipient_vars = []

        for i in range(len(self.simulation.processes)):
            if i != sender_index:
                var = IntVar()
                chk = Checkbutton(dialog, text=f"Process {i+1}", variable=var)
                chk.pack(anchor="w")
                checkboxes.append(chk)
                recipient_vars.append(var)

        def send_messages():
            timestamp = self.simulation.transmit_event(sender_index)
            for i, var in enumerate(recipient_vars):
                if var.get() == 1:
                    receiver_index = i if i < sender_index else i + 1
                    self.simulation.record_message(receiver_index, timestamp)
            label.config(text=f"Process {sender_index+1} Clock: {self.simulation.get_timestamp(sender_index)}")
            dialog.destroy()

        Button(dialog, text="Send", command=send_messages).pack()

    def accept_message_dialog(self, receiver_index, label):
        dialog = Toplevel(self.root)
        dialog.title("Pending Messages")

        messages = [(idx, msg[1]) for idx, msg in enumerate(self.simulation.pending_messages) if msg[0] == receiver_index]

        if not messages:
            Label(dialog, text="No messages to accept.").pack()
            Button(dialog, text="Close", command=dialog.destroy).pack()
            return

        selected_var = IntVar()

        for idx, timestamp in messages:
            Radiobutton(dialog, text=f"Message from Timestamp {timestamp}", variable=selected_var, value=idx).pack(anchor="w")

        def accept_message():
            if selected_var.get() >= 0:
                self.simulation.process_message(receiver_index, selected_var.get())
                label.config(text=f"Process {receiver_index+1} Clock: {self.simulation.get_timestamp(receiver_index)}")
                dialog.destroy()

        Button(dialog, text="Accept", command=accept_message).pack()

    def capture_snapshot(self):
        snapshot = self.simulation.capture_snapshot()
        dialog = Toplevel(self.root)
        dialog.title("Snapshot")
        Label(dialog, text="Snapshot of Logical Clocks").pack(pady=10)

        for process, timestamp in snapshot.items():
            Label(dialog, text=f"{process}: {timestamp}").pack(anchor="w")

        Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = LogicalClockApp(root)
    root.mainloop()
