
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import math
import numpy as np
import pandas as pd


# ============================================================
# Synthetic Manufacturing Data Generator
# ============================================================
# Design goals:
# 1. Preserve cross-table relationships.
# 2. Use operational constraints instead of independent random values.
# 3. Create plant/line/machine/product/shift effects.
# 4. Link downtime, quality, maintenance, and sensor behavior.
# 5. Create source-system-like outputs for ERP / MES / QMS / CMMS / SCADA.
#
# The data is synthetic and should be described as simulated in a portfolio.
# ============================================================


@dataclass
class Config:
    seed: int = 42
    start_date: str = "2026-01-01"
    days: int = 180
    plants: int = 3
    lines_per_plant: int = 3
    machines_per_line: int = 4
    products: int = 8


SHIFT_DEFS = [
    ("A", 6, 14),
    ("B", 14, 22),
    ("C", 22, 6),
]

DOWNTIME_CAUSES = {
    "planned": {
        "Changeover": 0.44,
        "Preventive Maintenance": 0.30,
        "Cleaning/Sanitation": 0.16,
        "Planned Inspection": 0.10,
    },
    "unplanned": {
        "Mechanical Failure": 0.30,
        "Electrical Fault": 0.17,
        "Material Starvation": 0.14,
        "Quality Hold": 0.13,
        "Sensor/Controls Fault": 0.10,
        "Operator Adjustment": 0.09,
        "Utility Interruption": 0.07,
    },
}

DEFECT_TYPES = [
    "Dimensional",
    "Surface",
    "Assembly",
    "Contamination",
    "Label/Packaging",
    "Functional Test",
]

MATERIALS = [
    "Steel",
    "Aluminum",
    "Polymer",
    "Copper",
    "Fastener Kit",
    "Packaging",
]


def _normalize(weights):
    arr = np.array(weights, dtype=float)
    return arr / arr.sum()


def make_dimensions(cfg: Config, rng: np.random.Generator):
    plants = []
    for p in range(1, cfg.plants + 1):
        plants.append({
            "plant_id": f"P{p:02d}",
            "plant_name": f"Plant {chr(64+p)}",
            "region": ["Southeast", "Midwest", "Southwest"][p-1 if p <= 3 else 0],
            "timezone": ["America/New_York", "America/Chicago", "America/Denver"][p-1 if p <= 3 else 0],
            "planned_shift_hours": 8.0,
        })
    dim_plant = pd.DataFrame(plants)

    lines = []
    machines = []
    machine_num = 1
    for plant in dim_plant["plant_id"]:
        for l in range(1, cfg.lines_per_plant + 1):
            line_id = f"{plant}_L{l:02d}"
            # Different lines have meaningfully different nominal capacity.
            line_rate = float(rng.uniform(42, 78))
            lines.append({
                "line_id": line_id,
                "plant_id": plant,
                "line_name": f"Line {l}",
                "nominal_units_per_hour": round(line_rate, 1),
                "commission_year": int(rng.integers(2008, 2024)),
            })
            for m in range(1, cfg.machines_per_line + 1):
                machine_id = f"M{machine_num:03d}"
                age_years = int(rng.integers(2, 18))
                health = float(np.clip(rng.normal(0.82 - age_years*0.008, 0.06), 0.48, 0.97))
                machines.append({
                    "machine_id": machine_id,
                    "line_id": line_id,
                    "plant_id": plant,
                    "machine_name": f"{line_id}-Machine-{m}",
                    "machine_type": ["Press", "CNC", "Assembly", "Packaging"][m-1 if m <= 4 else (m-1) % 4],
                    "install_year": 2026 - age_years,
                    "rated_units_per_hour": round(line_rate * rng.uniform(0.90, 1.12), 1),
                    "baseline_health_index": round(health, 3),
                })
                machine_num += 1

    dim_line = pd.DataFrame(lines)
    dim_machine = pd.DataFrame(machines)

    products = []
    for i in range(1, cfg.products + 1):
        family = ["Standard", "Premium", "Industrial"][i % 3]
        base_cycle_sec = float(rng.uniform(38, 82))
        products.append({
            "product_id": f"SKU{i:03d}",
            "product_name": f"Product {i:03d}",
            "product_family": family,
            "standard_cycle_seconds": round(base_cycle_sec, 1),
            "standard_unit_cost": round(float(rng.uniform(18, 85)), 2),
            "target_scrap_rate": round(float(rng.uniform(0.008, 0.035)), 4),
        })
    dim_product = pd.DataFrame(products)

    shifts = pd.DataFrame([
        {"shift_id": s, "start_hour": start, "end_hour": end, "scheduled_hours": 8}
        for s, start, end in SHIFT_DEFS
    ])

    return dim_plant, dim_line, dim_machine, dim_product, shifts


