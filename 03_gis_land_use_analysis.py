import pandas as pd
from shapely.geometry import Polygon

# SIMULASI DATA SPASIAL BIDANG LAHAN (PARCEL GEOMETRY & ATRIBUT)
parcels_data = [
    {
        "parcel_id": "P001",
        "owner": "Kelompok Tani Tani Makmur",
        "initial_type": "Pertanian Padi",
        "coordinates": [(102.25, -3.80), (102.26, -3.80), (102.26, -3.81), (102.25, -3.81)]
    },
    {
        "parcel_id": "P002",
        "owner": "PT Perumahan Asri",
        "initial_type": "Pertanian Padi",
        "coordinates": [(102.27, -3.82), (102.28, -3.82), (102.28, -3.83), (102.27, -3.83)]
    },
    {
        "parcel_id": "P003",
        "owner": "H. Sukri",
        "initial_type": "Pertanian Padi",
        "coordinates": [(102.29, -3.84), (102.295, -3.84), (102.295, -3.845), (102.29, -3.845)]
    }
]

# Data status verifikasi lapangan terbaru
field_survey = {
    "P001": {"current_status": "Padi Produktif", "building_density_pct": 2.0},
    "P002": {"current_status": "Konstruksi Perumahan", "building_density_pct": 78.5},
    "P003": {"current_status": "Padi Produktif", "building_density_pct": 0.0}
}

def calculate_polygon_area_ha(coords):
    """Menghitung estimasi luas poligon spasial dalam satuan Hektar (Ha)."""
    poly = Polygon(coords)
    area_deg2 = poly.area
    area_m2 = area_deg2 * (111320 ** 2)
    return round(area_m2 / 10000, 2)

def process_spatial_land_use(parcels, survey_data):
    results = []
    
    for item in parcels:
        pid = item["parcel_id"]
        area_ha = calculate_polygon_area_ha(item["coordinates"])
        
        survey = survey_data.get(pid, {"current_status": "Unknown", "building_density_pct": 0.0})
        status = survey["current_status"]
        density = survey["building_density_pct"]
        
        # Logika Otomasi Identifikasi Alih Fungsi Lahan (LP2B Violation Check)
        if item["initial_type"] == "Pertanian Padi" and density > 20.0:
            risk_category = "TERINDIKASI ALIH FUNGSI (SANKSI LP2B)"
        else:
            risk_category = "AMAN / AMANAH LP2B"
            
        results.append({
            "Parcel_ID": pid,
            "Pemilik": item["owner"],
            "Tipe_Awal": item["initial_type"],
            "Status_Lapangan": status,
            "Luas_Hektar": area_ha,
            "Kepadatan_Bangunan_Pct": density,
            "Kategori_Analisis": risk_category
        })
        
    return pd.DataFrame(results)

if __name__ == "__main__":
    print("=== OTOMASI ANALISIS DATA SPASIAL PENGGUNAAN LAHAN (LP2B GIS) ===")
    df_result = process_spatial_land_use(parcels_data, field_survey)
    
    print("\n--- HASIL PEMROSESAN ATRIBUT DAN GEOMETRI LAHAN ---")
    print(df_result.to_string(index=False))
    
    converted_area = df_result[df_result['Kategori_Analisis'].str.contains('ALIH FUNGSI')]['Luas_Hektar'].sum()
    print(f"\nTotal Luas Lahan Terindikasi Alih Fungsi Ilegal: {converted_area} Ha")