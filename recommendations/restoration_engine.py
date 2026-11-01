def calculate_restoration_index(veg_coverage_pct, soil_moisture_pct, slope_risk=15.0, ecological_weight=20.0):
    veg_score = max(0, 100 - veg_coverage_pct) * 0.35
    moisture_score = max(0, 100 - soil_moisture_pct) * 0.30
    slope_score = slope_risk * 0.20
    eco_score = ecological_weight * 0.15
    
    total_score = round(veg_score + moisture_score + slope_score + eco_score, 1)
    total_score = min(100.0, max(0.0, total_score))
    
    if total_score >= 70:
        status = "URGENT RESTORATION"
        color = "red"
        action = "Immediate native pioneer tree planting (e.g., Shorea spp., Dipterocarps). Establish drip irrigation."
        irrigation_plan = "High Flow Priority (Daily 12L/m²)"
    elif 40 <= total_score < 70:
        status = "MONITOR & ASSIST"
        color = "yellow"
        action = "Enrichment planting with secondary successional species. Assess soil organic matter."
        irrigation_plan = "Moderate Supplemental Priority (Bi-weekly 5L/m²)"
    else:
        status = "STABLE / HEALTHY"
        color = "green"
        action = "Routine canopy preservation and conservation monitoring."
        irrigation_plan = "No immediate irrigation needed"
        
    return {
        "index_score": total_score,
        "status": status,
        "status_color": color,
        "action_plan": action,
        "irrigation_plan": irrigation_plan
    }