def _shift_start(date, shift_id):
    row = {x[0]: x for x in SHIFT_DEFS}[shift_id]
    start_hour = row[1]
    return pd.Timestamp(date) + pd.Timedelta(hours=start_hour)


def _product_mix_for_line(line_id, products, rng):
    # Give each line a preferred subset but still allow cross-product production.
    n = len(products)
    weights = rng.dirichlet(np.ones(n) * 0.8)
    return dict(zip(products, weights))


def generate_orders(cfg, dim_plant, dim_product, rng):
    dates = pd.date_range(cfg.start_date, periods=cfg.days, freq="D")
    rows = []
    order_no = 1

    # Demand with weekday seasonality, product mix, and occasional peaks.
    for plant in dim_plant["plant_id"]:
        for date in dates:
            weekday_factor = 0.78 if date.dayofweek >= 5 else 1.0
            month_factor = 1 + 0.10 * math.sin(2 * math.pi * date.dayofyear / 90)
            shock = rng.choice([0.82, 1.0, 1.18], p=[0.05, 0.90, 0.05])
            n_orders = max(1, int(rng.poisson(4.5 * weekday_factor)))
            for _ in range(n_orders):
                prod = rng.choice(dim_product["product_id"])
                qty = int(max(40, rng.normal(380, 150) * month_factor * shock))
                due = date + pd.Timedelta(days=int(rng.integers(1, 8)))
                rows.append({
                    "order_id": f"SO{order_no:07d}",
                    "plant_id": plant,
                    "product_id": prod,
                    "order_date": date.date(),
                    "due_date": due.date(),
                    "order_qty": qty,
                    "priority": rng.choice(["Normal", "High", "Expedite"], p=[0.84, 0.13, 0.03]),
                    "status": "Released",
                })
                order_no += 1
    return pd.DataFrame(rows)


