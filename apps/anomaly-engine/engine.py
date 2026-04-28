import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class DataObservabilityEngine:
    def __init__(self):
        self.logger = logging.getLogger("anomaly-engine")

    def detect_freshness_breach(self, last_update: datetime, sla_mins: int):
        """
        Detects if a dataset has breached its freshness SLA.
        """
        now = datetime.now()
        latency = (now - last_update).total_seconds() / 60
        
        is_breach = latency > sla_mins
        if is_breach:
            self.logger.warning(f"SLA Breach: Latency {latency:.1f}m exceeds SLA {sla_mins}m")
            
        return {
            "is_breach": is_breach,
            "latency_mins": round(latency, 2),
            "sla_mins": sla_mins
        }

    def detect_volume_anomaly(self, current_count: int, historical_counts: list):
        """
        Uses statistical variance to detect anomalies in data volume.
        """
        if not historical_counts:
            return {"is_anomaly": False, "z_score": 0}
            
        mean = np.mean(historical_counts)
        std = np.std(historical_counts)
        
        if std == 0:
            return {"is_anomaly": False, "z_score": 0}
            
        z_score = abs(current_count - mean) / std
        is_anomaly = z_score > 3.0 # Standard 3-sigma threshold
        
        if is_anomaly:
            self.logger.warning(f"Volume Anomaly: Current count {current_count} is {z_score:.2f} std devs from mean {mean:.1f}")
            
        return {
            "is_anomaly": is_anomaly,
            "z_score": round(z_score, 2),
            "current": current_count,
            "expected_mean": round(mean, 1)
        }

    def detect_schema_drift(self, current_schema: dict, baseline_schema: dict):
        """
        Identifies breaking changes in dataset structure.
        """
        drift_found = False
        changes = []
        
        # Check for dropped columns
        for col in baseline_schema:
            if col not in current_schema:
                drift_found = True
                changes.append(f"CRITICAL: Column '{col}' dropped")
                
        # Check for type changes
        for col, dtype in current_schema.items():
            if col in baseline_schema and baseline_schema[col] != dtype:
                drift_found = True
                changes.append(f"WARNING: Column '{col}' type changed from {baseline_schema[col]} to {dtype}")
                
        return {
            "drift_found": drift_found,
            "changes": changes
        }

if __name__ == "__main__":
    engine = DataObservabilityEngine()
    
    # Test Freshness
    last_run = datetime.now() - timedelta(hours=2)
    print(f"Freshness Check: {engine.detect_freshness_breach(last_run, 60)}")
    
    # Test Volume
    history = [1000, 1100, 950, 1050, 1020]
    print(f"Volume Check: {engine.detect_volume_anomaly(500, history)}")
    
    # Test Schema
    baseline = {"id": "int", "name": "string", "rev": "decimal"}
    current = {"id": "int", "rev": "float"}
    print(f"Schema Check: {engine.detect_schema_drift(current, baseline)}")
