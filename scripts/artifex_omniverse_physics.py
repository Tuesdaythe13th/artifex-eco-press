# ---------------------------------------------------------
# ARTIFEX ECO‑PRESS – REV 8.4 DIGITAL TWIN (V2 ADVANCED)
# ---------------------------------------------------------

from omni.isaac.kit import SimulationApp  # type: ignore

simulation_app = SimulationApp({"headless": False})

import numpy as np  # type: ignore
import csv
from enum import Enum
from datetime import datetime
from omni.isaac.core import World  # type: ignore
from omni.isaac.core.objects import DynamicCuboid, VisualCylinder  # type: ignore

class CycleState(Enum):
    MOLD_CLOSE = 1
    INJECTION = 2
    COMPRESSION = 3
    COOLING_AND_CHARGE = 4
    MOLD_OPEN = 5
    EXTRACTION_AUDIT = 6

class ArtifexRev84DigitalTwin:
    """
    Artifex Eco‑Press Digital Twin (Rev 8.4) - ADVANCED
    Improvements:
    - Generates the physical 12-inch r-PET record dynamically during injection.
    - Applies thermodynamic color changes to the RECORD (not the steel platen).
    - Logs live 48-second telemetry to a CSV file simulating Portenta UART4.
    - Uses strict State Machine enum architecture.
    """

    # --- Rev 8.4 Physics Constants ---
    CLAMP_FORCE_KN = 1007.0          
    ACCUMULATOR_VOL_L = 18.9         
    ROD_FILL_L = 5.58                
    RETRACT_TIME_S = 0.58            
    SERVO_RPM = 1680.0               
    INJ_STROKE_S = 3.0               
    THERMAL_SETPOINT_C = 270.0       
    COOLING_DROP_C = (180.0, 120.0)  

    def __init__(self, world: World):
        self.world = world
        self.cycle_count = 0
        self.telemetry_file = open("artifex_telemetry_sim.csv", "w", newline="")
        self.csv_writer = csv.writer(self.telemetry_file)
        self.csv_writer.writerow(["timestamp", "cycle_id", "state", "gap_mm", "force_kn", "record_temp_c"])
        
        self.setup_scene()

    def setup_scene(self):
        """Construct the 3‑D hierarchy using exact Rev 8.4 dimensions."""
        # 1. H‑Frame (Sage Green)
        self.press = self.world.scene.add(
            DynamicCuboid(
                prim_path="/World/Artifex/PressFrame",
                position=np.array([0.0, 0.0, 0.5]),
                scale=np.array([1.0, 1.0, 1.0]),
                color=np.array([0.35, 0.45, 0.35]),
                mass=1500.0,
            )
        )

        # 2. 5‑Gallon Accumulator (Safety Orange)
        self.accumulator = self.world.scene.add(
            VisualCylinder(
                prim_path="/World/Artifex/Accumulator",
                position=np.array([-0.8, 0.0, 0.6]),
                radius=0.15,
                height=0.6,
                color=np.array([1.0, 0.3, 0.0]),
            )
        )
        self.accumulator.set_parent(self.press)

        # 3. 12‑inch Moving Platen (Steel)
        self.platen = self.world.scene.add(
            DynamicCuboid(
                prim_path="/World/Artifex/MovingPlaten",
                position=np.array([0.0, 0.0, 1.5]),
                scale=np.array([0.4, 0.4, 0.1]),
                color=np.array([0.8, 0.8, 0.82]),
                mass=200.0,
            )
        )

        # 4. The 12-inch Record (r-PET)
        self.record = self.world.scene.add(
            VisualCylinder(
                prim_path="/World/Artifex/VinylRecord",
                position=np.array([0.0, 0.0, 1.001]),
                radius=0.001, # Starts invisible
                height=0.003, # 3mm thick
                color=np.array([1.0, 0.5, 0.0]) # Starts hot molten orange
            )
        )

    @staticmethod
    def _temp_to_color(temp_c: float, low_c: float, high_c: float) -> np.ndarray:
        """Interpolates molten PET (orange/red) down to cooled state (dark grey)."""
        temp_c = np.clip(temp_c, low_c, high_c)
        t = (temp_c - low_c) / (high_c - low_c)
        # Hot = [1.0, 0.5, 0.0] (Molten), Cool = [0.1, 0.1, 0.1] (Dark Vinyl)
        r = 0.1 + (0.9 * t)
        g = 0.1 + (0.4 * t)
        b = 0.1
        return np.array([r, g, b])

    def log_telemetry(self, state: str, gap_mm: float, force_kn: float, temp_c: float):
        ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        self.csv_writer.writerow([ts, f"C-{self.cycle_count:03d}", state, f"{gap_mm:.1f}", f"{force_kn:.1f}", f"{temp_c:.1f}"])

    def execute_48s_cycle(self, time_s: float) -> str:
        cycle_time = time_s % 48.0
        
        # Increment cycle count on wraparound
        if cycle_time < 0.05 and time_s > 1.0:
            self.cycle_count += 1
            # Reset record geometry for new cycle
            self.record.set_world_pose(position=np.array([0.0, 0.0, 1.001]))
            self.record.set_local_scale(np.array([0.001, 0.001, 1.0]))

        # --- 1. MOLD CLOSE (0-4.5s) ---
        if cycle_time < 4.5:
            progress = cycle_time / 4.5
            z_pos = 1.5 - (0.498 * progress)
            self.platen.set_world_pose(position=np.array([0.0, 0.0, z_pos]))
            
            gap = (z_pos - 1.0) * 1000.0
            self.log_telemetry("MOLD_CLOSE", gap, 0.0, 25.0)
            return f"Mold Close | Gap: {gap:.1f}mm"

        # --- 2. INJECTION (4.5-7.5s) ---
        elif cycle_time < 7.5:
            self.platen.set_world_pose(position=np.array([0.0, 0.0, 1.002]))
            
            # Animate the plastic filling the 2mm cavity (radius grows to 150mm)
            progress = (cycle_time - 4.5) / self.INJ_STROKE_S
            current_radius = 0.001 + (0.15 * progress)
            
            # Scale the cylinder (Isaac Sim uses scale for dynamic resizing)
            # Base radius is 0.15, so scale goes from 0.0 to 1.0
            scale_factor = current_radius / 0.15
            self.record.set_local_scale(np.array([scale_factor, scale_factor, 1.0]))
            self.record.set_color(np.array([1.0, 0.5, 0.0])) # Molten
            
            self.log_telemetry("INJECTION", 2.0, 33.7, 270.0)
            return f"Injection | RPM: {self.SERVO_RPM} | Fill: {progress*100:.1f}%"

        # --- 3. COMPRESSION (7.5-12.5s) ---
        elif cycle_time < 12.5:
            self.platen.set_world_pose(position=np.array([0.0, 0.0, 1.0]))
            force_n = np.array([0.0, 0.0, -self.CLAMP_FORCE_KN * 1000.0])
            self.platen.apply_force(force_n)
            
            self.log_telemetry("COMPRESSION", 0.0, self.CLAMP_FORCE_KN, 180.0)
            return f"Compression | Force: {self.CLAMP_FORCE_KN:.1f}kN"

        # --- 4. ACTIVE COOLING (12.5-24.5s) ---
        elif cycle_time < 24.5:
            self.platen.set_world_pose(position=np.array([0.0, 0.0, 1.0]))
            elapsed = cycle_time - 12.5
            temp = max(self.COOLING_DROP_C[1], self.COOLING_DROP_C[0] - (elapsed * 5.0)) # Drops 60C over 12s
            
            # Apply thermodynamic color change to the RECORD
            color = self._temp_to_color(temp, self.COOLING_DROP_C[1], self.COOLING_DROP_C[0])
            self.record.set_color(color)
            
            self.log_telemetry("COOLING", 0.0, 0.0, temp)
            return f"Cooling | Accum Vol: {self.ACCUMULATOR_VOL_L}L | Record Temp: {temp:.1f}C"

        # --- 5. MOLD OPEN (24.5-25.08s) ---
        elif cycle_time < 25.08:
            progress = (cycle_time - 24.5) / self.RETRACT_TIME_S
            z_pos = 1.0 + (0.08 * progress)
            self.platen.set_world_pose(position=np.array([0.0, 0.0, z_pos]))
            
            self.log_telemetry("MOLD_OPEN", (z_pos - 1.0)*1000, 0.0, self.COOLING_DROP_C[1])
            return f"Accumulator Dump | Retract: 80mm | Time: {self.RETRACT_TIME_S}s"

        # --- 6. EXTRACTION & AUDIT (25.08-48s) ---
        else:
            self.platen.set_world_pose(position=np.array([0.0, 0.0, 1.08]))
            # Robot moves the record to the camera
            self.record.set_world_pose(position=np.array([0.6, 0.0, 1.001]))
            
            self.log_telemetry("EXTRACTION", 80.0, 0.0, 60.0)
            return "Robot Extraction & AI Audit"

    def shutdown(self):
        self.telemetry_file.close()


def main():
    world = World()
    world.scene.add_default_ground_plane()

    twin = ArtifexRev84DigitalTwin(world)
    world.reset()

    print("--- ARTIFEX REV 8.4 DIGITAL TWIN ENGAGED (V2 ADVANCED) ---")

    step_count = 0
    try:
        while simulation_app.is_running():
            world.step(render=True)
            time_s = step_count * world.get_physics_dt()

            state_msg = twin.execute_48s_cycle(time_s)

            if step_count % 60 == 0:
                print(f"[C-{twin.cycle_count:03d} | T={time_s % 48.0:04.1f}s] {state_msg}")

            step_count += 1
    finally:
        twin.shutdown()
        simulation_app.close()

if __name__ == "__main__":
    main()