def generate_production(cfg, dims, orders, rng):
    dim_plant, dim_line, dim_machine, dim_product, dim_shift = dims
    dates = pd.date_range(cfg.start_date, periods=cfg.days, freq="D")

    line_mix = {
        line: _product_mix_for_line(line, dim_product["product_id"].tolist(), rng)
        for line in dim_line["line_id"]
    }

    work_orders = []
    production = []
    downtime = []
    quality = []
    maintenance = []
    sensor_rows = []

    wo_num = 1
    event_num = 1
    q_num = 1
    maint_num = 1

    # Stable plant effects: represent true operational differences.
    plant_perf = {
        plant: float(np.clip(rng.normal(0.96, 0.025), 0.90, 1.02))
        for plant in dim_plant["plant_id"]
    }
    plant_quality = {
        plant: float(np.clip(rng.normal(1.0, 0.10), 0.82, 1.22))
        for plant in dim_plant["plant_id"]
    }

    # Shift effects are common in real facilities.
    shift_perf = {"A": 1.00, "B": 0.97, "C": 0.93}
    shift_scrap = {"A": 1.00, "B": 1.08, "C": 1.18}

    product_map = dim_product.set_index("product_id").to_dict("index")
    line_map = dim_line.set_index("line_id").to_dict("index")
    machine_map = dim_machine.set_index("machine_id").to_dict("index")

    # Track machine hours since maintenance to influence failure hazard.
    hours_since_pm = {m: float(rng.uniform(0, 350)) for m in dim_machine["machine_id"]}

    for date in dates:
        for _, line in dim_line.iterrows():
            plant_id = line["plant_id"]
            line_id = line["line_id"]
            line_machines = dim_machine.loc[dim_machine["line_id"] == line_id, "machine_id"].tolist()

            for shift_id, _, _ in SHIFT_DEFS:
                # Some weekend shifts are not scheduled.
                if date.dayofweek >= 5 and rng.random() < 0.35:
                    continue

                product_ids = list(line_mix[line_id].keys())
                probs = list(line_mix[line_id].values())
                product_id = rng.choice(product_ids, p=probs)
                prod = product_map[product_id]

                shift_start = _shift_start(date, shift_id)
                scheduled_minutes = 480

                # Changeover probability higher when product changes across shifts.
                planned_dt = 0
                if rng.random() < 0.38:
                    planned_dt += int(np.clip(rng.lognormal(mean=np.log(28), sigma=0.35), 12, 80))

                if rng.random() < 0.08:
                    planned_dt += int(rng.integers(20, 55))

                # Generate unplanned failures based on weakest machine + hours since PM.
                weakest = min(line_machines, key=lambda m: machine_map[m]["baseline_health_index"])
                health = machine_map[weakest]["baseline_health_index"]
                hazard = 0.035 + (1-health)*0.18 + min(hours_since_pm[weakest] / 1800, 0.10)
                n_failures = int(rng.poisson(hazard * 1.8))
                unplanned_dt = 0

                failure_records = []
                for _ in range(n_failures):
                    machine_id = rng.choice(line_machines)
                    cause = rng.choice(
                        list(DOWNTIME_CAUSES["unplanned"].keys()),
                        p=list(DOWNTIME_CAUSES["unplanned"].values())
                    )
                    duration = int(np.clip(rng.lognormal(mean=np.log(24), sigma=0.75), 4, 220))
                    unplanned_dt += duration
                    failure_records.append((machine_id, cause, duration))

                total_dt = min(planned_dt + unplanned_dt, 300)
                operating_minutes = max(60, scheduled_minutes - total_dt)

                # Ideal rate derived from product standard cycle time, limited by line capability.
                product_rate = 3600.0 / prod["standard_cycle_seconds"]
                ideal_rate = min(product_rate, line["nominal_units_per_hour"])

                # Speed loss depends on plant, shift, product complexity, and natural variation.
                complexity_penalty = {"Standard": 1.0, "Premium": 0.96, "Industrial": 0.92}[prod["product_family"]]
                perf_factor = np.clip(
                    plant_perf[plant_id] * shift_perf[shift_id] * complexity_penalty * rng.normal(0.97, 0.035),
                    0.72, 1.03
                )

                gross_units = int(max(0, operating_minutes / 60 * ideal_rate * perf_factor))

                # Scrap increases with night shift, poor health, and high throughput pressure.
                avg_health = np.mean([machine_map[m]["baseline_health_index"] for m in line_machines])
                pressure = max(0, perf_factor - 0.98)
                base_scrap = prod["target_scrap_rate"] * plant_quality[plant_id] * shift_scrap[shift_id]
                scrap_rate = np.clip(
                    base_scrap + (1-avg_health)*0.015 + pressure*0.08 + rng.normal(0, 0.004),
                    0.002, 0.12
                )
                scrap_units = int(round(gross_units * scrap_rate))
                good_units = max(0, gross_units - scrap_units)

                wo_id = f"WO{wo_num:08d}"
                work_orders.append({
                    "work_order_id": wo_id,
                    "plant_id": plant_id,
                    "line_id": line_id,
                    "product_id": product_id,
                    "scheduled_start": shift_start,
                    "scheduled_end": shift_start + pd.Timedelta(minutes=scheduled_minutes),
                    "planned_qty": int(round(ideal_rate * 8 * 0.88)),
                    "order_status": "Completed",
                })

                production.append({
                    "production_id": f"PR{wo_num:08d}",
                    "work_order_id": wo_id,
                    "production_date": date.date(),
                    "shift_id": shift_id,
                    "plant_id": plant_id,
                    "line_id": line_id,
                    "product_id": product_id,
                    "scheduled_minutes": scheduled_minutes,
                    "planned_downtime_minutes": planned_dt,
                    "unplanned_downtime_minutes": min(unplanned_dt, max(0, total_dt-planned_dt)),
                    "operating_minutes": operating_minutes,
                    "ideal_rate_units_per_hour": round(ideal_rate, 3),
                    "total_units": gross_units,
                    "good_units": good_units,
                    "scrap_units": scrap_units,
                    "actual_run_rate_units_per_hour": round(gross_units / (operating_minutes/60), 3),
                })

                # Downtime events are linked to the same shift/work order.
                cursor = shift_start + pd.Timedelta(minutes=int(rng.integers(10, 50)))
                if planned_dt > 0:
                    cause = rng.choice(
                        list(DOWNTIME_CAUSES["planned"].keys()),
                        p=list(DOWNTIME_CAUSES["planned"].values())
                    )
                    downtime.append({
                        "downtime_event_id": f"DT{event_num:08d}",
                        "work_order_id": wo_id,
                        "plant_id": plant_id,
                        "line_id": line_id,
                        "machine_id": rng.choice(line_machines),
                        "shift_id": shift_id,
                        "event_start": cursor,
                        "event_end": cursor + pd.Timedelta(minutes=planned_dt),
                        "duration_minutes": planned_dt,
                        "downtime_type": "Planned",
                        "reason_code": cause,
                    })
                    event_num += 1
                    cursor += pd.Timedelta(minutes=planned_dt + 5)

                for machine_id, cause, duration in failure_records:
                    downtime.append({
                        "downtime_event_id": f"DT{event_num:08d}",
                        "work_order_id": wo_id,
                        "plant_id": plant_id,
                        "line_id": line_id,
                        "machine_id": machine_id,
                        "shift_id": shift_id,
                        "event_start": cursor,
                        "event_end": cursor + pd.Timedelta(minutes=duration),
                        "duration_minutes": duration,
                        "downtime_type": "Unplanned",
                        "reason_code": cause,
                    })
                    event_num += 1
                    cursor += pd.Timedelta(minutes=duration + 3)

                    # Failures often create corrective maintenance.
                    if cause in ["Mechanical Failure", "Electrical Fault", "Sensor/Controls Fault"]:
                        maintenance.append({
                            "maintenance_order_id": f"MO{maint_num:07d}",
                            "plant_id": plant_id,
                            "line_id": line_id,
                            "machine_id": machine_id,
                            "maintenance_type": "Corrective",
                            "opened_at": cursor - pd.Timedelta(minutes=duration),
                            "closed_at": cursor,
                            "labor_hours": round(duration / 60 * rng.uniform(0.7, 1.4), 2),
                            "failure_mode": cause,
                            "parts_cost": round(float(max(0, rng.lognormal(np.log(180), 0.9)-80)), 2),
                            "status": "Closed",
                        })
                        maint_num += 1
                        hours_since_pm[machine_id] = max(0, hours_since_pm[machine_id] - duration/60 * 4)

                # Quality records by defect type; total rejects reconcile to scrap units.
                if scrap_units > 0:
                    weights = rng.dirichlet(np.ones(len(DEFECT_TYPES))*1.1)
                    defect_counts = np.floor(weights * scrap_units).astype(int)
                    remainder = scrap_units - defect_counts.sum()
                    if remainder > 0:
                        defect_counts[:remainder] += 1
                    for defect, cnt in zip(DEFECT_TYPES, defect_counts):
                        if cnt == 0:
                            continue
                        quality.append({
                            "quality_event_id": f"QE{q_num:08d}",
                            "work_order_id": wo_id,
                            "plant_id": plant_id,
                            "line_id": line_id,
                            "product_id": product_id,
                            "shift_id": shift_id,
                            "inspection_time": shift_start + pd.Timedelta(minutes=int(rng.integers(60, 450))),
                            "defect_type": defect,
                            "defect_units": int(cnt),
                            "disposition": rng.choice(["Scrap", "Rework"], p=[0.78, 0.22]),
                        })
                        q_num += 1

                # Sensor snapshots every hour for each machine.
                # Values respond to health, failures, and operating state.
                for machine_id in line_machines:
                    machine = machine_map[machine_id]
                    health = machine["baseline_health_index"]
                    failure_on_machine = any(fr[0] == machine_id for fr in failure_records)
                    for h in range(8):
                        ts = shift_start + pd.Timedelta(hours=h)
                        running = not (failure_on_machine and rng.random() < 0.28)
                        load = np.clip(rng.normal(0.78 if running else 0.10, 0.08), 0.0, 1.05)
                        temp = 52 + 22*load + (1-health)*12 + rng.normal(0, 2.0)
                        vib = 1.7 + 2.8*load + (1-health)*4.0 + rng.normal(0, 0.35)
                        power = 18 + 55*load + rng.normal(0, 3.0)
                        if failure_on_machine and rng.random() < 0.18:
                            temp += rng.uniform(7, 15)
                            vib += rng.uniform(1.5, 3.5)
                        sensor_rows.append({
                            "timestamp": ts,
                            "plant_id": plant_id,
                            "line_id": line_id,
                            "machine_id": machine_id,
                            "run_state": "RUN" if running else "STOP",
                            "load_pct": round(load*100, 1),
                            "temperature_c": round(temp, 2),
                            "vibration_mm_s": round(max(vib, 0.2), 3),
                            "power_kw": round(max(power, 0), 2),
                        })

                    hours_since_pm[machine_id] += operating_minutes / 60

                    # Preventive maintenance on long intervals.
                    if hours_since_pm[machine_id] > rng.normal(520, 40):
                        duration = int(np.clip(rng.normal(80, 18), 45, 150))
                        pm_start = shift_start + pd.Timedelta(hours=8)
                        maintenance.append({
                            "maintenance_order_id": f"MO{maint_num:07d}",
                            "plant_id": plant_id,
                            "line_id": line_id,
                            "machine_id": machine_id,
                            "maintenance_type": "Preventive",
                            "opened_at": pm_start,
                            "closed_at": pm_start + pd.Timedelta(minutes=duration),
                            "labor_hours": round(duration/60 * rng.uniform(0.9, 1.3), 2),
                            "failure_mode": "Scheduled PM",
                            "parts_cost": round(float(rng.uniform(25, 250)), 2),
                            "status": "Closed",
                        })
                        maint_num += 1
                        hours_since_pm[machine_id] = float(rng.uniform(0, 40))

                wo_num += 1

    return (
        pd.DataFrame(work_orders),
        pd.DataFrame(production),
        pd.DataFrame(downtime),
        pd.DataFrame(quality),
        pd.DataFrame(maintenance),
        pd.DataFrame(sensor_rows),
    )


