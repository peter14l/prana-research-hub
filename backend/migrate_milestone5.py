"""
PRANA Research Hub - Milestone 5 Database Migration & Evidence Recalibration
Applies strict evidence integrity rules:
1. Adds audit trail and recalibration columns to candidate_opportunities.
2. Corrects the Jalan candidate:
   - Removes unsupported 2,000+ unit claim
   - Corrects distance to 8.56 km [DERIVED_RESULT]
   - Removes unsupported Padmapukur midnight PM2.5 spike claim
   - Reclassifies NW wind association as an untested hypothesis
   - Removes VIIRS anomaly claims until actual data is ingested
   - Recalibrates evidence strength to 3.5 / 10
3. Audits and recalibrates all other candidates (Foundry, Landfill, Ferry).
4. Stores separate rebuilt scores across 6 distinct dimensions.
5. Updates GAP-001 description to remove unreferenced unit claim.
"""
import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "prana.db")

def run_migration():
    print(f"Running Milestone 5 Evidence Recalibration migration on {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Add Milestone 5 audit columns to candidate_opportunities if not exist
    cursor.execute("PRAGMA table_info(candidate_opportunities)")
    existing_cols = [row[1] for row in cursor.fetchall()]

    new_columns = [
        ("pre_audit_evidence_score", "REAL"),
        ("pre_audit_priority_score", "REAL"),
        ("evidence_audit_breakdown", "TEXT"),
        ("has_synthetic_dependency", "BOOLEAN DEFAULT 0"),
        ("has_unverified_claims", "BOOLEAN DEFAULT 0"),
        ("verified_evidence_summary", "TEXT"),
        ("missing_evidence_summary", "TEXT"),
        ("derived_distance_km", "REAL"),
        ("rebuilt_scores", "TEXT")
    ]

    for col_name, col_type in new_columns:
        if col_name not in existing_cols:
            cursor.execute(f"ALTER TABLE candidate_opportunities ADD COLUMN {col_name} {col_type}")
            print(f"Added column {col_name} to candidate_opportunities")

    # 2. Recalibrate Candidate 1: howrah-foundry-cupola-retrofit
    foundry_audit = [
        {
            "claim": "Industrial sector contributes 34% of winter PM2.5 in Ghusuri",
            "status": "PUBLISHED_RESEARCH",
            "citation": "CSIR-NEERI (2020) Table 6.14, p. 148",
            "support_type": "DIRECT_SUPPORT",
            "notes": "Direct chemical mass balance receptor modeling result for Howrah North."
        },
        {
            "claim": "Ghusuri statutory CAAQM station (site_5008) records highest regional PM2.5",
            "status": "VERIFIED_OBSERVATION",
            "citation": "CPCB site_5008 statutory monitoring registry",
            "support_type": "DIRECT_SUPPORT",
            "notes": "Verified station coordinates (22.6074°N, 88.3496°E) and statutory multi-year exceedance."
        },
        {
            "claim": "WBPCB 2022 Foundry Cluster Environmental Audit",
            "status": "MISSING_EVIDENCE",
            "citation": "Unfulfilled document citation",
            "support_type": "MISSING_IN_DB",
            "notes": "The 2022 survey document is not stored or cataloged in PRANA research_documents."
        },
        {
            "claim": "~350 artisanal coke-fired cold blast cupolas",
            "status": "UNVERIFIED_HYPOTHESIS",
            "citation": "Unreferenced narrative text",
            "support_type": "UNVERIFIED",
            "notes": "No official MSME census or factory registration register is cataloged in DB."
        }
    ]

    foundry_rebuilt = {
        "pollution_impact_potential": 9.2,
        "evidence_strength": 6.8,
        "engineering_feasibility": 7.0,
        "prototype_affordability": 6.5,
        "verification_feasibility": 8.8,
        "partnership_feasibility": 8.2
    }

    cursor.execute("""
        UPDATE candidate_opportunities SET
            pre_audit_evidence_score = 9.5,
            pre_audit_priority_score = 8.33,
            evidence_strength_score = 6.8,
            supporting_evidence = ?,
            evidence_audit_breakdown = ?,
            has_synthetic_dependency = 0,
            has_unverified_claims = 1,
            verified_evidence_summary = ?,
            missing_evidence_summary = ?,
            derived_distance_km = NULL,
            rebuilt_scores = ?
        WHERE slug = 'howrah-foundry-cupola-retrofit'
    """, (
        "Verified Evidence: (1) CSIR-NEERI (2020) Table 6.14, p. 148 confirms industrial emissions contribute 34% of winter PM2.5 in Ghusuri [PUBLISHED_RESEARCH - DIRECT SUPPORT]; (2) CPCB Ghusuri station site_5008 telemetry records continuous winter NAAQS exceedance [VERIFIED_OBSERVATION]. Missing / Unverified Claims: (3) WBPCB 2022 survey document is uninventoried in DB [MISSING_EVIDENCE]; (4) Operating census of ~350 cupola units is unreferenced [UNVERIFIED_HYPOTHESIS].",
        json.dumps(foundry_audit),
        "CSIR-NEERI (2020) Table 6.14 directly supports 34% winter industrial PM2.5 in Ghusuri [PUBLISHED_RESEARCH]; Ghusuri site_5008 statutory telemetry records persistent severe winter exceedance [VERIFIED_OBSERVATION].",
        "WBPCB 2022 Foundry Cluster Survey cited in candidate text is uninventoried in PRANA; operating cupola unit count is unreferenced in DB [MISSING_EVIDENCE].",
        json.dumps(foundry_rebuilt)
    ))
    print("Recalibrated howrah-foundry-cupola-retrofit (evidence: 9.5 -> 6.8)")

    # 3. Recalibrate Candidate 2: industrial-fence-line-attribution (Jalan Complex)
    jalan_audit = [
        {
            "claim": "2,000+ industrial units in Jalan Industrial Complex",
            "status": "UNVERIFIED_HYPOTHESIS",
            "citation": "Unreferenced narrative text",
            "support_type": "UNVERIFIED",
            "notes": "No DIC, MSME census, or official industrial park register exists in the database."
        },
        {
            "claim": "7.2 km monitoring gap to nearest statutory station",
            "status": "DERIVED_RESULT",
            "citation": "Padmapukur site_5010 coordinates (22.5632°N, 88.3182°E)",
            "support_type": "DIRECT_SUPPORT",
            "notes": "Exact Haversine geodesic distance from Jalan centroid (22.59°N, 88.24°E) to Padmapukur is 8.56 km (>7 km). Coordinates are statutory verified ground truth."
        },
        {
            "claim": "Padmapukur station displays sharp nocturnal PM2.5 spikes > 180 µg/m³",
            "status": "SYNTHETIC_DATA",
            "citation": "validated_observations (station_id 9)",
            "support_type": "NOT_FOUND_IN_DATA",
            "notes": "Zero midnight-to-dawn observations > 180 µg/m³ exist in the Padmapukur dataset. The only 2 readings > 180 µg/m³ occurred at midday (12:00 PM and 1:00 PM) on 2026-11-19 and are synthetic DEMO records."
        },
        {
            "claim": "Nocturnal spikes associated with calm north-westerly wind regimes",
            "status": "UNVERIFIED_HYPOTHESIS",
            "citation": "Open-Meteo reanalysis weather records",
            "support_type": "UNTESTED_HYPOTHESIS",
            "notes": "Synoptic NW reanalysis weather exists in DB, but the causal correlation to Padmapukur concentrations is an unlinked, untested hypothesis."
        },
        {
            "claim": "Satellite VIIRS day/night band radiance anomalies",
            "status": "MISSING_EVIDENCE",
            "citation": "Unfulfilled satellite citation",
            "support_type": "MISSING_IN_DB",
            "notes": "Zero NASA VIIRS radiance values, fire vectors, or satellite files exist in PRANA."
        }
    ]

    jalan_rebuilt = {
        "pollution_impact_potential": 7.2,
        "evidence_strength": 3.5,
        "engineering_feasibility": 8.5,
        "prototype_affordability": 8.7,
        "verification_feasibility": 9.2,
        "partnership_feasibility": 8.5
    }

    cursor.execute("""
        UPDATE candidate_opportunities SET
            problem_statement = ?,
            geographic_relevance = ?,
            pre_audit_evidence_score = 8.8,
            pre_audit_priority_score = 8.44,
            evidence_strength_score = 3.5,
            supporting_evidence = ?,
            evidence_audit_breakdown = ?,
            has_synthetic_dependency = 1,
            has_unverified_claims = 1,
            verified_evidence_summary = ?,
            missing_evidence_summary = ?,
            derived_distance_km = 8.56,
            rebuilt_scores = ?
        WHERE slug = 'industrial-fence-line-attribution'
    """, (
        "Major unmonitored peri-urban industrial agglomerations in the Jalan–Sankrail corridor operate completely outside the statutory CAAQM network, with the nearest statutory station located at a derived distance of 8.56 km. Discontinuous emissions escape regulatory detection, while downwind populations experience unmonitored exposure.",
        "Jalan Industrial Complex, NH-6 / Bombay Road, Domjur–Sankrail corridor, Howrah (22.59°N, 88.24°E). Nearest statutory station: Padmapukur (site_5010) at 8.56 km [DERIVED_RESULT from VERIFIED_OBSERVATION].",
        "Verified Evidence: (1) PRANA Station Verification Dossier confirms a derived monitoring gap of 8.56 km to the nearest statutory CAAQM station (Padmapukur site_5010) calculated from verified coordinates [DERIVED_RESULT from VERIFIED_OBSERVATION]. Untested Hypotheses: (2) Calm nocturnal north-westerly wind regimes may transport industrial emissions toward urban residential areas [UNVERIFIED_HYPOTHESIS]. Missing Evidence: (3) Local industrial unit census (claimed 2,000+ units), continuous nocturnal PM2.5 ground measurements, and NASA VIIRS satellite nighttime radiance data are currently uninventoried in the PRANA database [MISSING_EVIDENCE].",
        json.dumps(jalan_audit),
        "Geodesic monitoring gap of 8.56 km from Jalan centroid to Padmapukur CAAQM station (site_5010) mathematically derived via Haversine formula from statutory verified coordinates [DERIVED_RESULT from VERIFIED_OBSERVATION].",
        "2,000+ industrial unit census is unreferenced in DB; claimed midnight-to-dawn PM2.5 spikes > 180 µg/m³ do NOT exist in database records; NASA VIIRS satellite radiance data is missing [MISSING_EVIDENCE].",
        json.dumps(jalan_rebuilt)
    ))
    print("Recalibrated industrial-fence-line-attribution (evidence: 8.8 -> 3.5, distance: 8.56 km)")

    # 4. Recalibrate Candidate 3: landfill-fire-thermal-suppression (Dhapa)
    dhapa_audit = [
        {
            "claim": "Municipal solid waste & biomass burning contributes 14% of winter PM2.5",
            "status": "PUBLISHED_RESEARCH",
            "citation": "TERI (2025) Table 4.6, p. 87",
            "support_type": "REGIONAL_CONTEXT",
            "notes": "Statutory chemical mass balance finding for the entire Kolkata airshed; provides regional context but does not measure isolated Dhapa emissions."
        },
        {
            "claim": "NASA VIIRS satellite thermal anomaly hot spots at Dhapa coordinates",
            "status": "MISSING_EVIDENCE",
            "citation": "Unfulfilled satellite citation",
            "support_type": "MISSING_IN_DB",
            "notes": "Zero NASA VIIRS radiance values or fire detection coordinates exist in PRANA."
        },
        {
            "claim": "Elevated nocturnal CO at Ballygunge and Victoria stations under easterly winds",
            "status": "UNVERIFIED_HYPOTHESIS",
            "citation": "Unverified causal link",
            "support_type": "UNTESTED_HYPOTHESIS",
            "notes": "Ground CO telemetry exists, but the direct causal association linking Dhapa fires to specific station CO spikes is an unvalidated hypothesis."
        },
        {
            "claim": "4,000 tonnes/day waste intake across 50 hectares",
            "status": "UNVERIFIED_HYPOTHESIS",
            "citation": "Unreferenced narrative text",
            "support_type": "UNVERIFIED",
            "notes": "No municipal weighbridge records or KMC solid waste reports are cataloged in DB."
        }
    ]

    dhapa_rebuilt = {
        "pollution_impact_potential": 8.4,
        "evidence_strength": 4.2,
        "engineering_feasibility": 7.8,
        "prototype_affordability": 7.5,
        "verification_feasibility": 8.6,
        "partnership_feasibility": 7.9
    }

    cursor.execute("""
        UPDATE candidate_opportunities SET
            pre_audit_evidence_score = 8.5,
            pre_audit_priority_score = 8.21,
            evidence_strength_score = 4.2,
            supporting_evidence = ?,
            evidence_audit_breakdown = ?,
            has_synthetic_dependency = 0,
            has_unverified_claims = 1,
            verified_evidence_summary = ?,
            missing_evidence_summary = ?,
            derived_distance_km = NULL,
            rebuilt_scores = ?
        WHERE slug = 'landfill-fire-thermal-suppression'
    """, (
        "Verified Regional Context: (1) TERI (2025) Table 4.6 documents municipal solid waste and biomass burning as contributing 14% of winter PM2.5 regionally across Kolkata [PUBLISHED_RESEARCH - REGIONAL CONTEXT]. Untested Hypotheses: (2) Causal link between Dhapa fires and nocturnal CO spikes at Ballygunge and Victoria stations is unlinked in DB [UNVERIFIED_HYPOTHESIS]. Missing Evidence: (3) Dhapa municipal intake weighbridge records, NASA VIIRS 375m thermal infrared fire detections, and subsurface methane/isotherm profiling are uninventoried in DB [MISSING_EVIDENCE].",
        json.dumps(dhapa_audit),
        "TERI (2025) Table 4.6 documents 14% regional winter PM2.5 share for municipal solid waste and biomass burning [PUBLISHED_RESEARCH - REGIONAL CONTEXT].",
        "NASA VIIRS thermal infrared anomaly records at Dhapa coordinates are missing from DB; 4,000 tonnes/day intake figure is unverified in DB [MISSING_EVIDENCE].",
        json.dumps(dhapa_rebuilt)
    ))
    print("Recalibrated landfill-fire-thermal-suppression (evidence: 8.5 -> 4.2)")

    # 5. Recalibrate Candidate 4: hooghly-ferry-exhaust-retrofit
    ferry_audit = [
        {
            "claim": "River transport identified as uninventoried high-exposure hotspot",
            "status": "PUBLISHED_RESEARCH",
            "citation": "TERI (2025) Section 3.4",
            "support_type": "GAP_ACKNOWLEDGEMENT",
            "notes": "Acknowledges river craft emissions as an uninventoried research deficit, but does not provide empirical emission factors."
        },
        {
            "claim": "100,000 daily commuters across 32 river ghats",
            "status": "UNVERIFIED_HYPOTHESIS",
            "citation": "Unreferenced narrative text",
            "support_type": "UNVERIFIED",
            "notes": "No ticketing records or port commuter censuses exist in the database."
        },
        {
            "claim": "WBSTC fleet records reveal 40+ year-old mechanical diesels operating >14 hrs/day",
            "status": "MISSING_EVIDENCE",
            "citation": "Unfulfilled fleet citation",
            "support_type": "MISSING_IN_DB",
            "notes": "No WBSTC vessel data sheets or engine specifications exist in research_documents."
        },
        {
            "claim": "Near-river monitoring shows micro-spikes during passenger ferry departure bursts",
            "status": "MISSING_EVIDENCE",
            "citation": "Unfulfilled observation citation",
            "support_type": "MISSING_IN_DB",
            "notes": "Zero dockside or mobile ferry monitoring observations exist in validated_observations."
        }
    ]

    ferry_rebuilt = {
        "pollution_impact_potential": 7.5,
        "evidence_strength": 2.0,
        "engineering_feasibility": 7.2,
        "prototype_affordability": 7.0,
        "verification_feasibility": 8.5,
        "partnership_feasibility": 8.0
    }

    cursor.execute("""
        UPDATE candidate_opportunities SET
            pre_audit_evidence_score = 6.8,
            pre_audit_priority_score = 7.55,
            evidence_strength_score = 2.0,
            supporting_evidence = ?,
            evidence_audit_breakdown = ?,
            has_synthetic_dependency = 0,
            has_unverified_claims = 1,
            verified_evidence_summary = ?,
            missing_evidence_summary = ?,
            derived_distance_km = NULL,
            rebuilt_scores = ?
        WHERE slug = 'hooghly-ferry-exhaust-retrofit'
    """, (
        "Acknowledged Data Gap: (1) TERI (2025) Section 3.4 identifies river marine transport as an uninventoried source gap in official state emission inventories [PUBLISHED_RESEARCH - GAP ACKNOWLEDGEMENT]. Missing Evidence: (2) Empirical tailpipe emission factors, WBSTC marine diesel engine logs, and near-ghat pedestrian exposure micro-sensor records are completely absent from the database [MISSING_EVIDENCE].",
        json.dumps(ferry_audit),
        "TERI (2025) Section 3.4 acknowledges river marine craft as an uninventoried emission source in the Kolkata airshed [PUBLISHED_RESEARCH - GAP ACKNOWLEDGEMENT].",
        "Zero empirical tailpipe emission factors, engine hours, or near-ghat micro-sensor observations exist in PRANA [MISSING_EVIDENCE].",
        json.dumps(ferry_rebuilt)
    ))
    print("Recalibrated hooghly-ferry-exhaust-retrofit (evidence: 6.8 -> 2.0)")

    # 6. Correct GAP-001 in research_gaps
    cursor.execute("""
        UPDATE research_gaps SET
            description = 'Over unmonitored peri-urban industrial fabrication, casting, and chemical zones in the Jalan–Sankrail–Uluberia corridor, the nearest statutory CAAQM station (Padmapukur site_5010) is located at a derived distance of 8.56 km, leaving emissions unmonitored by statutory ground stations.'
        WHERE gap_code = 'GAP-001'
    """)
    print("Updated research_gaps GAP-001 description (removed 2,500 units claim, updated to 8.56 km derived distance)")

    conn.commit()
    conn.close()
    print("Milestone 5 Evidence Recalibration migration completed successfully.")

if __name__ == "__main__":
    run_migration()
