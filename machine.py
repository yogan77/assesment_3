import json


class Machine:

    def __init__(
        self,
        machine_id,
        plant_name,
        operating_hours,
        downtime,
        energy_consumption,
        units_produced,
        maintenance_cost,
    ):
        self.machine_id = machine_id
        self.plant_name = plant_name
        self.operating_hours = operating_hours
        self.downtime = downtime
        self.energy_consumption = energy_consumption
        self.units_produced = units_produced
        self.maintenance_cost = maintenance_cost

    # 1. Calculate Machine Efficiency
    def calculate_efficiency(self):
        active_hours = self.operating_hours - self.downtime
        if active_hours <= 0:
            return 0.0
        return self.units_produced / active_hours

    # 2. Calculate Production Cost per Unit (Energy Cost + Maintenance Cost)
    # Assuming a standard generic energy cost rate (e.g., $0.15 per kWh)
    def calculate_cost_per_unit(self, energy_rate=0.15):
        if self.units_produced == 0:
            return 0.0
        total_cost = (
            self.energy_consumption * energy_rate
        ) + self.maintenance_cost
        return total_cost / self.units_produced

    # 6. Check if Preventive Maintenance is required
    # Criteria: High downtime (>15 hours) OR high operating hours (>200 hours)
    def requires_maintenance(self):
        return self.downtime > 15 or self.operating_hours > 200

    def to_dict(self):
        return {
            "Machine ID": self.machine_id,
            "Plant Name": self.plant_name,
            "Efficiency (units/hr)": round(self.calculate_efficiency(), 2),
            "Cost Per Unit": round(self.calculate_cost_per_unit(), 2),
            "Maintenance Required": self.requires_maintenance(),
        }


class PlantManager:

    def __init__(self):
        self.machines = []

    def add_machine(self, machine):
        self.machines.append(machine)

    # 3. Identify Inefficient Machines (Efficiency below a threshold, e.g., 20 units/hr)
    def get_inefficient_machines(self, threshold=20.0):
        return [
            m
            for m in self.machines
            if m.calculate_efficiency() < threshold
        ]

    # 4. Find Machine with Highest Maintenance Cost
    def get_highest_maintenance_machine(self):
        if not self.machines:
            return None
        return max(self.machines, key=lambda m: m.maintenance_cost)

    # 5. Calculate Plant-wise Efficiency
    def get_plant_wise_efficiency(self):
        plant_data = {}
        for m in self.machines:
            if m.plant_name not in plant_data:
                plant_data[m.plant_name] = {
                    "total_units": 0,
                    "total_active_hours": 0,
                }
            plant_data[m.plant_name]["total_units"] += m.units_produced
            plant_data[m.plant_name]["total_active_hours"] += (
                m.operating_hours - m.downtime
            )

        plant_efficiencies = {}
        for plant, data in plant_data.items():
            if data["total_active_hours"] <= 0:
                plant_efficiencies[plant] = 0.0
            else:
                plant_efficiencies[plant] = round(
                    data["total_units"] / data["total_active_hours"], 2
                )
        return plant_efficiencies

    # 6. Displays machines requiring preventive maintenance
    def get_maintenance_candidates(self):
        return [m for m in self.machines if m.requires_maintenance()]

    # 7. Sort machines by efficiency
    def get_machines_sorted_by_efficiency(self, reverse=True):
        return sorted(
            self.machines, key=lambda m: m.calculate_efficiency(), reverse=reverse
        )

    # 8. Generate a maintenance report summary
    def generate_report(self):
        sorted_machines = self.get_machines_sorted_by_efficiency()
        highest_maint = self.get_highest_maintenance_machine()

        report = {
            "Plant-wide Efficiency": self.get_plant_wise_efficiency(),
            "Highest Maintenance Cost Machine": (
                highest_maint.machine_id if highest_maint else "None"
            ),
            "Inefficient Machines": [
                m.machine_id for m in self.get_inefficient_machines()
            ],
            "Machines Requiring Maintenance": [
                m.machine_id for m in self.get_maintenance_candidates()
            ],
            "All Machines Ranked By Efficiency": [
                m.to_dict() for m in sorted_machines
            ],
        }
        return report

    # 9. Save report to file
    def save_report_to_file(self, filename="maintenance_report.json"):
        report = self.generate_report()
        with open(filename, "w") as f:
            json.dump(report, f, indent=4)
        print(f"[Success] Report successfully saved to '{filename}'")

    # 10. Read the report from file
    @staticmethod
    def read_report_from_file(filename="maintenance_report.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return f"Error: File '{filename}' not found."


# --- Execution Example ---
if __name__ == "__main__":
    manager = PlantManager()

    # Populate Sample Data
    # Arguments: ID, Plant, Op Hours, Downtime, Energy(kWh), Units, Maint Cost
    manager.add_machine(Machine("M001", "Alpha Plant", 150, 10, 1200, 3500, 450))
    manager.add_machine(Machine("M002", "Alpha Plant", 220, 40, 1800, 2000, 900))
    manager.add_machine(Machine("M003", "Beta Plant", 100, 5, 800, 2500, 200))
    manager.add_machine(Machine("M004", "Beta Plant", 180, 35, 1400, 1500, 1100))

    # 1 & 2. Individual metrics can be called directly from Machine instances
    print("--- 1 & 2. Sample Individual Machine Metrics ---")
    sample_machine = manager.machines[0]
    print(
        f"Machine {sample_machine.machine_id} Efficiency: {sample_machine.calculate_efficiency():.2f} units/hour"
    )
    print(
        f"Machine {sample_machine.machine_id} Cost Per Unit: ${sample_machine.calculate_cost_per_unit():.2f}\n"
    )

    # 3. Identify inefficient machines
    print("--- 3. Inefficient Machines (< 20 units/hr) ---")
    for m in manager.get_inefficient_machines():
        print(
            f"Machine: {m.machine_id} | Efficiency: {m.calculate_efficiency():.2f}"
        )

    # 4. Find machine with highest maintenance cost
    print("\n--- 4. Highest Maintenance Cost Machine ---")
    highest_maint = manager.get_highest_maintenance_machine()
    print(
        f"Machine: {highest_maint.machine_id} | Cost: ${highest_maint.maintenance_cost}"
    )

    # 5. Plant-wise efficiency
    print("\n--- 5. Plant-Wise Efficiency ---")
    for plant, eff in manager.get_plant_wise_efficiency().items():
        print(f"Plant: {plant} | Avg Efficiency: {eff} units/hour")

    # 6. Machines requiring preventive maintenance
    print("\n--- 6. Preventive Maintenance Needed ---")
    for m in manager.get_maintenance_candidates():
        print(
            f"Machine: {m.machine_id} (Downtime: {m.downtime}h, OpHours: {m.operating_hours}h)"
        )

    # 7. Sort machines by efficiency
    print("\n--- 7. Machines Sorted By Efficiency (Highest to Lowest) ---")
    for m in manager.get_machines_sorted_by_efficiency():
        print(
            f"Machine: {m.machine_id} | Efficiency: {m.calculate_efficiency():.2f}"
        )

    # 8 & 9. Generate and Save Report to File
    print("\n--- 8 & 9. Generating and Saving Report ---")
    manager.save_report_to_file("factory_report.json")

    # 10. Read the Report
    print("\n--- 10. Reading Saved Report From File ---")
    saved_data = PlantManager.read_report_from_file("factory_report.json")
    print(json.dumps(saved_data, indent=2))