def build_kpi_table(production):
    df = production.copy()
    df["availability"] = df["operating_minutes"] / (
        df["scheduled_minutes"] - df["planned_downtime_minutes"]
    ).clip(lower=1)

    theoretical_output = (
        df["operating_minutes"] / 60 * df["ideal_rate_units_per_hour"]
    ).clip(lower=1)
    df["performance"] = df["total_units"] / theoretical_output
    df["quality"] = df["good_units"] / df["total_units"].replace(0, np.nan)

    # OEE capped at 1 because synthetic noise could otherwise make performance > 100%.
    df["availability"] = df["availability"].clip(0, 1)
    df["performance"] = df["performance"].clip(0, 1)
    df["quality"] = df["quality"].clip(0, 1)
    df["oee"] = df["availability"] * df["performance"] * df["quality"]
    df["scrap_rate"] = df["scrap_units"] / df["total_units"].replace(0, np.nan)
    return df


def create_source_system_extracts(outdir, dims, tables):
    dim_plant, dim_line, dim_machine, dim_product, dim_shift = dims
    work_orders, production, downtime, quality, maintenance, sensors = tables

    # ERP-like extracts
    erp_dir = outdir / "source_systems" / "erp"
    mes_dir = outdir / "source_systems" / "mes"
    qms_dir = outdir / "source_systems" / "qms"
    cmms_dir = outdir / "source_systems" / "cmms"
    scada_dir = outdir / "source_systems" / "scada"
    for d in [erp_dir, mes_dir, qms_dir, cmms_dir, scada_dir]:
        d.mkdir(parents=True, exist_ok=True)

    dim_product.to_csv(erp_dir / "product_master.csv", index=False)
    work_orders[[
        "work_order_id","plant_id","product_id","scheduled_start","scheduled_end","planned_qty","order_status"
    ]].to_csv(erp_dir / "work_orders.csv", index=False)

    production.to_csv(mes_dir / "production_runs.csv", index=False)
    downtime.to_csv(mes_dir / "downtime_events.csv", index=False)
    quality.to_csv(qms_dir / "quality_events.csv", index=False)
    maintenance.to_csv(cmms_dir / "maintenance_work_orders.csv", index=False)
    sensors.to_csv(scada_dir / "machine_telemetry.csv", index=False)


def create_multiplant_local_extracts(outdir, production, downtime):
    # Project 3 deliberately introduces realistic local-system inconsistency.
    # This is not "dirty randomness"; it is controlled schema heterogeneity.
    mp = outdir / "project3_multiplant_local"
    mp.mkdir(parents=True, exist_ok=True)

    plant_ids = sorted(production["plant_id"].unique())
    code_maps = {
        plant_ids[0]: {
            "Mechanical Failure":"MECH","Electrical Fault":"ELEC","Material Starvation":"MAT",
            "Quality Hold":"QH","Sensor/Controls Fault":"CTRL","Operator Adjustment":"OP",
            "Utility Interruption":"UTIL","Changeover":"CO","Preventive Maintenance":"PM",
            "Cleaning/Sanitation":"CLEAN","Planned Inspection":"INSP"
        },
        plant_ids[1]: {
            "Mechanical Failure":"M01","Electrical Fault":"E01","Material Starvation":"S01",
            "Quality Hold":"Q01","Sensor/Controls Fault":"C01","Operator Adjustment":"O01",
            "Utility Interruption":"U01","Changeover":"C/O","Preventive Maintenance":"P/M",
            "Cleaning/Sanitation":"SAN","Planned Inspection":"PI"
        },
        plant_ids[2]: {
            "Mechanical Failure":"BREAKDOWN","Electrical Fault":"ELECTRICAL","Material Starvation":"NO_MATERIAL",
            "Quality Hold":"QUALITY","Sensor/Controls Fault":"AUTOMATION","Operator Adjustment":"ADJUST",
            "Utility Interruption":"UTILITY","Changeover":"CHANGEOVER","Preventive Maintenance":"PREV_MAINT",
            "Cleaning/Sanitation":"CLEANING","Planned Inspection":"INSPECTION"
        },
    }

    for i, plant in enumerate(plant_ids):
        p_prod = production.loc[production["plant_id"] == plant].copy()
        p_dt = downtime.loc[downtime["plant_id"] == plant].copy()

        if i == 0:
            # ISO-ish names, minutes
            p_prod.rename(columns={
                "production_date":"prod_date","shift_id":"shift","total_units":"total_count",
                "good_units":"good_count","scrap_units":"reject_count"
            }, inplace=True)
            p_dt["local_reason_code"] = p_dt["reason_code"].map(code_maps[plant])
        elif i == 1:
            # Different names, seconds for downtime
            p_prod.rename(columns={
                "production_date":"date","shift_id":"crew","total_units":"qty_total",
                "good_units":"qty_good","scrap_units":"qty_scrap"
            }, inplace=True)
            p_dt["duration_seconds"] = p_dt["duration_minutes"] * 60
            p_dt["local_reason_code"] = p_dt["reason_code"].map(code_maps[plant])
            p_dt = p_dt.drop(columns=["duration_minutes"])
        else:
            # Shift encoded numerically, date string MM/DD/YYYY
            p_prod["production_date"] = pd.to_datetime(p_prod["production_date"]).dt.strftime("%m/%d/%Y")
            p_prod["shift_id"] = p_prod["shift_id"].map({"A":1, "B":2, "C":3})
            p_prod.rename(columns={
                "production_date":"production_day","shift_id":"shift_no","total_units":"produced",
                "good_units":"accepted","scrap_units":"scrapped"
            }, inplace=True)
            p_dt["local_reason_code"] = p_dt["reason_code"].map(code_maps[plant])

        p_prod.to_csv(mp / f"{plant}_production_local.csv", index=False)
        p_dt.to_csv(mp / f"{plant}_downtime_local.csv", index=False)

    # Mapping table required to standardize local downtime codes.
    mapping_rows = []
    for plant, cmap in code_maps.items():
        for std, local in cmap.items():
            mapping_rows.append({
                "plant_id": plant,
                "local_reason_code": local,
                "standard_reason": std,
                "standard_category": "Planned" if std in DOWNTIME_CAUSES["planned"] else "Unplanned",
            })
    pd.DataFrame(mapping_rows).to_csv(mp / "downtime_reason_mapping.csv", index=False)


def inject_quality_issues(outdir, production, downtime, rng):
    # Deliberately create a SMALL separate bad-data sample for QA exercises.
    qa_dir = outdir / "project2_qa_exercises"
    qa_dir.mkdir(parents=True, exist_ok=True)

    prod = production.sample(min(800, len(production)), random_state=7).copy()
    dt = downtime.sample(min(300, len(downtime)), random_state=11).copy()

    issues = []

    if len(prod) >= 20:
        idx = prod.sample(3, random_state=1).index
        prod.loc[idx, "line_id"] = None
        issues += [("production","missing_line_id",str(i)) for i in idx]

        idx = prod.sample(2, random_state=2).index
        prod.loc[idx, "scrap_units"] = prod.loc[idx, "total_units"] + 5
        issues += [("production","scrap_gt_total",str(i)) for i in idx]

        duplicate = prod.sample(2, random_state=3)
        prod = pd.concat([prod, duplicate], ignore_index=True)
        issues += [("production","duplicate_row","appended")]

    if len(dt) >= 10:
        idx = dt.sample(2, random_state=4).index
        dt.loc[idx, "duration_minutes"] = -15
        issues += [("downtime","negative_duration",str(i)) for i in idx]

    prod.to_csv(qa_dir / "production_with_known_issues.csv", index=False)
    dt.to_csv(qa_dir / "downtime_with_known_issues.csv", index=False)
    pd.DataFrame(issues, columns=["table_name","issue_type","reference"]).to_csv(
        qa_dir / "known_issues_manifest.csv", index=False
    )


def validate(production, downtime, quality):
    checks = []

    def add(name, passed, value):
        checks.append({"check": name, "passed": bool(passed), "value": value})

    add("good_plus_scrap_equals_total",
        ((production["good_units"] + production["scrap_units"]) == production["total_units"]).all(),
        int(((production["good_units"] + production["scrap_units"]) != production["total_units"]).sum()))

    add("operating_time_nonnegative",
        (production["operating_minutes"] >= 0).all(),
        int((production["operating_minutes"] < 0).sum()))

    add("downtime_duration_positive",
        (downtime["duration_minutes"] > 0).all() if len(downtime) else True,
        int((downtime["duration_minutes"] <= 0).sum()) if len(downtime) else 0)

    q = quality.groupby("work_order_id")["defect_units"].sum()
    p = production.set_index("work_order_id")["scrap_units"]
    common = q.index.intersection(p.index)
    add("quality_defects_reconcile_to_scrap",
        (q.loc[common] == p.loc[common]).all(),
        int((q.loc[common] != p.loc[common]).sum()))

    return pd.DataFrame(checks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="generated_data")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--days", type=int, default=180)
    args = parser.parse_args()

    cfg = Config(seed=args.seed, days=args.days)
    rng = np.random.default_rng(cfg.seed)
    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)

    dims = make_dimensions(cfg, rng)
    dim_plant, dim_line, dim_machine, dim_product, dim_shift = dims
    orders = generate_orders(cfg, dim_plant, dim_product, rng)
    tables = generate_production(cfg, dims, orders, rng)
    work_orders, production, downtime, quality, maintenance, sensors = tables
    kpis = build_kpi_table(production)

    # Core warehouse-ready files
    core = outdir / "core"
    core.mkdir(parents=True, exist_ok=True)
    dim_plant.to_csv(core / "dim_plant.csv", index=False)
    dim_line.to_csv(core / "dim_line.csv", index=False)
    dim_machine.to_csv(core / "dim_machine.csv", index=False)
    dim_product.to_csv(core / "dim_product.csv", index=False)
    dim_shift.to_csv(core / "dim_shift.csv", index=False)
    orders.to_csv(core / "erp_sales_orders.csv", index=False)
    work_orders.to_csv(core / "fact_work_order.csv", index=False)
    production.to_csv(core / "fact_production.csv", index=False)
    downtime.to_csv(core / "fact_downtime.csv", index=False)
    quality.to_csv(core / "fact_quality.csv", index=False)
    maintenance.to_csv(core / "fact_maintenance.csv", index=False)
    sensors.to_csv(core / "fact_sensor_hourly.csv", index=False)
    kpis.to_csv(core / "fact_production_with_kpis.csv", index=False)

    create_source_system_extracts(outdir, dims, tables)
    create_multiplant_local_extracts(outdir, production, downtime)
    inject_quality_issues(outdir, production, downtime, rng)

    validation = validate(production, downtime, quality)
    validation.to_csv(outdir / "validation_report.csv", index=False)

    metadata = {
        "seed": cfg.seed,
        "start_date": cfg.start_date,
        "days": cfg.days,
        "plants": cfg.plants,
        "lines_per_plant": cfg.lines_per_plant,
        "machines_per_line": cfg.machines_per_line,
        "products": cfg.products,
        "rows": {
            "orders": len(orders),
            "work_orders": len(work_orders),
            "production": len(production),
            "downtime": len(downtime),
            "quality": len(quality),
            "maintenance": len(maintenance),
            "sensor_hourly": len(sensors),
        }
    }
    (outdir / "generation_metadata.json").write_text(
        __import__("json").dumps(metadata, indent=2)
    )

    print("Synthetic manufacturing dataset generated.")
    print(__import__("json").dumps(metadata, indent=2))
    print("\nValidation:")
    print(validation.to_string(index=False))


if __name__ == "__main__":
    main()
